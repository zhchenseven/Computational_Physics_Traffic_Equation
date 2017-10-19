# include <iostream>
# include <armadillo>

# include "IBC.h"

using namespace std;
using namespace arma;

IBC::IBC(string ini_typee , string bnd_typee , string flux_typee, string exa_typee)
{
	ini_type = ini_typee;
	bnd_type = bnd_typee;
	flux_type = flux_typee;
	exa_type = exa_typee;
	Para();
	cout << "A class of IBC is constructed." << endl << endl;
}



void IBC::set_IBC(string ini_typee, string bnd_typee)
{
	ini_type = ini_typee;
	bnd_type = bnd_typee;
}

void IBC::set_flux(string flux_typee)
{
	flux_type = flux_typee;
}

void IBC::IBC_cetr(void)
{
	if (ini_type == "TL")
	{
		Para * pP = (Para *)this;
		IB_traffic_light I;
		I.eva_IB(pP);
	}
	else if (ini_type == "TL_di")
	{
		
			Para * pP = (Para *)this;
			IB_traffic_light_di I;
			I.eva_IB(pP);
		
	}
	else
		
	{
		cout << "Your specified initial condition type " << ini_type << " is not available yet." << endl;
		exit(1);
	}
}

void IBC::set_exa_type(string exa_typee)
{
	exa_type = exa_typee;
}


IB_traffic_light::IB_traffic_light()
{
	cout << "A class of trafic light initial condition is constructed." << endl << endl;
}

void IB_traffic_light::eva_IB(Para * pP)
{
	uvec ind_neg = find(pP->x<= 0 && pP->x >=-1000);
	pP->uo= rowvec(pP->N, fill::zeros);
	pP->uo(ind_neg)= pP->rhom*rowvec(ind_neg.n_elem, fill::ones);
	pP->ui = pP->uo;
	pP->un = rowvec(pP->N, fill::zeros);
	pP->u_track = mat(pP->N_itr, pP->N,fill::zeros);
	pP->u_exact= mat(pP->N_itr, pP->N,fill::zeros);
	pP->ind_track = uvec(pP->N_itr, fill::zeros);
	pP->t_out= rowvec(pP->N_itr+1, fill::zeros);
	pP->t_evo = rowvec(pP->N_itr, fill::zeros);
}


IB_traffic_light_di::IB_traffic_light_di()
{
	cout << "A class of trafic light initial condition when the discontinuity in the interior is constructed." << endl << endl;
}

void IB_traffic_light_di::eva_IB(Para * pP)
{
	uvec ind_neg = find(pP->x <= 0 && pP->x >= -1000);
	pP->uo = rowvec(pP->N, fill::zeros);
	pP->uo(ind_neg) = pP->rhom*rowvec(ind_neg.n_elem, fill::ones);
	pP->uo(ind_neg(ind_neg.n_elem - 1) + 1) = pP->rhom/2;
	pP->ui = pP->uo;
	pP->un = rowvec(pP->N, fill::zeros);
	pP->u_track = mat(pP->N_itr, pP->N, fill::zeros);
	pP->u_exact = mat(pP->N_itr, pP->N, fill::zeros);
	pP->ind_track = uvec(pP->N_itr, fill::zeros);
	pP->t_out = rowvec(pP->N_itr + 1, fill::zeros);
	pP->t_evo = rowvec(pP->N_itr, fill::zeros);
}




