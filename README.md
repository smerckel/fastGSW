# fast_gsw

A ctypes-based Python interface for fast, vectorized execution of a few
[TEOS-10 GSW](http://www.teos-10.org/) (Gibbs SeaWater) oceanographic
functions, intended for processing large arrays of CTD
(conductivity/temperature/pressure) data, such as from ocean gliders.

Currently implemented:

- `rho(C, t, P, lon, lat)` — in-situ density
- `pot_rho(C, t, P, lon, lat)` — potential density (reference pressure 0 dbar)
- `SA(C, t, P, lon, lat)` — absolute salinity
- `CT(C, t, P, lon, lat)` — conservative temperature

All inputs/outputs are plain numpy arrays (scalars are broadcast); units are
conductivity in mS/cm, temperature in °C, pressure in dbar, and longitude /
latitude in decimal degrees.

## Why

The pure-Python [`gsw`](https://pypi.org/project/gsw/) package computes
in-situ density (and similar derived quantities) as a chain of several
composed Python function calls per array (e.g.
`SP_from_C -> SA_from_SP -> rho_t_exact`). For large arrays of CTD triplets,
`fast_gsw` collapses that whole pipeline into a single C function call by
vendoring and compiling the TEOS-10 C implementation and calling it via
`ctypes`, which removes the Python-level per-step call overhead.

## Install

```
pip install fast_gsw
```

This compiles the vendored TEOS-10 C sources at install time, so a C
compiler (gcc/clang) must be available. No other manual steps, root access,
or system-wide library installation are required.

To install from a local checkout:

```
pip install .
```

## License

`fast_gsw` itself is licensed under the GPLv3 (see `LICENSE`). It vendors and
compiles source code from the [TEOS-10 GSW-C](https://github.com/TEOS-10/GSW-C)
Oceanographic Toolbox, C version 3.06.16, under the license in
`src/fast_gsw/_csrc/LICENSE`.
