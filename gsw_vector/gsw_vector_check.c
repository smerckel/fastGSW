#include <stdio.h>
#include "gsw_vector.h"


int main()
{
  double C[1],t[1],P[1],lat[1],lon[1],rho[1],SA[1];

  C[0]=26.;
  t[0]=5.;
  P[0]=1.;
  // these coordinates work
  lat[0]=71.2;
  lon[0]=-126;
  // but what about these?
  lat[0]=42.89869899379396;
  lon[0]=5.135901098949273;


  double SP0=gsw_sp_from_c(C[0],t[0],P[0]);
  printf("SP0:  %12.6f\n",S0);
  double SA0=gsw_sa_from_sp(SP0,P[0],lon[0],lat[0]);
  printf("SA0:  %12.6f\n",SA0);
  double rho0=gsw_rho_t_exact(SA0,t[0],P[0]);
  printf("rho0: %12.6f\n",rho0);
  

  
  gsw_vector_rho(C,t,P,lon,lat,1,rho);
  gsw_vector_SA(C,t,P,lon,lat,1,SA);

  printf("rho: %12.6f\n",rho[0]);
  printf("SA:  %12.6f\n",SA[0]);
  return 0;
}
