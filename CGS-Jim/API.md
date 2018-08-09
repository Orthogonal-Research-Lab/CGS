# APIs  

### Module: CGS_parcels.fieldset
#### Class CGS_field(x_vel, y_vel)
>CGS_field can be initialized by assigning the velocities in given positions. The velocities should be in the form of 2-dimensional numpy arrays, with positive values pointing to right or up.  
>The simulation environment of CGS is within a region of 1*1 unit square, and the velocities of flows are determined according to positions within the field.  
>For example, if the x_vel is a numpy array of [[0.5,0.2],[0.3,0.4]], then the x_directional velocity in (0.0,1,0) is 0.3.
>>**Parameters:**
>>>**x_vel:** 2-dimensional numpy array determining x_directional velocities at different positions of the field.  
>>>**y_vel:** 2-dimensional numpy array determining y_directional velocities at different positions of the field.

##### deploy_kernels(x_pos, y_pos, pclass):  
>Deploy kernels onto the flow field created above. The positions of kernels in x and y directions should be provided in 1-dimension numpy arrays respectively.
>>**Parameters:**
>>>**x_pos:** 1-dimensional numpy array determining initial positions of kernels in the x_dimension.  
>>>**y_pos:** 1-dimensional numpy array determining initial positions of kernels in the y_dimension.  
>>>**pclass:** Always suggested to use kernel.

##### simulate(time_length, period, output_filename, collision_thres, mutation_period):
>Do the simulation.
>>**Parameters:**
>>>**time_length:** total time length of simulation.  
>>>**period:** time period of simulation.  
>>>**output_filename:** save simulation results to the output file.  
>>>**collision_thres:** under what distance threshold will two kernels be considered as colliding together.  
>>>**mutation_period:** the period of meaning mutations.

##### word_freq_table(mode='total'):
>Show the simulation results in the form of pandas DataFrame table.   
> If the mode is selected as 'total', the total amount of kernels in both active and inactive state will be calculated and presented.  
> If the mode is selected as 'active', only the amount of kernels in active state will be presented.  
>If the mode is selected as 'all', all the information including 'total', 'active' and 'inactive' will be presented.  
>Default mode is 'total'.
>>**Parameters:**
>>>**mode:** Can be one of 'total', 'active', or 'all'.

##### plot_wordfreq(mode='total'):
>Plot the simulation results.
> If the mode is selected as 'total', the total amount of kernels in both active and inactive state will be calculated and presented.  
> If the mode is selected as 'active', only the amount of kernels in active state will be presented.  
>If the mode is selected as 'all', all the information including 'total', 'active' and 'inactive' will be presented.  
>Default mode is 'total'.
>>**Parameters:**
>>>**mode:** Can be one of 'total', 'active', or 'all'.

##### plot_trajectories(file_name,interval=200):
>Show the trajectories of the kernels within the flow field by animation.  
>Should provide filename, perhaps the same as that provided in 'simulate' function.
>>Parameters:
>>>file_name: file name of the simulation result.  
>>>interval: interval of animation. Default interval is 200.  
        
### Module: CGS_parcels.kernel
#### Class kernel_set(fieldset, pclass=kernel, lon=[], lat=[], depth=None, time=None, repeatdt=None)
>Already initialized through CGS_field class.  
>Assign each kernel with word, meaning, fitness and color.

##### set_kernel(word_meaning_freq_fit,prob=0.5,decay_rate=0.01,lower_bound=0.1,ratio=0.5):
> Assign each kernel within the field with word, meaning and fitness according to given frequency.
>> **Parameters:**
>>> **word_meaning_freq_fit:** A dictionary in the form as below  
>>> words_meanings = {'apple':(0.3,[('red',0.15,20),('fruit',0.6,30),('eatable',0.25,5)]), 'tomato':(0.8,[('red',0.3,20),('fruit',0.3,40),('vegetable',0.4,15)])}  
>>> **prob:** probability that a word will transform from 'active' to 'inactive' state.  
>>> **decay_rate:** the decay rate of transformation probability of word state with respect to time.  
>>> **lower bound:** the lower bound of word transforming probability.  
>>> **ratio:** initial proportion of word particles that is in 'active' state.

### Module: CGS_parcels.ngrams
##### getNgrams(query, startYear, endYear,smoothing=0,case_insensitive=False):
> Fetch google ngram data from <https://books.google.com/ngrams> and store the data in pandas.DataFrame form.
>> **Parameters:**
>>> **query:** the words interested. Words should be separated by comma.
>>> **startYear:** start year of the data.
>>> **endYear:** end year of the data.

##### use_ngram(word_meaning,year):
> Fetch word frequency data of a specific year from google ngrams.
>> **Parameters:**
>>>**word_meaning:** should be in the form as below:  
>>>word_meaning = {'apple':[('red',0.15,20),('fruit',0.6,30),('eatable',0.25,5)], 'tomato':[('red',0.3,20),('fruit',0.3,40),('vegetable',0.4,15)]}  
>>>**year:** the specific year of which word frequency data is fetched.

### Module: CGS_parcels.CGS_notebook_tool
#### Class CGS_field_initializer(**kwargs)
>Widgets for CGS to allow easy usage.

##### display():
>Display widgets in jupyter notebook.

##### build(word_meaning_freq_fit=None,collision_thres=1e-4,mutation_period=5,field_set=None,particle_set=None):
>Function starting from initializing CGS_field to simulation.
>>**Parameters:**
>>>**word_meaning_freq_fit:** A dictionary in the form as below  
>>> words_meanings = {'apple':(0.3,[('red',0.15,20),('fruit',0.6,30),('eatable',0.25,5)]), 'tomato':(0.8,[('red',0.3,20),('fruit',0.3,40),('vegetable',0.4,15)])}  
>>> **collision_thres:** collision_thres: under what distance threshold will two kernels be considered as colliding together.  
>>> **mutation_period:** the period of meaning mutations.  

##### plot():
>Plot the simulation results.

##### animate():
>Show the trajectories of the kernels within the flow field by animation.

##### table():
>Show the simulation results in the form of pandas DataFrame table.


