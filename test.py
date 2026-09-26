import numpy as np
import fast_gsw
import gsw
import profile

N=1000000
C=np.array([40.]*N)
t=np.array([12.]*N)
P=np.array([0.]*N)

lat=np.array([54.]*N)
lon=np.array([8.]*N)


def get_rho(C,t,P,lat,lon):
    SP=gsw.SP_from_C(C,t,P)
    SA=gsw.SA_from_SP(SP,P,lat,lon)
    rho2=gsw.rho_t_exact(SA,t,P)
    return rho2

profile.run("rho=fast_gsw.rho(C,t,P,lat,lon)")

#profile.run("rho2=get_rho(C,t,P,lat,lon)")
