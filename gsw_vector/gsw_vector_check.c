#include <stdio.h>
#include "gsw_vector.h"


int main()
{
  double C[1],t[1],P[1],lat[1],lon[1],rho[1],SA[1];

  C[0]=26.;
  t[0]=5.;
  P[0]=1.;
  lat[0]=71.2;
  lon[0]=-126;
   
  gsw_vector_rho(C,t,P,lon,lat,1,rho);
  gsw_vector_SA(C,t,P,lon,lat,1,SA);

  printf("rho: %12.6f\n",rho[0]);
  printf("SA:  %12.6f\n",SA[0]);
  return 0;
}
