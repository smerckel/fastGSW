"""Test suite for fast_gsw.

fast_gsw wraps a compiled C library (via ctypes) that reimplements a handful
of TEOS-10 / GSW functions (rho, pot_rho, CT, SA) for fast, vectorized CTD
processing. The `gsw` package (pure Python reference implementation) is used
here as an independent oracle to check numerical correctness.
"""
import numpy as np
import pytest

import fast_gsw
from fast_gsw import Caller

# Conductivity/temperature/pressure profile, reused at several fixed
# locations around the globe.
C = np.array([40.0, 35.0, 30.0, 45.0, 20.0])
T = np.array([12.0, 15.0, 5.0, 20.0, 25.0])
P = np.array([0.0, 100.0, 500.0, 10.0, 50.0])

LOCATIONS = [
    (8, 54),  # North Sea
    (6, 43),  # Mediterranean Sea
    (-65, 19),  # Caribbean Sea
    (-70, 54),  # Labrador Sea
    (150, -30),  # Tasman Sea
]


def reference_SA(C, t, P, lon, lat):
    gsw = pytest.importorskip("gsw")
    SP = gsw.SP_from_C(C, t, P)
    return gsw.SA_from_SP(SP, P, lon, lat)


def reference_CT(C, t, P, lon, lat):
    gsw = pytest.importorskip("gsw")
    SA = reference_SA(C, t, P, lon, lat)
    return gsw.CT_from_t(SA, t, P)


def reference_rho(C, t, P, lon, lat):
    gsw = pytest.importorskip("gsw")
    SA = reference_SA(C, t, P, lon, lat)
    CT = reference_CT(C, t, P, lon, lat)
    return gsw.rho(SA, CT, P)


def reference_pot_rho(C, t, P, lon, lat):
    gsw = pytest.importorskip("gsw")
    SA = reference_SA(C, t, P, lon, lat)
    return gsw.pot_rho_t_exact(SA, t, P, 0)


@pytest.mark.parametrize("lon,lat", LOCATIONS)
class TestAgainstReferenceGSW:
    def test_SA(self, lon, lat):
        LON, LAT = np.full(C.shape, lon), np.full(C.shape, lat)
        expected = reference_SA(C, T, P, LON, LAT)
        result = fast_gsw.SA(C, T, P, LON, LAT)
        np.testing.assert_allclose(result, expected, rtol=1e-4)

    def test_CT(self, lon, lat):
        LON, LAT = np.full(C.shape, lon), np.full(C.shape, lat)
        expected = reference_CT(C, T, P, LON, LAT)
        result = fast_gsw.CT(C, T, P, LON, LAT)
        np.testing.assert_allclose(result, expected, rtol=1e-4)

    def test_rho(self, lon, lat):
        LON, LAT = np.full(C.shape, lon), np.full(C.shape, lat)
        expected = reference_rho(C, T, P, LON, LAT)
        result = fast_gsw.rho(C, T, P, LON, LAT)
        np.testing.assert_allclose(result, expected, rtol=1e-4)

    def test_pot_rho(self, lon, lat):
        LON, LAT = np.full(C.shape, lon), np.full(C.shape, lat)
        expected = reference_pot_rho(C, T, P, LON, LAT)
        result = fast_gsw.pot_rho(C, T, P, LON, LAT)
        np.testing.assert_allclose(result, expected, rtol=1e-4)


class TestInputHandling:
    LON = np.full(C.shape, -30.0)
    LAT = np.full(C.shape, -30.0)

    def test_list_input_matches_array_input(self):
        array_result = fast_gsw.rho(C, T, P, self.LON, self.LAT)
        list_result = fast_gsw.rho(
            list(C), list(T), list(P), list(self.LON), list(self.LAT)
        )
        np.testing.assert_allclose(list_result, array_result)

    def test_integer_dtype_input_is_cast_to_float(self):
        C_int = np.array([40, 35, 30, 45, 20])
        result = fast_gsw.rho(C_int, T, P, self.LON, self.LAT)
        expected = fast_gsw.rho(C_int.astype(float), T, P, self.LON, self.LAT)
        np.testing.assert_allclose(result, expected)

    def test_scalar_lon_lat_broadcast_against_vector(self):
        # lon/lat given as scalars should broadcast across the vector inputs.
        result = fast_gsw.rho(C, T, P, -30.0, -30.0)
        expected = fast_gsw.rho(C, T, P, self.LON, self.LAT)
        np.testing.assert_allclose(result, expected)

    def test_single_element_array_returns_single_value(self):
        result = fast_gsw.rho(C[:1], T[:1], P[:1], self.LON[:1], self.LAT[:1])
        assert result.shape == (1,)

    def test_mismatched_lengths_raise_value_error(self):
        with pytest.raises(ValueError):
            fast_gsw.rho([40.0, 41.0, 42.0], [12.0, 12.0], 0.0, -30.0, -30.0)


class TestCaller:
    """Unit tests for the helper class fast_gsw.Caller used internally."""

    def setup_method(self):
        self.caller = Caller()

    @pytest.mark.parametrize(
        "value,expected",
        [
            (5.0, False),
            ("abc", True),  # strings are iterable, even though likely unintended
            ([1, 2, 3], True),
            (np.array([1, 2, 3]), True),
            (np.float64(1.0), False),
        ],
    )
    def test_is_iterable(self, value, expected):
        assert self.caller.is_iterable(value) is expected

    def test_cast_arguments_broadcasts_scalars(self):
        n, (c, t, p, lon, lat) = self.caller.cast_arguments(
            [40.0, 41.0], 12.0, 0.0, -30.0, -30.0
        )
        assert n == 2
        np.testing.assert_array_equal(t, [12.0, 12.0])
        np.testing.assert_array_equal(lat, [-30.0, -30.0])

    def test_cast_arguments_rejects_unequal_length_vectors(self):
        with pytest.raises(ValueError, match="equally long"):
            self.caller.cast_arguments([1.0, 2.0], [1.0, 2.0, 3.0], 0.0, 0.0, 0.0)

    def test_cast_arguments_all_scalars_raises_index_error(self):
        # Known bug: when every argument is a scalar, cast_arguments never
        # discovers a vector length and indexes into an empty list.
        with pytest.raises(IndexError):
            self.caller.cast_arguments(40.0, 12.0, 0.0, -30.0, -30.0)
