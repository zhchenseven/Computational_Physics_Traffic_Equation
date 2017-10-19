# ifndef _EVO_DYNAM
# define _EVO_DYNAM

# include <iostream>
# include <armadillo>
# include "IBC.h"

using namespace std;
using namespace arma;


class Evo_dynam :public IBC
{
public:
	double txr;
	Evo_dynam(double txrr=0);
	void evo_exe_cetr(void);

	void evo_DN(Evo_dynam *pEd, double (Evo_dynam::*p_F)(double,double));
	double  F_Rm(double rho_L, double rho_R);
	double  F_LW(double rho_L, double rho_R);
	double  F_Roe(double rho_L, double rho_R);
	double  F_REF(double rho_L, double rho_R);
	double  f(double rho);

	typedef double(Evo_dynam::*p_F)(double, double);
	p_F retn_F_func(void);



	double a(double rho);
	double retn_dt(rowvec & rho);



	rowvec get_exact_sol(double t_point);

	void store_data(void);

};

# endif
