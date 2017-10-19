import numpy as np
from READ_DATA import Read_Data
import cv2
import matplotlib.pyplot as plt
import os
from  pylab import  *
from scipy import interpolate
## This function helps read file from the dat and make movie

class Gen_movie:
    def __init__(self):
        self.M=0
        self.fd_name=''
        self.index=0
        self.x=[]
        self.x_name=''
        self.t_out=[]
        self.t_out_name=''
        self.u_num=[]
        self.u_num_name=''
        self.u_exa=[]
        self.u_exa_name=''
        self.data_type='dat'
        self.size_sufx='size'
        self.read=Read_Data()

        self.mov_name=''
        self.fps=10
        self.fine_fac=2

        self.main_fd_name=''
        self.main_fd_ctrl=0

        self.phase_err=[]
        self.M_arr=[]

    def set_basic(self,M,fd_name,data_type='dat',size_sufx='size',index=0,M_arr=[]):
        self.M=M
        self.fd_name=fd_name
        self.data_type=data_type
        self.size_sufx=size_sufx
        self.index=index
        self.M_arr=M_arr
        if len(M_arr)!=0:
            self.M=len(M_arr)


    def set_var(self,x_name,t_out_name,u_num_name,u_exa_name):
        self.x_name=x_name
        self.t_out_name=t_out_name
        self.u_num_name=u_num_name
        self.u_exa_name=u_exa_name

    def ini_read(self):
        self.read.set_data_info(self.fd_name,self.index,self.data_type,self.size_sufx)

    def read_x(self):
        self.read.set_data_name(self.x_name)
        self.x=self.read.load_bin_cetr()
        self.read.set_data_name(self.u_num_name)
        self.u_num=self.read.load_bin_cetr()
        self.read.set_data_name(self.u_exa_name)
        self.u_exa=self.read.load_bin_cetr()

    def read_t_info(self):
        self.read.set_data_name(self.t_out_name)
        self.t_out=self.read.load_bin_cetr()



    def set_movie_para(self,mov_name,fps,fine_fac):
        self.mov_name=mov_name
        self.fps=fps
        self.fine_fac=fine_fac

    def read_raw_data(self):
        self.ini_read()
        self.read_x()
        self.read_t_info()

    def get_save_name(self,l):
        if l < 10:
            name0 = '000' + str(l)
        elif l < 100:
            name0 = '00' + str(l)
        elif l < 1000:
            name0 = '0' + str(l)
        else:
            name0 = str(l)
        return 'frm' + name0 + '_' + str(self.index) + '.png'

    def incl_path(self,name):
        return self.fd_name+'_'+str(self.index)+'/'+name

    def gen_movie(self):
            y_max_1=np.max(abs(self.u_num))
            y_max_2=np.max(abs(self.u_exa))
            y_max=np.max([y_max_1,y_max_2])
            for i in range(0, self.M + 1):
                print ('generate movie finished', 100 * (i + 1) / (self.M+1), '%')
                j = i + 1
                name = self.get_save_name(j)
                name=self.incl_path(name)
                if i != self.M:
                    fig1= plt.figure()

                    plt.subplot(2,1,1)
                    legd_lst=['u_exact','u_numeric']
                    if len(self.M_arr)==0:
                        plt.plot(self.x, self.u_exa[i, :], linewidth=3,color='red')
                    else:
                        plt.plot(self.x, self.u_exa[self.M_arr[i], :], linewidth=3, color='red')
                    # plt.plot(self.x, self.u_num[i, :], linewidth=1,color='blue')
                    # plt.plot([0, 0], [0, 1.05*y_max], 'k-', lw=1)
                    # plt.ylim(-1.1*y_max, 1.1*y_max)
                    plt.ylim([-0.2,0.2])
                    plt.xlabel('$x$')
                    plt.ylabel('$u$')
                    if len(self.M_arr)==0:
                        plt.title('The movie of wave motion in real space at t='+str(self.t_out[i]))
                    else:
                        plt.title('The movie of wave motion in real space at t=' + str(self.t_out[self.M_arr[i]]))
                    plt.grid(True)
                    plt.legend(["exact"], loc='best',fontsize=10)

                    plt.subplot(2,1,2)
                    legd_lst=['u_exact','u_numeric']
                    # plt.plot(self.x, self.u_num[i, :], linewidth=1,color='red')
                    if len(self.M_arr)==0:
                        plt.plot(self.x, self.u_num[i, :], linewidth=3,color='blue')
                    else:
                        plt.plot(self.x, self.u_num[self.M_arr[i], :], linewidth=3, color='blue')
                    # plt.plot([0, 0], [0, 1.05*y_max], 'k-', lw=1)
                    # plt.ylim(-1.1*y_max, 1.1*y_max)
                    plt.ylim([-0.2,0.2])
                    plt.xlabel('$x$')
                    plt.ylabel('$u$')
                    if len(self.M_arr)==0:
                        plt.title('The movie of wave motion in real space at t='+str(self.t_out[i]))
                    else:
                        plt.title('The movie of wave motion in real space at t=' + str(self.t_out[self.M_arr[i]]))
                    plt.grid(True)
                    plt.legend(["numeric"], loc='best',fontsize=10)
                    # plt.subplot(2, 1, 1)
                    # plt.semilogy(np.arange(0,self.ind_track[i]+1), self.itr_dif[0:self.ind_track[i]+1], linewidth=1,color='r')
                    # plt.xlim(0, self.ind_track[-1])
                    # plt.ylim(0, 1.05 * y_max)
                    # plt.xlabel('iteration')
                    # plt.ylabel('inf_norm_dif')
                    # plt.title('Difference Norm trace when iteraction='+str(self.ind_track[i]+1))
                    # plt.grid(True)
                    # # plt.legend(legd_lst, loc='best',fontsize=7)
                    # plt.subplot(2,1,2)
                    # x_new, y_new, Z = self.interp_2D(self.x, self.x, self.fx[:, :, i], self.fine_fac)
                    # X, Y = np.meshgrid(x_new, y_new)
                    # plt.pcolormesh(X, Y, Z, shading='gouraud',vmin=0,vmax=f_max)
                    # # plt.plot([x[0], x[-1]], [0, 0], linewidth=1, color='magenta')
                    # # plt.plot([0, 0], [x[0], x[-1]], linewidth=1, color='magenta')
                    # plt.title("T ")
                    # plt.xlabel('$x_1$')
                    # plt.ylabel('$x_2$')
                    # axis('equal')
                    # plt.colorbar()
                    fig1.savefig(name)
                    plt.close()
                else:
                    fig1 = plt.figure()
                    plt.subplot(1, 1, 1)
                    plt.plot([], [])
                    fig1.savefig(name)
                    plt.close()

            name=self.get_save_name(1)
            name=self.incl_path(name)
            img = cv2.imread(name)
            height, width, layers = img.shape
            #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            if os.name=='nt':
                fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            else:
                fourcc=cv2.cv.CV_FOURCC(*'avc1')
            #fourcc = cv2.VideoWriter_fourcc(*'avc1')
            #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            #fourcc=cv2.cv.CV_FOURCC(*'XVID')
            mov_name = self.mov_name +'_'+ str(self.index) + '.avi'
            mov_name=self.incl_path(mov_name)
            video = cv2.VideoWriter(mov_name, fourcc, self.fps, (width, height))
            for i in range(0,self.M+1):
                j=i+1
                print ('movies finished', 100 * i / self.M, '%')
                name=self.get_save_name(j)
                name=self.incl_path(name)
                img = cv2.imread(name)
                video.write(img)
                os.remove(name)
            cv2.destroyAllWindows()
            video.release()

    def interp_2D(self, x, y, Z, fine_fac):
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        f = interpolate.RectBivariateSpline(y, x, Z)
        dx = dx / fine_fac
        dy = dy / fine_fac
        xnew = np.arange(x[0], x[-1] + dx, dx)
        ynew = np.arange(y[0], y[-1] + dy, dy)
        znew = f(ynew, xnew)
        return (xnew, ynew, znew)

    def set_main_fd_ctrl(self,main_fd_ctrl,main_fd_name):
        self.main_fd_ctrl=main_fd_ctrl
        self.main_fd_name=main_fd_name

    def retn_file_name(self):
        if self.main_fd_ctrl==1:
            return self.main_fd_name+'_'+str(self.index)+'/'+self.fd_name
        else:
            return self.fd_name

    def read_x_data(self,read_ini_ctrl=0):
        read = Read_Data()
        read.set_data_info(self.retn_file_name(), self.index, self.data_type, self.size_sufx)

        read.set_data_name(self.u_num_name)
        u_num=read.load_bin_cetr()
        if read_ini_ctrl==0:
            return u_num
        else:
            read.set_data_name(self.x_name)
            x=read.load_bin_cetr()
            read.set_data_name(self.u_exa_name)
            u_exa=read.load_bin_cetr()
            return x,u_exa,u_num

    def plot_group_data(self,fd_name_base,var_name,var_str,var_val,y_min=0,y_max=0):
        # fdname basis is the folder name base string, var_name is the string of the name to be changed of interest, var_str is the list of strings to be evaluated for the var
        # var_val is the list of values of variable
        n=len(var_str)
        self.phase_err=[]
        for i in range(n):

            self.fd_name=fd_name_base+'_'+var_name+'_'+var_str[i]
            if i==0:
                x,u_exa,u_num=self.read_x_data(1)
                u_exa=u_exa[-1,:]
                u_num_arr=zeros((n,len(u_exa)))
            else:
                u_num = self.read_x_data()
            self.phase_err.append(x[argmax(u_num)]-x[argmax(u_exa)])

            u_num_arr[i, :] = u_num
        print self.phase_err
        # then start to plot
        f1=plt.figure()
        # y_max=-99
        # y_min=99
        ax=f1.add_subplot(1,1,1)
        # norm_all=np.zeros(self.M)
        col_lst = ['k', 'b', 'r', 'g', 'm']
        plt.plot(x, u_exa,'o', linewidth=3,color=col_lst[0],markersize=10)
        # y_max=np.max([y_max,u_exa.max()])
        # y_min = np.min([y_min, u_exa.min()])
        legd_lst = []
        legd_lst.append('exact')
        for i in range(n):
            plt.plot(x, u_num_arr[i,:], linewidth=3,color=col_lst[i+1])
            legd_lst.append(var_name+'='+str(var_val[i]))
            # y_max = np.max([y_max, u_num_arr[i,:].max()])
            # y_min = np.min([y_min, u_num_arr[i,:].min()])
            # norm_all+=self.norm_simp[i][0]
        # self.norm_simp.append((norm_all,'all'))
        # plt.plot(self.t_out, norm_all, linewidth=3, color='k')
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='x', labelsize=40)
        ax.tick_params(axis='y', labelsize=40)
        if y_min!=0 or y_max!=0:
            plt.ylim(y_min,y_max)
        # plt.ylim(1.1*y_min, 1.1*y_max)
        title_string='The results of the exact u and numerical results in the case of ' +str(fd_name_base)
        plt.title(title_string,fontsize=20)
        plt.xlabel('$x$',fontsize=50)
        plt.ylabel('u',fontsize=50)
        plt.grid(True)
        ll=plt.legend(legd_lst,loc='best',fontsize=30)
        ll.get_frame().set_linewidth(2)

    def plot_err_norm(self,nu,err_arr,title_str,scheme_lst,y_min=0,y_max=0,log_scale_ctrl=0):
        f1=plt.figure()
        # y_max=-99
        # y_min=99
        ax=f1.add_subplot(1,1,1)
        # norm_all=np.zeros(self.M)
        col_lst = ['k', 'b', 'r', 'g', 'm']
        n=len(nu)
        x=np.arange(1,n+1)
        m=len(scheme_lst)
        nu_lst=[]
        for i in range(m):
            plt.plot(x, err_arr[i,:],'-o', linewidth=3,color=col_lst[i+1],markersize=10)
        for i in range(n):
            nu_lst.append('nu='+str(nu[i]))
            # y_max = np.max([y_max, err_arr[i,:].max()])
            # y_min = np.min([y_min, err_arr[i,:].min()])
            # norm_all+=self.norm_simp[i][0]
        # self.norm_simp.append((norm_all,'all'))
        # plt.plot(self.t_out, norm_all, linewidth=3, color='k')
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='x', labelsize=40)
        ax.tick_params(axis='y', labelsize=40)
        # plt.ylim(1.1*y_min, 1.1*y_max)
        title_string='The results of the L1 norm of error of between the exact u and numerical results in the case of ' +title_str
        plt.title(title_string,fontsize=20)
        if log_scale_ctrl==1:
            ax.set_yscale("log", nonposy='clip')
        plt.xlabel('nu',fontsize=30)
        plt.ylabel('$\epsilon$',fontsize=50)
        plt.xticks(x, nu_lst,fontsize=30)
        if y_min!=0 or y_max!=0:
            plt.ylim(y_min,y_max)
        plt.grid(True)
        plt.xlim(0.5,4.5)
        ll=plt.legend(scheme_lst,loc='best',fontsize=40)
        ll.get_frame().set_linewidth(2)

    def plot_ampd_phase_err(self,nu,theta,scheme_lst,title_str,ampd_arr,err_type,plot_ana_ctrl=0,y_min=0,y_max=0,N_itr=[]):
        n=len(nu)
        m=len(scheme_lst)
        if plot_ana_ctrl==1:
            ana_ampd_arr=np.zeros((m,n))
            for i in range(m):
                for j in range(n):
                    ana_ampd_arr[i,j]=self.retn_ana_err_cetr(err_type,scheme_lst[i],theta,nu[j])
                    if err_type=='phase':
                        ana_ampd_arr[i, j]*=-N_itr[j]
                    else:
                        ana_ampd_arr[i, j] =np.power(ana_ampd_arr[i,j],N_itr[j])


        f1=plt.figure()
        # y_max=-99
        # y_min=99
        ax=f1.add_subplot(1,1,1)
        # norm_all=np.zeros(self.M)
        col_lst = ['k', 'b', 'r', 'g', 'm']
        n=len(nu)
        x=np.arange(1,n+1)
        nu_lst=[]
        if err_type=='phase':
            ampd_arr/=np.pi
        for i in range(m):
            plt.plot(x, ampd_arr[i,:],'-o', linewidth=3,color=col_lst[i+1],markersize=10)
        for i in range(n):
            nu_lst.append('nu=' + str(nu[i]))
            # y_max = np.max([y_max, ampd_arr[i,:].max()])
            # y_min = np.min([y_min, ampd_arr[i,:].min()])
        if plot_ana_ctrl==1:
            if err_type == 'phase':
                ana_ampd_arr /= np.pi
            for i in range(m):
                plt.plot(x, ana_ampd_arr[i, :], '--x', linewidth=3, color=col_lst[i + 1],markersize=40)
                # y_max = np.max([y_max, ampd_arr[i, :].max()])
                # y_min = np.min([y_min, ampd_arr[i, :].min()])
            # norm_all+=self.norm_simp[i][0]
        # self.norm_simp.append((norm_all,'all'))
        # plt.plot(self.t_out, norm_all, linewidth=3, color='k')
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='x', labelsize=40)
        ax.tick_params(axis='y', labelsize=40)
        # plt.ylim(1.1*y_min, 1.1*y_max)
        title_string='The results of the ' +err_type+ ' error of both the analytical and numerical results in the case of ' +title_str
        plt.title(title_string,fontsize=20)
        plt.xlabel('nu',fontsize=50)
        if err_type=='ampd':
            plt.ylabel('|z|',fontsize=50)
        else:
            plt.ylabel('phase error ($\pi$)', fontsize=50)
        plt.xticks(x, nu_lst, fontsize=30)
        plt.grid(True)
        full_lst=scheme_lst
        plt.xlim(0.5, 4.5)
        if y_min!=0 or y_max!=0:
            plt.ylim(y_min,y_max)
        # plt.ylim(0, 1.2)
        if plot_ana_ctrl:
            for i in range(len(scheme_lst)):
                full_lst.append(scheme_lst[i]+',analytical')
        ll=plt.legend(full_lst,loc='best',fontsize=20)
        ll.get_frame().set_linewidth(2)



    def retn_ana_err_cetr(self,err_type,scheme_type,theta,nu):
        if scheme_type=='LF':
            return self.retn_err_LF(err_type,theta,nu)
        elif scheme_type=='UW1':
            return self.retn_err_UW1(err_type, theta, nu)
        elif scheme_type=='LW':
            return self.retn_err_LW(err_type, theta, nu)
        elif scheme_type=='MD':
            return self.retn_err_MD(err_type, theta, nu)


    def retn_err_LF(self,err_type,theta,nu):
        if err_type=='ampd':
            return np.sqrt(np.cos(theta)**2+nu**2*np.sin(theta)**2)
        else:
            return nu*theta+np.arctan(-nu*np.tan(theta))

    def retn_err_UW1(self,err_type,theta,nu):
        if err_type=='ampd':
            return np.sqrt((1-nu+nu*cos(theta))**2+nu**2*np.sin(theta)**2)
        else:
            return nu*theta+np.arctan(-nu*np.sin(theta)/(1-nu+nu*np.cos(theta)))

    def retn_err_LW(self,err_type,theta,nu):
        if err_type=='ampd':
            return np.sqrt(1-nu**2*(1-nu**2)*(1-np.cos(theta))**2)
        else:
            return nu*theta+np.arctan(-nu*np.sin(theta)/(1+nu**2*(np.cos(theta)-1)))

    def retn_err_MD(self, err_type, theta, nu):
        if err_type=='ampd':
            return np.sqrt((1-2*self.q(nu)*np.sin(theta/2)**2)**2+nu**2*np.sin(theta)**2)
        else:
            return nu*theta+np.arctan(-nu*np.sin(theta)/(1-2*self.q(nu)*np.sin(theta/2)**2))

    def q(self,nu):
        return 1.0/3.0+2*nu**2/3.0


    def plot_cmp_scheme(self,scheme_str,suf_string='',y_max=0):
        self.fd_name=scheme_str+'_sf_0p3_T_60'
        x, u_exa, u_num= self.read_x_data(1)
        M=u_exa.shape[0]
        u_exa_f=u_exa[M-1,:]
        u_num_f=u_num[M-1,:]
        u_num_i=u_num[0,:]

        if len(suf_string)!=0:
            self.set_main_fd_ctrl(1,'scan_F_'+scheme_str+suf_string)
            self.fd_name = scheme_str + '_sf_0p3_T_60'
            x_alt, u_exa, u_num = self.read_x_data(1)
            M = u_exa.shape[0]
            u_num_f_alt = u_num[M - 1, :]
            u_num_i_alt = u_num[0, :]


        f1=plt.figure()
        # y_max=-99
        # y_min=99
        ax=f1.add_subplot(1,1,1)
        # norm_all=np.zeros(self.M)
        col_lst = ['k', 'b', 'r', 'g', 'm']
        l1=plt.plot(x, u_exa_f,'r-o', linewidth=3,markersize=10)
        # y_max=np.max([y_max,u_exa.max()])
        # y_min = np.min([y_min, u_exa.min()])
        legd_lst = []
        legd_lst.append('exact')
        legd_lst.append('numeric')
        legd_lst.append('initial')
        l2 = plt.plot(x, u_num_f, linewidth=3, color='b')
        l3 = plt.plot(x, u_num_i, 'g--o', linewidth=3, markersize=10)
        if len(suf_string) != 0:
            l4= plt.plot(x_alt, u_num_f_alt, linewidth=3, color='c')
            l5 = plt.plot(x_alt, u_num_i_alt, 'm--o', linewidth=3, markersize=10)
            legd_lst.append('numerical, interior discontinuity')
            legd_lst.append('initial, interior discontinuity')
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='x', labelsize=40)
        ax.tick_params(axis='y', labelsize=40)
        if y_max!=0:
            plt.ylim(0, y_max)
        else:
            plt.ylim(0, 0.25)
        title_string='The results of the exact u and numerical results of the ' +scheme_str + ' flux case.'
        plt.title(title_string,fontsize=20)
        plt.xlabel('$x$',fontsize=50)
        plt.ylabel(r'$\rho$',fontsize=50)
        plt.grid(True)
        ll=plt.legend(legd_lst,loc='best',fontsize=30)
        ll.get_frame().set_linewidth(2)


    def plot_cmp_safe_fac(self,scheme_str):

        fd_name_str=[]
        sf_str=['0p3','0p6','0p9']
        for i in xrange(len(sf_str)):
            fd_name_str.append(scheme_str+'_sf_'+sf_str[i]+'_T_60')
        # read safe_fac=0.3 case
        self.fd_name=fd_name_str[0]
        x, u_exa, u_num= self.read_x_data(1)
        M=u_exa.shape[0]
        u_exa_f=u_exa[M-1,:]
        u_num_f_0p3=u_num[M-1,:]
        u_num_i=u_num[0,:]

        # read safe_fac=0.6 case
        self.fd_name = fd_name_str[1]
        _, u_exa, u_num = self.read_x_data(1)
        M=u_exa.shape[0]
        u_num_f_0p6=u_num[M-1,:]

        # read safe_fac=0.9 case
        self.fd_name = fd_name_str[2]
        _, u_exa, u_num = self.read_x_data(1)
        M=u_exa.shape[0]
        u_num_f_0p9=u_num[M-1,:]


        f1=plt.figure()
        # y_max=-99
        # y_min=99
        ax=f1.add_subplot(1,1,1)
        # norm_all=np.zeros(self.M)
        col_lst = ['k', 'b', 'r', 'g', 'm']
        l1=plt.plot(x, u_exa_f,'r-o', linewidth=3,markersize=10)
        # y_max=np.max([y_max,u_exa.max()])
        # y_min = np.min([y_min, u_exa.min()])
        legd_lst = []
        legd_lst.append('exact')
        legd_lst.append('safe_fac=0.3')
        legd_lst.append('safe_fac=0.6')
        legd_lst.append('safe_fac=0.9')
        l2 = plt.plot(x, u_num_f_0p3, linewidth=3, color='b')
        l3 = plt.plot(x, u_num_f_0p6, linewidth=3, color='g')
        l4 = plt.plot(x, u_num_f_0p9, linewidth=3, color='m')
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='x', labelsize=40)
        ax.tick_params(axis='y', labelsize=40)

        # plt.ylim(-0.5, 0.5)
        title_string='The results of different safe factor results of the ' +scheme_str + ' flux case.'
        plt.title(title_string,fontsize=20)
        plt.xlabel('$x$',fontsize=50)
        plt.ylabel(r'$\rho$',fontsize=50)
        plt.grid(True)
        ll=plt.legend(legd_lst,loc='best',fontsize=30)
        ll.get_frame().set_linewidth(2)

    def plot_cmp_T_f(self,scheme_str):
        fd_name_str=[]
        T_str=['20','40','60']
        for i in xrange(len(T_str)):
            fd_name_str.append(scheme_str+'_sf_0p3_T_'+T_str[i])
        # read T=20 case
        self.fd_name=fd_name_str[0]
        x, u_exa, u_num= self.read_x_data(1)
        M=u_exa.shape[0]
        u_exa_T_20=u_exa[M-1,:]
        u_num_T_20=u_num[M-1,:]
        u_num_i=u_num[0,:]

        # read T=40 case
        self.fd_name=fd_name_str[1]
        x, u_exa, u_num= self.read_x_data(1)
        M=u_exa.shape[0]
        u_exa_T_40=u_exa[M-1,:]
        u_num_T_40=u_num[M-1,:]


        # read T=60 case
        self.fd_name=fd_name_str[2]
        x, u_exa, u_num= self.read_x_data(1)
        M=u_exa.shape[0]
        u_exa_T_60=u_exa[M-1,:]
        u_num_T_60=u_num[M-1,:]


        f1=plt.figure()
        # y_max=-99
        # y_min=99
        ax=f1.add_subplot(1,1,1)
        # norm_all=np.zeros(self.M)
        col_lst = ['k', 'b', 'r', 'g', 'm']
        l1=plt.plot(x, u_num_i,'k--o', linewidth=3,markersize=10)
        # y_max=np.max([y_max,u_exa.max()])
        # y_min = np.min([y_min, u_exa.min()])
        legd_lst = []
        legd_lst.append('initial')
        legd_lst.append('T=20,numeric')
        legd_lst.append('T=20,exact')
        legd_lst.append('T=40,numeric')
        legd_lst.append('T=40,exact')
        legd_lst.append('T=60,numeric')
        legd_lst.append('T=60,exact')
        l2 = plt.plot(x, u_num_T_20,'r', linewidth=3)
        l3 = plt.plot(x, u_exa_T_20,'ro' ,linewidth=3)
        l4 = plt.plot(x, u_num_T_40,'b', linewidth=3)
        l5 = plt.plot(x, u_exa_T_40,'bo' ,linewidth=3)
        l6 = plt.plot(x, u_num_T_60,'g', linewidth=3)
        l7 = plt.plot(x, u_exa_T_60,'go' ,linewidth=3)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(4)
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='x', labelsize=40)
        ax.tick_params(axis='y', labelsize=40)

        # plt.ylim(-0.1, 0.2)
        title_string='The results of different final results of the ' +scheme_str + ' flux case.'
        plt.title(title_string,fontsize=20)
        plt.xlabel('$x$',fontsize=50)
        plt.ylabel(r'$\rho$',fontsize=50)
        plt.grid(True)
        ll=plt.legend(legd_lst,loc='best',fontsize=30)
        ll.get_frame().set_linewidth(2)


