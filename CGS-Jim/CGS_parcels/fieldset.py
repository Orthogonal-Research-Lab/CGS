import parcels
import sys
import warnings
import numpy as np
from datetime import timedelta
from argparse import ArgumentParser
from CGS_parcels.plot_kernel import plot_kernel_trajectories
from CGS_parcels.kernel import kernel_set
from CGS_parcels.kernel_file import kernel_file
from CGS_parcels.advection import self_AdvectionRK4

class CGS_field:
    """CGS flow field that simulates the environmental flows.
    The field can be initialized by the velocities of flows in given positions.
    """
    
    def __init__(self,x_vel,y_vel):
        """CGS_field can be initialized by assigning the velocities in given positions.
        The velocities should be in the form of 2-dimensional numpy arrays, with postive values pointing to right or up.
        The simulation environment of CGS is within a region of 1*1 unit square, and the velocities of flows are detemined
        according to positions within the field. For example, if the x_vel is a numpy array of [[0.5,0.2],[0.3,0.4]], then
        the x-directional velocity in (0.0,1,0) is 0.3.
        """
        
        ## make sure the dimensions of x_vel are equal to those of y_vel
        if x_vel.shape != y_vel.shape:
            raise RuntimeError("The dimensions of x_vel should be the same as those of y_vel")
        
        self.x_velocities = x_vel
        self.y_velocities = y_vel

        
        ## initialize parcels fields with lon and lat values set according to the values of len(x_vel) and len(y_vel)
        field_x = parcels.Field(name='U',data=x_vel,lon=np.linspace(start=0,stop=1,num=len(x_vel[0])),\
                                lat=np.linspace(start=0,stop=1,num=len(x_vel)))
        field_y = parcels.Field(name='V',data=y_vel,lon=np.linspace(start=0,stop=1,num=len(y_vel[0])),\
                                lat=np.linspace(start=0,stop=1,num=len(y_vel)))
        
        ## initialize parcels fieldset with fields created above
        fieldset = parcels.FieldSet(U=field_x,V=field_y)
        self.fieldset = fieldset
        
    def deploy_kernels(self,x_pos,y_pos,pclass):
        """Deploy kernels onto the flow field created above. 
        The postions of kernels in x and y directions should be provided in 1-dimension numpy arrays respectively.
        For example, if two kernels are created, and the x_pos and y_pos are set as [1,2] and [3,4], then
        the positions of the two kernels will be at [1,3] and [2,4] respectively.
        """
        
        ## set the pclass to be self-defined kernel
        kset = kernel_set(fieldset=self.fieldset,pclass=pclass,lon=x_pos,lat=y_pos)
        self.kset = kset
    
    def simulate(self,time_length,period,output_filename,collision_thres,mutation_period):
        """Do the simulation.
        time_length: total time length of simulation.
        period: time period of simulation.
        output_filename: save simulation results to the output file.
        collision_thres: under what distance threshold will two kernels be considered as colliding together.
        mutation_period: the period of meaning muatations. 
        """
        
        ## do the simulation with time information provided above. outputfile updated with period provided above.
        kset = self.kset
        data = kset.execute(collision_thres,mutation_period,pyfunc=self_AdvectionRK4,runtime=timedelta(minutes=time_length),\
                            dt=timedelta(minutes=period),output_file=kernel_file(name=output_filename,\
                                                     particleset=kset,outputdt=timedelta(minutes=period)))
        self.kernel_FSM = data

    def word_freq_table(self,mode='total'):
        """Show the simulation results in the form of pandas DataFrame table.
        If the mode is selected as 'total', the total amount of kernels in both active and inactive state will be calculated
        and presented.
        If the mode is selected as 'active', only the amount of kernels in active state will be presented.
        If the mode is selected as 'all', all the information including 'total', 'active' and 'inactive' will be presented.
        Default mode is 'total'.
        """
        
        data = self.kernel_FSM
        if mode == 'total':
            x_data = [tot for tot in data.columns.values if tot[1] == 'total']
        elif mode == 'active':
            x_data = [act for act in data.columns.values if act[1] == 'active']
        elif mode == 'all':
            x_data = data.columns[1:]
        else:
            x_data = [tot for tot in data.columns.values if tot[1] == 'total']
        return data[x_data]
       
    def plot_wordfreq(self,mode='total'):
        """Plot the simulation results.
        If the mode is selected as 'total', the total amount of kernels in both active and inactive state will be calculated
        and presented.
        If the mode is selected as 'active', only the amount of kernels in active state will be presented.
        If the mode is selected as 'all', all the information including 'total', 'active' and 'inactive' will be presented.
        Default mode is 'total'.
        """
        
        data = self.kernel_FSM
        if mode == 'total':
            y_data = [tot for tot in data.columns.values if tot[1] == 'total']
        elif mode == 'active':
            y_data = [act for act in data.columns.values if act[1] == 'active']
        elif mode == 'all':
            y_data = data.columns[1:]
        else:
            y_data = [tot for tot in data.columns.values if tot[1] == 'total']
        data.plot(x='time',y=y_data)
        
    def plot_trajectories(self,file_name,interval=200):
        """Show the trajectories of the kernels within the flow field by animation.
        Should provide filename, perhaps the same as that provided in 'simulate' function.
        Could set the interval of animation. Default interval is 200.
        """
        return plot_kernel_trajectories(file_name+'.nc', interval)

