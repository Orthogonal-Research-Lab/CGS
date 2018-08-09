# Contextual Geometric Structures (CGS): a hybrid modeling approach
Contextual Geometric Structures using parcels <https://github.com/OceanParcels/parcels>


### Simulation Goals
The goals of this CGS-based project are the following:

1. To simulate how both words and their meanings evolve in a synthetic cultural context.

2. To discover factors that affect changing rates of word usage and meaning in a synthetic culture, using the concept of finite state machines, hydrodynamics, and genetic algorithms.

### Key Concepts

#### Flow field:
This project utilizes particles and an environmental flow field to simulate the diversity of words and meanings in a population. Each particle is associated with a kernel, which contains a single word and a meaning of the word. Particles within the field flow freely, but also tend to collide in a flow-dependent manner.

#### Words:  
In this model, a single word may have many meanings, but a particle represents a single word and meaning pair (word:meaning). There are different mechanisms for words and meanings, respectively. 

For words, a finite state machine (FSM) is implemented to simulate the behavior of word-frequency alteration. The concept is described in Figure 1. Words may be in either 'active' or 'inactive' states. When a word is in an 'active' state, it may transition to an 'inactive' state at a probability of _p_. This active state may also be maintained after a triggering event with a probability of 1-_p_. 

When a word is in an 'inactive' state, it always transforms to the 'active' state after a triggering event. While activation after a triggering event is deterministic, the triggering events themselves (a collision of particles) occur at a rate _q_ (or a conditional probability of 1|_q_), and is dependent on the number of particles in the simulation. 

As the simulation evolves, the active-to-inactive probability (_p_) tends to decrease with time. This is consistent with the idea that words are more likely to disappear when they are young and at low-frequencies in the population. As words persist with respect to time, their frequency is more likely to stabilize as well.

![](/image/word.jpg)
Figure 1. Probabilities of transitions between active and inactive states.

#### Meanings:
In CGS, every word:meaning combination (a single particle) is assigned a fitness value, which is used for the genetic algorithm component. Mutation occurs at a given rate (_u_) and changes the meaning of a word to another meaning of the same word with a probability proportional to the meaning's fitness value. 

We can illustrate this by considering a group of meanings for a single word: if a given meaning has a higher fitness value, the other meanings have higher chances to transform into this meaning upon mutation.

### Installation
This package is currently only available for Windows. Please clone the repository to the Desktop and proceed with the installation:

1. Please create a virtual environment first.  
	
   		$ virtualenv environment_name --python=2.7 --no-site-packages  
		
2. Activate virtual environment.  
	  
		$ cd path_to_environment/Scripts  
    	$ activate
	
3. Then install package with:
	
		$ pip install git+https://github.com/jimboH/CGS.git@master --process-dependency-links

 
