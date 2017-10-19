#ifndef _PARA
# define _PARA

# include <iostream>
# include <armadillo>

using namespace std;
using namespace arma;

class Para
{
public:
	//N is the number of actual iterations
	int N;
	//x_low is the lower limit of x
	double x_low;
	// x_sup is the upper limit of x
	double x_sup;
	//M controls the number of tracking time, which includes the initial time and the final time, we demand M>2
	int M;
	// T specifies the final time point
	double T;
	// nu is the CFL number 
	double nu;

	// uo is the wavefunction at initial time
	rowvec uo;

	// un 
	rowvec un;

	// dt is the time spacing
	double dx;
	// dx is the spacing
	double dt;
	// x is the range of interest
	rowvec x;

	// u_track is the matrix to record data
	mat u_track;

	// ind_track specifies the index to  record data
	uvec ind_track;

	// N_itr is the number of maximal iterations to undergo
	int N_itr;




	// u_exact is the exact solution of the wave equation corresponding to the recording time
	mat u_exact;

	// ui records the initial wave packet for the later exact solutions
	rowvec ui;

	// uf_exact indicates the exact solution of the final time point
	rowvec uf_exact;

	// t_out is the output time points
	rowvec t_out;

	// err is the error of L1 error
	double err;

	// vm is the maximal velocity
	double vm;

	// rho is the maximal density
	double rhom;

	// safe_fac is the safe factor
	double safe_fac;

	// t_evo is the recording of each time step;
	rowvec t_evo;


	Para(int NN = 0, double x_loww = 0, double x_supp = 0, int MM = 50, double TT = 1, double nuu = 1, rowvec uoo = rowvec(), rowvec unn = rowvec(),
		double dxx = 0, double dtt = 0, rowvec xx = rowvec(), mat u_trackk = mat(), uvec ind_trackk = uvec(), int N_itrr = 0,mat u_exactt = mat(), rowvec uii = rowvec(),
		rowvec uf_exactt = rowvec(), rowvec t_outt = rowvec(), double errr = 0, double vmm = 0, double rhomm = 0, double safe_facc =0,rowvec t_evoo= rowvec());

	void set_para( double x_loww, double x_supp,double dxx,  double TT,double vmm, double rhomm,double safe_facc);

	
};

# endif
