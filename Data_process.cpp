# include <iostream>
# include <armadillo>
# include <direct.h>
# include "Data_process.h"

using namespace std;
using namespace arma;


template <typename T>
string n2s(T Number)
{
	stringstream ss;
	ss << Number;
	return ss.str();
}

Data_process::Data_process(string vis_namee, int indexx, string fd_namee, string data_typee, string size_sufxx,  string main_fd_namee,int creat_main_fd_ctrll)
{
	vis_name = vis_namee;
	index = indexx;
	fd_name = fd_namee;
	data_type = data_typee;
	size_sufx = size_sufxx;
	main_fd_name = main_fd_namee;
	creat_main_fd_ctrl = creat_main_fd_ctrll;
	Evo_dynam();
	cout << "A class of Data_process is constructed." << endl << endl;
}

void Data_process::set_process_ctrl(string vis_namee, int indexx, string data_typee, string size_sufxx)
{
	vis_name = vis_namee;
	index = indexx;
	fd_name = vis_name + "_" + n2s(index);

	data_type = data_typee;
	size_sufx = size_sufxx;
}

void Data_process::exe_cetr()
{
	IBC_cetr();
	evo_exe_cetr();
}

void Data_process::create_folder(void) const
{
	if (creat_main_fd_ctrl == 1)
	{
		string ss = main_fd_name + "_" + n2s(index);
		const char * s0 = ss.c_str();
		_mkdir(s0);
	}
	const char * s = fd_name.c_str();
	/*windows use _mkdir(s); and linux use int result = mkdir(s, 0777);*/
	_mkdir(s);
	//int result = mkdir(s, 0777);

}


string Data_process::get_save_path(string name) const
{
	string path;
	path = fd_name + "/" + name;

	return path;
}


void Data_process::save_data_univ(rowvec & f, string name)
{
	name = "R1_" + name;
	name = get_save_name_univ(name);
	f.save(name, raw_binary);
}

void Data_process::save_data_univ(mat & f, string name)
{
	name = "R2_" + name;
	name = get_save_name_univ(name);
	f.save(name, raw_binary);
}


void Data_process::save_data_univ(uvec & f, string name)
{
	rowvec ff(f.n_elem);
	int i;
	for (i = 0; i < f.n_elem; i++)
		ff(i) = f(i);
	save_data_univ(ff, name);
}

string Data_process::get_save_name_univ(string name)
{

	return get_save_path(get_save_name(name, data_type));

}


string Data_process::get_save_name(string name, string data_typee)
{
	name = name + "." + data_typee;

	return name;
}

void Data_process::save_data_and_size(rowvec & f, string name)
{
	save_data_univ(f, name);
	rowvec size(1);
	size(0) = f.n_elem;
	save_data_size(name, size_sufx, size);
}


void Data_process::save_data_and_size(mat & f, string name)
{
	save_data_univ(f, name);
	rowvec size(2);
	size(0) = f.n_rows; size(1) = f.n_cols;
	save_data_size(name, size_sufx, size);
}



void Data_process::save_data_and_size(uvec & f, string name)
{
	save_data_univ(f, name);
	rowvec size(1);
	size(0) = f.n_elem;
	save_data_size(name, size_sufx, size);
}

void Data_process::save_data_size(string name, string sufx, rowvec size)
{
	name = name + '_' + sufx;
	save_data_univ(size, name);

}


void Data_process::process()
{
	create_folder();
	save_info();
	eva_err();
}

void Data_process::save_info(void)
{
	save_data_and_size(x, "x");
	save_data_and_size(ui, "ui");
	save_data_and_size(un, "uf");
	save_data_and_size(u_track, "u_track");
	save_data_and_size(u_exact, "u_exact");
	save_data_and_size(t_out, "t_out");
}




void Data_process::rec_info(ofstream & out)
{
	rowvec para(13);
	fds name_para(13);
	string wt_string = "";
	out << "The data are stored in this text." << endl << "This is the " << vis_name << " case."
		<< endl << "The initial condition option is " << ini_type << endl << "The boundary condition option is " << bnd_type << endl
		 << endl << "The flux option is " << flux_type << endl;
	wt_string += "The parameters are:\n\n";

	para(0) = N; para(1) = x_low; para(2) = x_sup; para(3) = M; para(4) = T; para(5) = nu; para(6) = dx; para(7) = dt; para(8) = N_itr;
 para(9) = err; para(10) = vm; para(11) = rhom; para(12) = safe_fac;
	name_para(0) = "N"; name_para(1) = "x_low"; name_para(2) = "x_sup"; name_para(3) = "M"; name_para(4) = "T";
	name_para(5) = "nu"; name_para(6) = "dx"; name_para(7) = "dt"; name_para(8) = "N_itr";
 name_para(9) = "err"; name_para(10) = "vm"; name_para(11) = "rhom"; name_para(12) = "safe_fac";
	wt_string += get_str_from_tp(para, name_para);
	out << wt_string;

}


string Data_process::get_str_from_tp(rowvec & v, fds & str)
{
	string s = "";
	int n = str.n_elem, i;
	for (i = 0; i < n; i++)
	{
		s += str(i) + " = " + num2str(v(i)) + "\n";
	}
	s += "\n";
	return s;
}

void Data_process::write_log()
{
	string name = "log", wt_string = "";
	name += "_" + vis_name;
	name = get_save_path(get_save_name(name, "txt"));
	// windows use ofstream out(name); linux use ofstream out(name.c_str());
	ofstream out(name.c_str());
	rec_info(out);
	out.close();
}


void Data_process::eva_err(void)
{
	err = 0;
	int i;
	cout << "exact uf is :" << endl << uf_exact << endl << "numeric uf is :" << endl << un << endl;
	for (i = 0; i < N ; i++)
	{
		err += abs(uf_exact(i) - un(i));
	}
	err /= N;
}

string Data_process::dn2s(double x)
{
	string sign = "";
	if (x < 0)
	{
		sign = "n";
		x *= (-1);
	}
	int n = int(x * 10000);
	int n_wan = (n - n % 10000) / 10000;
	n -= n_wan * 10000;
	string s_zero = "";
	if (n < 1000)
		s_zero += "0";
	if (n < 100)
		s_zero += "0";
	if (n < 10)
		s_zero += "0";
	int i;
	for (i = 0; i < 4; i++)
	{
		if (n % 10 == 0)
			n /= 10;
		else
			break;
	}
	if (n == 0)
		return sign + n2s(n_wan);
	else
		return sign + n2s(n_wan) + "p" + s_zero + n2s(n);

}

void Data_process::set_vis_name(string vis_namee)
{
	vis_name = vis_namee;
	if (creat_main_fd_ctrl==1)
		fd_name = main_fd_name+"_"+ n2s(index)+"/"  +vis_name + "_" + n2s(index);
	else
		fd_name = vis_name + "_" + n2s(index);
}

void Data_process::set_main_fd(string main_fd_namee)
{
	creat_main_fd_ctrl = 1;
	main_fd_name = main_fd_namee;
}

int Data_process::maxindex(rowvec & arr)
{
	int n = arr.n_elem,i,ind_max=-1;
	double max = -999;
	for (i = 0; i < n; i++)
	{
		if (arr(i) > max)
		{
			max = arr(i);
			ind_max = i;
		}
	}
	return ind_max;
}
