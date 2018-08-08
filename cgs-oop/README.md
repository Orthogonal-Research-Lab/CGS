# Installation

1. pull git repo
2. if not already installed, download python3.6 and pip
3. run build.sh by typing ./build.sh into terminal - make sure you are in proper directory


# Input Instructions

The Input file has 6 inputs which change the outcome of the simulation. I will go through them line by line

Line 1:
The first line tells you how many years, (and subsequently, how many generations), your simulation will run for

Line 2:
Line 2 is where you input the tuples you want for the simulation

Line 3:
Line 3 is where you input the number of cultures you want in your simulation.

Line 4:

Line 4 is if you want to see the tuples frequency information over time with google n-grams

Line 5:

Line 5 is where you clarify which type of machine learning you want to use. Right now the possibilities include

knn.py
genetic_algorithm.py

which you can see in the repo folder

Line 6:
Line 6 is where you input the number of frames you want to represent each generation during the simulation



# Tutorial:

If the input file looks like this

years: 300
hot, soft, cold
cultures: 5 
Population: 50
None
genetic_algorithm.py
years in each frame (1-20): 2

Line 1 means the simulation will simulate 300 years of time
Line 2 means this simulation will be run with a kernel that has 3 tuples- hot, soft, and cold
Line 3 means that this simulation will contain 5 seperate cultures
Line 4 means that the initial population will be 50 individuals
Line 5 means that google-n-grams will not be run during this simulation
Line 6 means that you will be using a genetic algorithm for this simulation
Line 7 means that each frame in the rendered animation will represent 2 years


# Running Simulation:
To run the simulation you can do one of two things

either
1. type the below line into the command line and hit enter

oop-blender-demo.blend -P model.py

or 

2. open blender
-- open model.py in the text editor in blender
-- run the script


after these steps you should see the generational output in the terminal as well as a csv file displaying all the data in the folder

Now you can run the animation by rendering it in blender. Go to Render--> Render animation. You will now see the animation run.

