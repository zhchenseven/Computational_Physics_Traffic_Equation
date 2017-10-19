from Make_movie import Gen_movie
import matplotlib.pyplot as plt
import numpy as np

Plot=Gen_movie()
M=30
fd_name=''
index=0
data_type='dat'
size_sufx='size'
main_fd_name='scan_F_LW'

Plot.set_basic(M,fd_name,data_type,size_sufx,index)
main_fd_ctrl=1
Plot.set_main_fd_ctrl(main_fd_ctrl,main_fd_name)

x_name='R1_x'
t_out_name='R1_t_out'
u_exa_name='R2_u_exact'
u_num_name='R2_u_track'


Plot.set_var(x_name,t_out_name,u_num_name,u_exa_name)
scheme_lst=['Rm','LW','Roe','REF']
for i in xrange(len(scheme_lst)):
    main_fd_name = 'scan_F_'+scheme_lst[i]
    Plot.set_main_fd_ctrl(main_fd_ctrl, main_fd_name)
    scheme_str=scheme_lst[i]
    Plot.plot_cmp_safe_fac(scheme_str)


plt.show()