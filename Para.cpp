# include <iostream>
# include <armadillo>
# include "Para.h"


using namespace std;
using namespace arma;

Para::Para(int NN, double x_loww, double x_supp, int MM , double TT, double nuu , rowvec uoo , rowvec unn ,double dxx, double dtt ,
	rowvec xx , mat u_trackk , uvec ind_trackk , int N_itrr,   mat u_exactt , rowvec uii ,
	rowvec uf_exactt , rowvec t_outt, double errr , double vmm , double rhomm, double safe_facc,rowvec t_evoo )
{
	N = NN;
	x_low = x_loww;
	x_sup = x_supp;
	M = MM;
	T = TT;
	nu = nuu;
	uo = uoo;
	un = unn;
	dx = dxx;
	dt = dtt;
	x = xx;
	u_track = u_trackk;
	ind_trackk = ind_track;
	N_itr = N_itrr;
	u_exact = u_exactt;
	ui = uii;
	uf_exact = uf_exactt;
	t_out = t_outt;
	err = errr;
	vm = vmm;
	rhom = rhomm;
	safe_fac = safe_facc;
	t_evo = t_evoo;
	cout << "A class of Para is constructed." << endl << endl;
}


void Para::set_para(double x_loww, double x_supp, double dxx,  double TT, double vmm, double rhomm,double safe_facc)
{
	x_low = x_loww;
	x_sup = x_supp;
	T = TT;
	dx = dxx;
	x = regspace<rowvec>(x_low,dx,x_sup);
	N = x.n_elem;
	uo = rowvec(N, fill::zeros);
	un = rowvec(N, fill::zeros);
	N_itr = 200000;
	vm = vmm;
	rhom = rhomm;
	t_evo = rowvec(N_itr, fill::zeros);
	safe_fac = safe_facc;
}

