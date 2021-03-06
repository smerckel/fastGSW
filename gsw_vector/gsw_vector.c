#include "gsw_vector.h"
#include <stdio.h>
#include <stdlib.h>


void gsw_vector_rho(double *C,
		    double *t,
		    double *P,
		    double *lon,
		    double *lat,
		    unsigned int size,
		    double *rho)
{
  unsigned int i;
  double SA,SP;

  for(i=0;i<size;++i){
    SP=gsw_sp_from_c(C[i],t[i],P[i]);
    SA=gsw_sa_from_sp(SP,P[i],lon[i],lat[i]);
    rho[i]=gsw_rho_t_exact(SA,t[i],P[i]);
  }
}


void gsw_vector_pot_rho(double *C,
			double *t,
			double *P,
			double *lon,
			double *lat,
			unsigned int size,
			double *rho)
{
  unsigned int i;
  double SA,SP;
  
  for(i=0;i<size;++i){
    SP=gsw_sp_from_c(C[i],t[i],P[i]);
    SA=gsw_sa_from_sp(SP,P[i],lon[i],lat[i]);
    rho[i]=gsw_pot_rho_t_exact(SA,t[i],P[i], 0.);
  }
}


void gsw_vector_SA(double *C,
		    double *t,
		    double *P,
		    double *lon,
		    double *lat,
		    unsigned int size,
		    double *SA)
{
  unsigned int i;
  double SP;
  
  for(i=0;i<size;++i){
    SP=gsw_sp_from_c(C[i],t[i],P[i]);
    SA[i]=gsw_sa_from_sp(SP,P[i],lon[i],lat[i]);
  }
}

void gsw_vector_CT(double *C,
		    double *t,
		    double *P,
		    double *lon,
		    double *lat,
		    unsigned int size,
		    double *CT)
{
  unsigned int i;
  double SP,SA;
  
  for(i=0;i<size;++i){
    SP=gsw_sp_from_c(C[i],t[i],P[i]);
    SA=gsw_sa_from_sp(SP,P[i],lon[i],lat[i]);
    CT[i]=gsw_ct_from_t(SA,t[i],P[i]);
  }
}

