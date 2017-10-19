from Make_movie import Gen_movie
import numpy as np


Movie=Gen_movie()
M=202
# M_arr=np.arange(0,3999,50)
fd_name='Rm_T_60_sf_0p3_ini_di'
index=0
data_type='dat'
size_sufx='size'

Movie.set_basic(M,fd_name,data_type,size_sufx,index)

x_name='R1_x'
t_out_name='R1_t_out'
u_exa_name='R2_u_exact'
u_num_name='R2_u_track'

mov_name='demo'
fps=10
fine_fac=4
Movie.set_movie_para(mov_name,fps,fine_fac)

Movie.set_var(x_name,t_out_name,u_num_name,u_exa_name)
Movie.read_raw_data()
Movie.gen_movie()