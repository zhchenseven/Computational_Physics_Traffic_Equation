# include <iostream>
# include <armadillo>

# include "Evo_dynam.h"

using namespace std;
using namespace arma;

enum F_type_code
{
	Rm,
	LW,
	Roe,
	REF

};


F_type_code hash_F_type(string const & s)
{
	if (s == "Rm")
		return Rm;
	if (s == "LW")
		return LW;
	if (s == "Roe")
		return Roe;
	if (s == "REF")
		return REF;
	else
	{
		cout << "Your specified flux type " << s << " is not available yet." << endl;
		exit(1);
	}
}



Evo_dynam::Evo_dynam(double txrr )
{
	txr = txrr;
	IBC();
	cout << "A class of Evo_dynam is constructed." << endl << endl;
}


void Evo_dynam::evo_exe_cetr(void)
{
	p_F pF = retn_F_func();
	//cout << "nu=" << nu << ",dx=" << dx << ",dt=" << dt << endl;
	//qnu = (this->*pq)(nu)*dx/(2*dt);
	if (bnd_type == "DN" )
		evo_DN(this,pF);
	else
	{
		cout << "Your specified flux type " << flux_type << " and boundary condition "<<bnd_type<<  " is not available yet." << endl;
		exit(1);
	}
}



typedef double(Evo_dynam::*p_F)(double,double);
p_F Evo_dynam::retn_F_func(void)
{
	switch (hash_F_type(flux_type))
	{
	case Rm:
	{
		p_F p = &Evo_dynam::F_Rm;
		return p;
	}

	case LW:
	{
		p_F p = &Evo_dynam::F_LW;
		return p;
	}

	case Roe:
	{
		p_F p = &Evo_dynam::F_Roe;
		return p;
	}

	case REF:
	{
		p_F p = &Evo_dynam::F_REF;
		return p;
	}

	default:
	{
		cout << "Your specified flux type " << flux_type << " is not available yet." << endl;
		exit(1);
		break;
		break;
	}
	}
}


void Evo_dynam::evo_DN(Evo_dynam *pEd, double (Evo_dynam::*p_F)(double, double))
{
	int n, j;
	int n_flag = 1;
	double Fj1, Fj2;
	double t_elasped;
	double txr=0;
	wall_clock timer;
	t_out(0) = 0;
	u_track.row(0) = uo;
	u_exact.row(0) = uo;
	M = 0;
	cout << "M= " << M << ",M_fac= " <<", N_itr= " << N_itr << endl ;
	timer.tic();
	for (n = 0; n < N_itr; n++)
	{
		dt = retn_dt(uo);
		//if (dt < 0.01)
		//	dt = 0.01;
		txr = dt / dx;
		
		for (j = 0; j < N; j++)
		{
			if (j == 0)
			{
				// the left most flow is given by its zero
				//Fj1 = (this->*p_F)(0, uo(j));
				Fj1 = 0;
				Fj2 = (this->*p_F)(uo(j), uo(j + 1));
				un(j) = uo(j) - txr*(Fj2 - Fj1);
				// old and wrong flow
				//un(j) = 0;
			}
			else if (j<N-1)
			{
				Fj1 = (this->*p_F)(uo(j-1),uo(j));
				Fj2 = (this->*p_F)(uo(j), uo(j+1));
				un(j) = uo(j) - txr*(Fj2 - Fj1);
			}
			else
			{
				Fj1 = (this->*p_F)(uo(j - 1), uo(j));
				// the rightmost flow is given by its right end point
				Fj2 = f(uo(N - 1));
				un(j) = uo(j) - txr*(Fj2 - Fj1);
			}

		}
		//un(N-1) = f(uo(N-2));

		uo = un;
		//cout << un << endl;
		if (n == 0)
			t_evo(n) = dt;
		else
			t_evo(n) = t_evo(n - 1) + dt;
		cout << "n= " << n << endl;
		//cout<< "tn=" << t_evo(n) << endl;
		//cout << "un=" << un << endl;
		t_out(n + 1) = t_evo(n);
		u_track.row(n+1) = un;
		u_exact.row(n+1)= get_exact_sol(t_evo(n));
		//cout << "t_evo(n)= " << t_evo(n) << endl;
		if (t_evo(n) > T)
			break;
	}
	uf_exact = u_exact.row(n);
	//cout << "uf_exact" << endl << uf_exact << endl << "uf" << endl << un << endl;
	// here, M points including the initial point plus the iterations
	M = n+2;
	store_data();
	t_elasped = timer.toc();
	cout << "The F1 dirichlet and neumann condition takes " << t_elasped << " s in C++." << endl;
}


inline double  Evo_dynam::f(double rho)
{
	return  rho*vm*(1 - rho / rhom);
}

void Evo_dynam::store_data(void)
{
	mat u_exact_tmp = mat(M, N, fill::zeros);
	mat u_track_tmp= mat(M, N, fill::zeros);
	rowvec t_out_tmp = rowvec(M, fill::zeros);
	int i;
	u_exact_tmp = u_exact(span(0, M - 1), span(0, N - 1));
	u_track_tmp=u_track(span(0, M - 1), span(0, N - 1));
	t_out_tmp = t_out(span(0, M - 1));
	u_exact = u_exact_tmp;
	u_track = u_track_tmp;
	t_out = t_out_tmp;
	cout << "t_out" << endl << t_out << endl;
}



rowvec Evo_dynam::get_exact_sol(double t_point)
{
	int i, pi;
	double x_point = 0;
	double aR = a(0);
	double aL = a(rhom);
	rowvec un_exact = rowvec(N, fill::zeros);
	for (i = 0; i < N; i++)
	{
		x_point = x(i);
		if (x_point / t_point < aL)
			un_exact(i) = rhom;
		else if (x_point / t_point > aR)
			un_exact(i) = 0;
		else
			un_exact(i) = rhom / 2 * (1 - x_point / (vm*t_point));
		if (exa_type == "part_Riemann")
		{
			double x_r = vm*t_point;
			double x_l = x_r - sqrt(400 * vm*t_point / rhom);
			int ind_part = 0;
			if (t_point > 1000 / vm)
				ind_part = (x_point <= x_r && x_point >= x_l);
			else
				ind_part = (x_point >= -1000);
			un_exact(i) *= ind_part;
		}
	}
	return un_exact;
}

double  Evo_dynam::F_Rm(double rho_L, double rho_R)
{
	double aL = a(rho_L);
	double aR = a(rho_R);
	if (aL <= 0 && aR >= 0)
		return rhom*vm / 4;
	else if (aL + aR >= 0)
		return f(rho_L);
	else
		return f(rho_R);
}

double  Evo_dynam::F_LW(double rho_L, double rho_R)
{
	double e;
	e = (rho_R + rho_L) / 2.0 - txr / 2.0*(f(rho_R) - f(rho_L));
	return f(e);
}

double  Evo_dynam::F_Roe(double rho_L, double rho_R)
{
	double aL = a(rho_L);
	double aR = a(rho_R);
	if (aR + aL >= 0)
		return f(rho_L);
	else
		return f(rho_R);
}

double  Evo_dynam::F_REF(double rho_L, double rho_R)
{
	double aL = a(rho_L);
	double aR = a(rho_R);
	if (aL <= 0 && aR >= 0)
		return (f(rho_L) + f(rho_R) - (aR - aL)*(rho_R - rho_L)/2.0) / 2.0;
	else if (aL + aR >= 0)
		return f(rho_L);
	else
		return f(rho_R);
}


inline double Evo_dynam::a(double rho)
{
	return vm*(1 - 2 * rho / rhom);
}

double Evo_dynam::retn_dt(rowvec & rho)
{
	rowvec a_rho = vm*(1 - 2 * rho / rhom);
	double a_max = arma::abs(a_rho).max();
	return dx / a_max*safe_fac;
}

