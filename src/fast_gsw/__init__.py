import ctypes
import glob
import os

import numpy as np

_pkg_dir = os.path.dirname(os.path.abspath(__file__))
_candidates = glob.glob(os.path.join(_pkg_dir, "libgsw_vector*"))
if not _candidates:
    raise ImportError(
        "Could not locate the compiled libgsw_vector shared library inside "
        f"the fast_gsw package directory ({_pkg_dir}); was fast_gsw installed "
        "correctly (pip install .)?"
    )
libgsw=ctypes.CDLL(_candidates[0])

## return and argument declarations.
libgsw.gsw_vector_rho.restype=ctypes.c_void_p
libgsw.gsw_vector_rho.argtypes=(ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.c_uint,
                                ctypes.POINTER(ctypes.c_double))

libgsw.gsw_vector_pot_rho.restype=ctypes.c_void_p
libgsw.gsw_vector_pot_rho.argtypes=(ctypes.POINTER(ctypes.c_double),
                                    ctypes.POINTER(ctypes.c_double),
                                    ctypes.POINTER(ctypes.c_double),
                                    ctypes.POINTER(ctypes.c_double),
                                    ctypes.POINTER(ctypes.c_double),
                                    ctypes.c_uint,
                                    ctypes.POINTER(ctypes.c_double))


libgsw.gsw_vector_SA.restype=ctypes.c_void_p
libgsw.gsw_vector_SA.argtypes=(ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.c_uint,
                                ctypes.POINTER(ctypes.c_double))

libgsw.gsw_vector_CT.restype=ctypes.c_void_p
libgsw.gsw_vector_CT.argtypes=(ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.POINTER(ctypes.c_double),
                                ctypes.c_uint,
                                ctypes.POINTER(ctypes.c_double))

class Caller(object):

    def __call__(self,libgsw_vector_fun,C,t,P,lon,lat):
        return self.call_function(libgsw_vector_fun,C,t,P,lon,lat)
    
    def is_iterable(self,x):
        ''' see if a parameter is iterable '''
        try:
            (_x for _x in x)
            return True
        except TypeError:
            return False

    def cast_arguments(self,*p):
        ''' casts all arguments into double arrays.

        Not intended to be called directly.
        '''
        pm=[]
        plist=[self.is_iterable(_p) for _p in p]
        s=[len(_p) for _p,_pl in zip(p,plist) if _pl]
        if not all([_s==s[0] for _s in s]):
            raise ValueError("Not all vectors are equally long.")
        for i,(_p,_pl) in enumerate(zip(p,plist)):
            if not _pl:
                pm.append(np.array([_p]*s[0]).astype(float))
            else:
                try:
                    if _p.dtype!=np.float64:
                        pm.append(_p.astype('float'))
                    else:
                        pm.append(_p)
                except AttributeError:
                    pm.append(np.array(_p).astype('float'))
        return s[0],pm

    def call_function(self,libgsw_vector_fun,C,t,P,lon,lat):
        n,(C,t,P,lon,lat)=self.cast_arguments(C,t,P,lon,lat)
        x=np.zeros(n,float)
        libgsw_vector_fun(C.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                          t.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                          P.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                          lon.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                          lat.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                          n,
                          x.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
        return x

__caller=Caller()
    
def rho(C,t,P,lon,lat):
    '''
    Calculates in situ density of seawater from conductivity, in-situ temperature and pressure,
    and lat/lon.

    C conductivity: mS/cm
    t in-situ temperature: deg C
    P pressure: dbar

    lon longitude: decimal degrees
    lat latitude: decimal degrees

    '''
    return __caller(libgsw.gsw_vector_rho,C,t,P,lon,lat)


def pot_rho(C,t,P,lon,lat):
    '''
    Calculates in potential density of seawater from conductivity, in-situ temperature and pressure,
    and lat/lon.

    C conductivity: mS/cm
    t in-situ temperature: deg C
    P pressure: dbar

    lon longitude: decimal degrees
    lat latitude: decimal degrees

    '''
    return __caller(libgsw.gsw_vector_pot_rho,C,t,P,lon,lat)


def CT(C,t,P,lon,lat):
    '''
    Calculates in conservative temperature from conductivity, in-situ temperature,pressure,
    and lat/lon.

    C conductivity: mS/cm
    t in-situ temperature: deg C
    P pressure: dbar

    lon longitude: decimal degrees
    lat latitude: decimal degrees

    '''
    return __caller(libgsw.gsw_vector_CT,C,t,P,lon,lat)

def SA(C,t,P,lon,lat):
    ''' returns absolute salinity

    C conductivity: mS/cm
    t in-situ temperature: deg C
    P pressure: dbar

    lon longitude: decimal degrees
    lat latitude: decimal degrees

    '''
    return __caller(libgsw.gsw_vector_SA,C,t,P,lon,lat)


