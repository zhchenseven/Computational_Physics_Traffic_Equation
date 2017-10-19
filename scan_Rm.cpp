# include <iostream>
# include <armadillo>

# include "Data_process.h"

using namespace std;
using namespace arma;

//int main(int argv, char ** argc)
int scan_Rm(int argv, char ** argc)
{
	Data_process Project;
	rowvec safe_fac_arr(3, fill::zeros);
	rowvec T_arr(3, fill::zeros);
	safe_fac_arr << 0.9 << 0.6 << 0.3 << endr;
	T_arr << 60 << 40 << 20<<endr;
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
	string flux_type = "Rm";
	Project.set_flux(flux_type);
	string main_fd_name = "scan_F_Rm";
	string vis_name = "Rm_T_20_sf_0p9";
	int index = 0;
	string data_type = "dat";
	string size_sufx = "size";
	Project.set_process_ctrl(vis_name, index, data_type, size_sufx);
	Project.set_main_fd(main_fd_name);
	int i, j;
	for (i = 0; i < safe_fac_arr.n_elem; i++)
	{
		Project.safe_fac = safe_fac_arr(i);
		for (j = 0; j < T_arr.n_elem; j++)
		{	
			Project.creat_main_fd_ctrl = 1;
			Project.T = T_arr(j);
			vis_name = flux_type+ "_sf_" + Project.dn2s(safe_fac_arr(i)) + "_T_" + Project.dn2s(T_arr(j)) ;
			cout << "vis_name is " << Project.vis_name << endl;
			Project.set_vis_name(vis_name);
			if (i != 0 || j != 0)
				Project.creat_main_fd_ctrl = 0;
			Project.exe_cetr();
			Project.process();
			Project.write_log();

		}
	}



	system("pause");
	return 0;
}