# ifndef _IBC
# define _IBC

# include <iostream>
# include <armadillo>
# include "Para.h"

using namespace std;
using namespace arma;

class IBC :public Para
{
public:
	// ini_type is the type of the initial conditions
	string ini_type;
	// bnd_type is the type of boundary conditions
	string bnd_type;
	// flux_type determines the type of flux
	string flux_type;

	string exa_type;

	IBC(string ini_typee = "", string bnd_typee = "",string flux_typee = "",string exa_typee="full_Riemann");

	void set_IBC(string ini_typee, string bnd_typee);
	void set_flux(string flux_typee);
	void IBC_cetr(void);
	void set_exa_type(string exa_typee);
};



class IB_traffic_light
{
public:
	IB_traffic_light();
	void eva_IB(Para * pP);
};

class IB_traffic_light_di
{
public:
	IB_traffic_light_di();
	void eva_IB(Para * pP);
};


# endif
