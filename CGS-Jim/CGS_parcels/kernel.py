import parcels
import random
import pandas as pd
import numpy as np
from CGS_parcels.advection import self_AdvectionRK4
from datetime import timedelta,datetime 

class word_state:
    
    def __init__(self,word,prob,status,meaning=None,fitness=None,color=None):
        """
        prob = probability to change from status 'active' to status 'inactive'.
        status = single character to present the status: A for activate, B for inactivate.
        word = the word it represents.
        meaning = the meaning it represents.
        """
        self.word = word
        self.prob = prob
        self.status = status
        self.meaning = meaning
        self.fitness = fitness
        self.color = color
    
    def transition(self):
        """
        Check whether the kernel is activated (status A) or inactivated (status B).
        Then do the transition according to given probability.
        """
        
        if self.status == 'A':
            randnum = random.uniform(0.0,1.0)
            if randnum < self.prob:
                self.status = 'B'
        else:
            self.status == 'A'
            
    def mutation(self,total_fitness,all_meanings):
        """
        Mutation that change the meaning of a word, but does not change the word.
        """
        
        fitnesses = [attr[1] for attr in all_meanings]
        odds = [float(fit)/total_fitness for fit in fitnesses]
        opt = random.random()
        acc = 0.0
        for i in range(len(odds)-1):
            if opt>=acc and opt<acc+odds[i]:
                self.meaning = all_meanings[i][0]
            acc += odds[i]

class kernel(parcels.ScipyParticle):
    """Inherit kernels from ScipyParticle in parcels.
    Add additional functionalities for finite state machine, word_meaning and color settings.
    """
    def __init__(self, lon, lat, fieldset, depth=0., time=0., cptr=None):
        """The nd_array serves as additional attributes of ScipyParticle.
        The nd_array should be given in the form of numpy array. 
        """
        self.word_state = None
        super(kernel,self).__init__(lon, lat, fieldset, depth=0., time=0., cptr=None)
        
    def set_FSM(self,word,prob,ratio):
        randnum = random.uniform(0.0,1.0)      
        status = 'A' if randnum < ratio else 'B'
        self.word_state = word_state(word,prob,status)
    
    def set_word_meaning(self,meaning,fitness):
        self.word_state.meaning = meaning
        self.word_state.fitness = fitness
    
    def set_color(self,color):
        self.word_state.color = color

 
class kernel_set(parcels.ParticleSet):
    """
    Class inherited from parcels.ParticleSet.
    Assign each kernel with word, meaning, fitness and color.
    """
    def __init__(self, fieldset, pclass=kernel, lon=[], lat=[], depth=None, time=None, repeatdt=None):
        super(kernel_set,self).__init__(fieldset=fieldset, pclass=pclass, lon=lon, lat=lat, depth=None, time=None, repeatdt=None)
    
    def set_kernel(self,word_meaning_freq_fit,prob=0.5,decay_rate=0.01,lower_bound=0.1,ratio=0.5):  
        """Assign each kernel within the field with word, meaning and fitness according to given frequency.
        """
        self._set_particle_color(word_meaning_freq_fit)
        self._prob_decay_rate = decay_rate
        self._prob_lower_bound = lower_bound
        kernel_amount = len(self.particles)
        word_freq = [(word,word_attr[0]) for word,word_attr in word_meaning_freq_fit.items()]
        kernel_id_word = 0
        for item in word_freq:
            word,w_freq = item
            relative_freq_word = w_freq/sum([freq for _,freq in word_freq])
            word_num = int(round(kernel_amount * relative_freq_word))
            if word_num + kernel_id_word >= kernel_amount + 1:
                word_num = kernel_amount - kernel_id_word
            for idx in range(word_num):
                self.particles[idx+kernel_id_word].set_FSM(word,prob,ratio)
            meaning_freq_fit = word_meaning_freq_fit[word][1]
            kernel_id_meaning = 0
            for meaning_tuple in meaning_freq_fit:
                meaning,m_freq,fitness = meaning_tuple
                meaning_num = int(round(word_num * m_freq))
                if meaning_num + kernel_id_meaning >= word_num +1:
                    meaning_num = word_num - kernel_id_meaning
                for idx in range(meaning_num):
                    self.particles[idx+kernel_id_meaning+kernel_id_word].set_word_meaning(meaning,fitness)
                    self.particles[idx+kernel_id_meaning+kernel_id_word].set_color(self._particle_color[(word,meaning)])
                kernel_id_meaning += meaning_num
            kernel_id_word += word_num
        self._get_word_total_fitness(word_meaning_freq_fit)
        self._get_word_meaning(word_meaning_freq_fit)
    
    def _set_particle_color(self,word_meaning_freq_fit):
        word_meaning = [(word,meaning[0]) for word in word_meaning_freq_fit.keys() for meaning in word_meaning_freq_fit[word][1]]
        color = np.linspace(0.0, 1.0, len(word_meaning),endpoint=False)
        self._particle_color = {word_meaning[i]:color[i] for i in range(len(word_meaning))}
        
    def _meaning_to_word(self,word_meaning_freq_fit):
        self._meaning_to_word = {attr[0]:word for word in word_meaning_freq_fit.keys() for attr in \
                                 word_meaning_freq_fit[word][1]}
    
    def _get_word_meaning(self,word_meaning_freq_fit):
        """
        Build a dictionary {word: [[all its meanings],[all fitnesses of meanings]]}
        """
        self._word_meaning_fitness = {word:[[attr[0],attr[2]] for attr in word_meaning_freq_fit[word][1]] for word in \
                                     word_meaning_freq_fit.keys()}
    
    def _get_word_total_fitness(self,word_meaning_freq_fit):
        """
        Build a dictionary {word: total fitness of a word}.
        """
        fitnesses = [sum([attr[2] for attr in word_meaning_freq_fit[key][1]]) for key in word_meaning_freq_fit.keys()]
        self._word_total_fitness = {key:total_fitness for key in word_meaning_freq_fit.keys() for total_fitness in fitnesses}
        
    def _random_mutation(self):
        for particle in self.particles:
            word = particle.word_state.word
            particle.word_state.mutation(self._word_total_fitness[word],self._word_meaning_fitness[word])
            meaning = particle.word_state.meaning
            particle.set_color(self._particle_color[(word,meaning)])
            
    def _collide(self,thres):
        collision = np.zeros(0,dtype=object)
        for id1 in self.particles:
            for id2 in self.particles:
                if id1==id2:
                    continue
                if (id1.lon-id2.lon)**2+(id1.lat-id2.lat)**2 < thres**2:
                    collision = np.append(collision,id2)
        collision = np.unique(collision)
        return collision

    def _decay_prob(self):
        for particle in self.particles:
            if particle.word_state.prob > self._prob_lower_bound+1e-3:
                particle.word_state.prob -= self._prob_decay_rate
            
    def count_states(self):
        meaning_states = {}
        
        for idx in self.particles:
            st = idx.word_state
            if ('--'.join([st.word,st.meaning]),'active') in meaning_states:
                meaning_states[('--'.join([st.word,st.meaning]),'active')] += 1
                meaning_states[('--'.join([st.word,st.meaning]),'total')] += 1
            elif ('--'.join([st.word,st.meaning]),'inactive') in meaning_states:
                meaning_states[('--'.join([st.word,st.meaning]),'inactive')] += 1
                meaning_states[('--'.join([st.word,st.meaning]),'total')] += 1
            else:
                if st.status == 'A':
                    meaning_states[('--'.join([st.word,st.meaning]),'active')] = 1
                else:
                    meaning_states[('--'.join([st.word,st.meaning]),'inactive')] = 1
                meaning_states[('--'.join([st.word,st.meaning]),'total')] = 1
        return meaning_states
        
    
    def execute(self, collision_thres=0.0001, mutation_period=5, pyfunc=self_AdvectionRK4, endtime=None, runtime=None, dt=1.,
                moviedt=None, recovery=None, output_file=None, movie_background_field=None):
        """Overload execute function from parcels.particleset module.
        """
        # check if pyfunc has changed since last compile. If so, recompile
        if self.kernel is None or (self.kernel.pyfunc is not pyfunc and self.kernel is not pyfunc):
            # Generate and store Kernel
            if isinstance(pyfunc, parcels.kernel.Kernel):
                self.kernel = pyfunc
            else:
                self.kernel = self.Kernel(pyfunc)
            # Prepare JIT kernel execution
            if self.ptype.uses_jit:
                self.kernel.remove_lib()
                self.kernel.compile(compiler=GNUCompiler())
                self.kernel.load_lib()

        # Convert all time variables to seconds
        if isinstance(endtime, timedelta):
            raise RuntimeError('endtime must be either a datetime or a double')
        if isinstance(endtime, datetime):
            endtime = np.datetime64(endtime)
        if isinstance(endtime, np.datetime64):
            if not self.time_origin:
                raise NotImplementedError('If fieldset.U.grid.time_origin is not a date, execution endtime must be a double')
            endtime = (endtime - self.time_origin) / np.timedelta64(1, 's')
        if isinstance(runtime, timedelta):
            runtime = runtime.total_seconds()
        if isinstance(dt, timedelta):
            dt = dt.total_seconds()
        outputdt = output_file.outputdt if output_file else np.infty
        if isinstance(outputdt, timedelta):
            outputdt = outputdt.total_seconds()
        if isinstance(moviedt, timedelta):
            moviedt = moviedt.total_seconds()

        assert runtime is None or runtime >= 0, 'runtime must be positive'
        assert outputdt is None or outputdt >= 0, 'outputdt must be positive'
        assert moviedt is None or moviedt >= 0, 'moviedt must be positive'

        # Set particle.time defaults based on sign of dt, if not set at ParticleSet construction
        for p in self:
            if np.isnan(p.time):
                p.time = self.fieldset.U.grid.time[0] if dt >= 0 else self.fieldset.U.grid.time[-1]

        # Derive _starttime and endtime from arguments or fieldset defaults
        if runtime is not None and endtime is not None:
            raise RuntimeError('Only one of (endtime, runtime) can be specified')
        _starttime = min([p.time for p in self]) if dt >= 0 else max([p.time for p in self])
        if self.repeatdt is not None and self.repeat_starttime is None:
            self.repeat_starttime = _starttime
        if runtime is not None:
            endtime = _starttime + runtime * np.sign(dt)
        elif endtime is None:
            endtime = self.fieldset.U.grid.time[-1] if dt >= 0 else self.fieldset.U.grid.time[0]

        if abs(endtime-_starttime) < 1e-5 or dt == 0 or runtime == 0:
            dt = 0
            runtime = 0
            endtime = _starttime
            logger.warning_once("dt or runtime are zero, or endtime is equal to Particle.time. "
                                "The kernels will be executed once, without incrementing time")

        # Initialise particle timestepping
        for p in self:
            p.dt = dt

        # First write output_file, because particles could have been added
        if output_file:
            output_file.write(self, _starttime)
        if moviedt:
            self.show(field=movie_background_field, show_time=_starttime)

        if moviedt is None:
            moviedt = np.infty
        time = _starttime
        if self.repeatdt:
            next_prelease = self.repeat_starttime + (abs(time - self.repeat_starttime) // self.repeatdt + 1) * self.repeatdt * np.sign(dt)
        else:
            next_prelease = np.infty if dt > 0 else - np.infty
        next_output = time + outputdt if dt > 0 else time - outputdt
        next_movie = time + moviedt if dt > 0 else time - moviedt
        next_input = self.fieldset.computeTimeChunk(time, np.sign(dt))

        tol = 1e-12
        
        plot_data = []
        intervals = np.array([],dtype=np.float64)
        mutation_time = 0 
        while (time < endtime and dt > 0) or (time > endtime and dt < 0) or dt == 0:
            
            if dt > 0:
                time = min(next_prelease, next_input, next_output, next_movie, endtime)
            else:
                time = max(next_prelease, next_input, next_output, next_movie, endtime)
            self.kernel.execute(self, endtime=time, dt=dt, recovery=recovery, output_file=output_file)
            if abs(time-next_prelease) < tol:
                pset_new = ParticleSet(fieldset=self.fieldset, time=time, lon=self.repeatlon,
                                       lat=self.repeatlat, depth=self.repeatdepth,
                                       pclass=self.repeatpclass)
                for p in pset_new:
                    p.dt = dt
                self.add(pset_new)
                next_prelease += self.repeatdt * np.sign(dt)
            if abs(time-next_output) < tol:
                if output_file:
                    output_file.write(self, time)
                next_output += outputdt * np.sign(dt)
            if abs(time-next_movie) < tol:
                self.show(field=movie_background_field, show_time=time)
                next_movie += moviedt * np.sign(dt)
            next_input = self.fieldset.computeTimeChunk(time, dt)
            if dt == 0:
                break
            
            
            
            ## Mutation with period mutation_period
            mutation_time += 1
            if mutation_time % mutation_period == 0:
                self._random_mutation()
            ## Check if collsion conditions are met
            collision = self._collide(collision_thres)
            for cols in collision:
                cols.word_state.transition()
            ## Decrease FSM transforming probability according to decay rate
            self._decay_prob()
            ## Count the amounts of word_meaning kernels that are in different states
            meaning_states = self.count_states()
            tot_counts = len(self.particles)
            for key in meaning_states.keys():
                meaning_states[key] = float(meaning_states[key])/tot_counts
            plot_data.append(meaning_states)
            intervals = np.append(intervals,time)
            
        if output_file:
            output_file.write(self, time)

        ## Return word_meaning data in the form of pandas.DataFrame
        df =pd.DataFrame(plot_data)
        df.insert(0,'time',[str(i) for i in intervals])
        return df
