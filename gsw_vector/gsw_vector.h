#ifndef GSW_VECTOR_H
#define GSW_VECTOR_H

#include <stdlib.h>
#include "gswteos-10.h"

void gsw_vector_rho(double *C,
		    double *t,
		    double *P,
		    double *lat,
		    double *lon,
		    unsigned int size,
		    double *rho);

void gsw_vector_SA(double *C,
		   double *t,
		   double *P,
		   double *lat,
		   double *lon,
		   unsigned int size,
		   double *SA);

void gsw_vector_CT(double *C,
		   double *t,
		   double *P,
		   double *lat,
		   double *lon,
		   unsigned int size,
		   double *CT);

#endif
