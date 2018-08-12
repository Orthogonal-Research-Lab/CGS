import numpy as np
import ipywidgets as widgets
from CGS_parcels.fieldset import CGS_field
from CGS_parcels.kernel import kernel
from IPython.display import display

class CGS_field_initializer(widgets.Tab):
    """Widgets for CGS to allow easy usage.
    """
    def __init__(self,**kwargs):
        self._set_tab()
        style = {'description_width': 'initial'}
        children = [self._field_setting, self._particle_setting, self._simulation_setting, self._output_setting, \
                 self._word_setting]
        super(CGS_field_initializer,self).__init__(children=children,style=style, **kwargs)
        
    def _set_tab(self):
        ## set titles
        style = {'description_width': 'initial'}
        self.set_title(0,'Field setting')
        self.set_title(1,'Particle setting')
        self.set_title(2,'Simulation setting')
        self.set_title(3,'Output setting')
        self.set_title(4,'Word setting')
        
        ## set widgets
        self._field_setting = widgets.Select(options=['random','vortex','self-defined'],description='Select a field setting: ',\
                                            disabled=False,value='random',style=style)
        self._particle_num = widgets.IntText(description='Number of particles initially: ',disabled=False,value=100,style=style)
        self._particle_mode = widgets.Select(options=['random','middle','self-defined'],description=\
                                    'How particles are distributed initially: ',disables=False,value='random',style=style)
        self._particle_setting = widgets.Accordion(children=[self._particle_num,self._particle_mode])
        self._particle_setting.set_title(0,'Num of particles')
        self._particle_setting.set_title(1,'Distribution mode of particles')
        self._time_length = widgets.IntText(description='Simulation time length: ',disabled=False,value=200,style=style)
        self._time_period = widgets.IntText(description='Simulation time period: ',disabled=False,value=5,style=style)
        self._collision_threshold = widgets.FloatText(description='Particles collision threshold: ',disabled=False,value=0.0001,\
                                                    style=style)
        self._simulation_setting = widgets.Accordion(children=[self._time_length,self._time_period,self._collision_threshold])
        self._simulation_setting.set_title(0,'Time length')
        self._simulation_setting.set_title(1,'Time period')
        self._simulation_setting.set_title(2,'Collision threshold')
        self._output_setting = widgets.Text(description='Save output file to: ',disabled=False,style=style,\
                                            layout=widgets.Layout(width='50%'),value='C:\Users\User\Downloads\example')
        self._decay_rate = widgets.FloatText(description='Decay rate of transformation probability:',\
                                           disabled=False,value=0.001,style=style,layout=widgets.Layout(width='40%'))
        self._mutation_period = widgets.IntText(description='Mutation period of meanings: ',disabled=False,value=5,style=style)
        self._word_setting = widgets.Accordion(children=[self._decay_rate,self._mutation_period])
        self._word_setting.set_title(0,'State transformation probability decay rate')
        self._word_setting.set_title(1,'Mutation period of meanings')
    
    @property
    def field_setting(self):
        return self._field_setting
    
    @property
    def particle_distribution(self):
        return self._particle_mode
    
    @property
    def particle_num(self):
        return self._particle_num
    
    @property
    def time_length(self):
        return self._time_length
    
    @property
    def time_period(self):
        return self._time_period
    
    @property
    def output_file(self):
        return self._output_setting
    
    @property
    def animation_setting(self):
        return self._animation_setting
    
    def build(self,word_meaning_freq_fit=None,collision_thres=1e-4,mutation_period=5,field_set=None,particle_set=None):
        """
        Function starting from initializing CGS_field to simulation.
        """
        if word_meaning_freq_fit == None:
            raise RuntimeError('Please input word_meaning_freq_fit.')
        if self._field_setting.value == 'random':
            xv = np.random.uniform(-1.0,1.0,[100,100])*2e-4
            yv = np.random.uniform(-1.0,1.0,[100,100])*2e-4
        elif self._field_setting.value == 'vortex':
            omega = 2e-3
            x_pos = np.linspace(0.0,1.0,51,endpoint=False)[1:51]
            y_pos = np.linspace(0.0,1.0,51,endpoint=False)[1:51]
            xv = omega*x_pos
            yv = omega*y_pos
        else:
            try:
                xv,yv = field_set
            except ValueError:
                raise ValueError('Please input field_set in the form of (x_velocities,y_velocities).')
            except TypeError:
                raise TypeError('Please input field_set or select other pre-defined field_set mode.')
            
        if self._particle_num.value == 0:
            raise RuntimeError('Please specify the number of particles in the field.')
            
        if self._particle_mode.value == 'random':
            xpos = np.random.rand(self._particle_num.value)
            ypos = np.random.rand(self._particle_num.value)
        elif self._particle_mode.value == 'middle':
            xpos = np.array([0.5]*self._particle_num.value,dtype=np.float32)
            ypos = np.array([0.5]*self._particle_num.value,dtype=np.float32)
        else:
            try:
                xv,yv = particle_set
            except ValueError:
                raise ValueError('Please input particle_set in the form of (x_positions,y_positions).')
            except TypeError:
                raise TypeError('Please input particle_set or select other pre-defined particle_set mode.')
        
        if self._time_length.value == 0:
            raise RuntimeError('Please specify the time length of simulation.')
        if self._time_period.value == 0:
            raise RuntimeError('Please specify the time period of simulation.')
        
        if self._output_setting.value == '':
            raise RuntimeError('Please specify the output file path of simulation.')

        if self._decay_rate.value < 0.0 or self._decay_rate.value > 0.5:
            raise RuntimeError('Decay rate should be in the range from 0.0 to 0.5')
            
        if self._mutation_period.value == 0:
            raise RuntimeError('Please specify the mutation period of meanings.')
        
        if self._collision_threshold.value < 0.0 or self._collision_threshold.value > 1e-3:
            raise RuntimeError('Collision threshold should be in the range from 0.0 to 0.001')
     
        self.CGS = CGS_field(xv,yv)
        self.CGS.deploy_kernels(xpos,ypos,kernel)
        self.CGS.kset.set_kernel(word_meaning_freq_fit)
        
        self.CGS.simulate(self._time_length.value,self._time_period.value,self._output_setting.value,\
                          self._collision_threshold.value,self._mutation_period.value)
    
    def plot(self):
        self.CGS.plot_wordfreq()

    def animate(self,interval=200):
        return self.CGS.plot_trajectories(self._output_setting.value,interval)

    def table(self):
        return self.CGS.word_freq_table()
        
    def display(self):
        """
        Display widgets in jupyter notebook
        """
        display(self)
