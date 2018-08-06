import random
import time
from create_random_string import get_random_word
import operator

from deap import base
from deap import tools

toolbox = base.Toolbox()
toolbox.register("select", tools.selTournament, tournsize=3)

class Individual():
    def __init__(self,get_my_word,word_or_not):
        #creates an individual 
        #input: get_my_word- function passed in to create individual
        #word_or_not- boolean to decide whether real or word or made up one
        self.fitness=0
        self.fitness_valid = False
        if word_or_not:
            self.word=get_my_word()
        else:
            self.word=get_my_word(False)


    def rep(self,index= -1):
        if index==-1:
            return self.word
        else:
            return self.word[index]

    def set_word(self,new_word):
        self.word=new_word

    def set_fitness(self,fit):
    # set fitness of each individual
        self.fitness=fit
        if fit > 0:
            self.fitness_valid = True
        else:
            self.fitness_valid = False

    def get_fitness(self):
        return self.fitness


class Population():

    def __init__(self,n, weight,real_words = True):
        self.individuals=[]
        for i in range(0,n):
            self.individuals.append(Individual(get_random_word,real_words))

        self.weight = weight

    def selBest(self):
        # selects most fit individual in the population
        sort_by = operator.attrgetter("fitness")
        self.individuals.sort(key=sort_by, reverse = True)
        return self.individuals[0]

class Evolution():
    def __init__(self, weight="hot"):
        self.weight= weight

    def evaluate_fitness(self,ind):
    # evaluate the fitness of each individual in the population
    # input: one individual object
        if(ind.rep()==self.weight):
            return len(ind.rep())+2

        fitness = 0
        tracker = ind.rep()

        if(len(self.weight)==len(ind.rep())):
            fitness+=1
            for i in range(0,len(self.weight)):
                if(self.weight[i]==tracker[i]):
                    fitness+=1.1
                elif(self.weight[i] in tracker):
                    fitness+=1
        else:
            for i in range(0,len(self.weight)):
               if self.weight[i] in tracker:
                   fitness+=1

        return fitness

    def mate(self,parent1,parent2):
    
    # generates children from one generation to the next
    # input: two individual objects
        child1 = ''
        child2 = ''
        child1_length = len(parent1.word)
        child2_length = len(parent2.word)

        for i in range(0,child1_length):
            if (len(parent2.word) > i):
                temp=[parent2.rep(i),parent1.rep(i)]
                child1+=random.choice(temp)
            else:
                child1+=parent1.rep(i)
            
        for i in range(0,child2_length):
            if (len(parent1.word) > i):
                temp=[parent2.rep(i),parent1.rep(i)]
                child2+=random.choice(temp)
            else:
                child2+=parent2.rep(i)

        parent1.set_word(child1)
        parent2.set_word(child2)

    def mutate(self,ind,mut_precentage):
        new_word=''
        for i in range(0,len(ind.rep())):
            if random.random()< mut_precentage:
                new_word = get_random_word(real_word=False,size=1)
            else:
                new_word +=ind.rep(i)

        ind.set_word(new_word)
        
def main():
    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual

    CXPB, MUTPB = 0.5, 0.3
    # Variable keeping track of the number of generations
    g = 0

    tuple1 = "hot"
    pop = Population(20,tuple1)
    evolve = Evolution()


    print("Start of evolution")

    fits = []
    for ind in pop.individuals:
        ind.set_fitness(evolve.evaluate_fitness(ind))
        fits.append(ind.get_fitness())

    print("evaluated {} individuals".format(len(pop.individuals)))
    list_of_generations = []
        
    while max(fits) < len(pop.weight)+2 and g <1000:
        # A new generation
        g = g + 1

        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop.individuals, len(pop.individuals))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]): # every 2 element, and every 2 element starting from index 1

            if random.random() < CXPB:
                evolve.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                child1.set_fitness(0)
                child2.set_fitness(0)

        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                evolve.mutate(mutant,0.3)
                mutant.set_fitness(0)
        # Evaluate the individuals with an invalid fitness

        invalid_ind = [ind for ind in offspring if not ind.fitness_valid]
        fitnesses = list(map(evolve.evaluate_fitness, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.set_fitness(fit)
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop.individuals[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.get_fitness() for ind in pop.individuals]
        
        length = len(pop.individuals)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print(length)
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        this_gens_data = (min(fits),max(fits),mean,std)
        list_of_generations.append(this_gens_data)

    
    print("-- End of (successful) evolution --")
    create_csv(list_of_generations)
    
    best_ind = pop.selBest()
    print("Best individual is %s, %s" % (best_ind.rep(), best_ind.get_fitness()))

def create_csv(gen_data):
# function that creates and fills table with each generations data
# input : gen_data - list of tuples that have min, max, avg, and std dev of each generation from max
    down_dir = "generation_files.csv"
    csv = open(down_dir, "w") 
    columnTitleRow = "min, max, avg, std\n"
    csv.write(columnTitleRow)

    for generation in gen_data:
        column = "{0},{1},{2},{3}\n".format(generation[0],generation[1],generation[2],generation[3])
        csv.write(column)
    csv.close()

if __name__=='__main__':
    main()

