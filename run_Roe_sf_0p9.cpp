# include <iostream>
# include <armadillo>

# include "Data_process.h"

using namespace std;
using namespace arma;

//int main(int argv, char ** argc)
int Roe(int argv, char ** argc)
{
	Data_process Project;
	int N = 32;
	double x_low = -2000;
	double x_sup = 4000;
	double dx = 50;
	double rhom = 0.1;
	double vm = 50;
	double T = 60;
	double safe_fac = 0.9;
	int M = 1000;
	Project.set_para(x_low, x_sup, dx, T,  vm,  rhom,safe_fac);
	string ini_type = "TL";
	string bnd_type = "DN";
	Project.set_IBC(ini_type, bnd_type);
	string flux_type = "Roe";
	Project.set_flux(flux_type);

	string vis_name = "Roe_T_20_sf_0p9";
	int index = 0;
	string data_type = "dat";
	string size_sufx = "size";
	Project.set_process_ctrl(vis_name, index, data_type, size_sufx);

	Project.exe_cetr();
	Project.process();
	Project.write_log();

	system("pause");
	return 0;
}