# Computational_Physics_Traffic_Equation
Traffic phenomena occur every single day and is closely related to everyone. Physically, sudden changes for traffic problems (e.g., red ligh or green light turns on) can be described by the traffic equations.  Here, we present our work to use the finite volume numerical approaches to simulate the traffic problems. The code is written using an object-oriented numerical framework in C++. We also attach the code to process, visualiza the data, and make animations using python packages.

The code is for the third course project in computational fluid dynamics (MASE 5412) in Washington University in St. Louis.

Here, we adopt the object-oriented numerical framework to simulate the physics. The .h and .cpp files that are not beginning with 'run' are files are the classes for defining the numerical procedures. Specifically, Para.cpp and Para.h defines the physical parameters for the equation, the set-up, and for the mesh. IBC.cpp and IBC.h defines the initial and boundary conditions for a specified selection. Then, Evo_dynam.cpp and Evo_dynam.h evolves the iterations that leads to the convergence of thermal equilibrium states. Finally, Data_process.cpp and Data_process.h processes and stores the data, which are further visualized, animated, and interpreted using python.

The run_*.cpp files provide main functions to invoke, embody the class and define a numerical investigations. Various .cpp files are for the case of various parameter sets and various finite volume schemes. The scan_*.cpp files provide various numerical investigations for various parameter sets.

Here, we employ the python files for processing data and generating animations. In doing so, READ_DATA.py and Make_movie.py define the classes. gen_movie_script_*.py provide the main functions for generating animations to show the numerical simulation of the dynamical traffic change. plot_*.py provides the main function for processing and plotting data.

Here, we also provide the necessary information for running the code. 

For the python code, the project work by using the pycharm IDE with specified anaconda library. One thing that is worth noting is one may need to install the opencv3 for generating the animations. 

For the C++ code, we invoke the Armadillo library (http://arma.sourceforge.net/) that provides MATLAB-like functions for linear algebra operations. For the Windows user, one needs to install the MS Visual Studio 2015, and open the example1_win64.vcxproj for running the code. For the Mac OS or Ubuntu user, one needs to install the armadillo library at first (please refer to the readme.txt in the downloaded armadillo package), then compile and link the codes.
