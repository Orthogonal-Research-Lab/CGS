## Google Summer of Code 2018 Report

## Achievements  
This summer, I worked on making a simulation of evolution using the Contextual Geometric Structure (CGS) paradigm. So far, I have created a way to see how words, or inidividuals in a population, evolve to a maximum fitness. The code in this repository is built from scratch. The things I have accomplished so far include:  

### Project Accomplishments
1. a paramaterized visual simulation utilizing the blender rendering engine with an object oriented approach that allows for easy future additions.

2. a KNN algorithm that creates a continuum of images, and determines where on this continuum new members should be placed.

3. a Genetic Algorithm (GA) that determines how many generations it takes for a population to get to a level of "maximum fitness".

4. a dataset of shapes and images to be used for the KNN algorithm. I will upload this to an open source data set community

5. a library that pulls 1 word, multiple words, or creates random words for the user to manipulate. Nothing that has the speed or memory complexity currently exists like this in other python libraries. Will soon upload this to PyPi

6. Creates a file of generation data that shows min,max,std dev,avg of each generations fitness

## Things to be done in the future  

1. Integrate the cultures from the blender simulation with the data from the genetic algorithm


2. Rather than running scripts externally from blender file find a way to import external files as libraries.

3. Extend to windows computers.

4. Extend genetic algorithm to 2,3, etc. tuple representations of a culture
 
