import random
import math
import operator
from skimage.feature import canny
import argparse
import numpy
import pickle
import sys

def loadDataset(filename, split, trainingSet=[] , testSet=[]):
# Function to load dataset and split training and testing data
# parameters-
# filename: name of file where dataset is stored
# split: split between training set and test set
# trainingSet: empty list to be filled with training set
# testSet: empty list to be filled with training set

    filed = open('data.pickle','rb')
    list_of_training_data = pickle.load(filed)
    for edges in list_of_training_data:
        if random.random() < split:
            trainingSet.append(edges)
        else:
            testSet.append(edges)

def euclideanDistance(instance1, instance2, length):
# funtion determines distance between images
# parameters-
# instance1: first picture to be compared- list of tuples (numpy array- pixels, string-shape type)
# instance2: second picture to be compared - list of tuples(numpy array- pixels, string-shape type)
# length: length of numpy array
    distance = 1024
    for x in range(length):
        for y in range(length):
            # comparing pixels from numpy array
            if(instance1[0][x,y]==instance2[0][x,y]):
                distance -=1
    return distance

def getNeighbors(trainingSet, testInstance, k):
# function determines neighbors of test instance
# parameters-
# trainingSet: set of training data
# testInstance: instance you're finding neighbors too
# k: number of neighbors you want
    distances = []
    length = len(testInstance[0])-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
# function determines response of neighbors as to what test instance is classified as
# parameters - 
# neighbors: list of neighbors to testInstance
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getContinuumResponse(neighbors):

    summed = 0
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response == 'Hexagon':
            val = 0.5
        elif response == 'Rectangle':
            val = 1
        else:
            val = -1
        summed += val

    if summed < 0:
        summed = 0
    result = summed/len(neighbors)

    return result

def getAccuracy(testSet, predictions):
#function benchmarks accuracy of knn algo
# parameters - 
# testSet: test data
# predictions: what algorithm predicted
    correct = 0
    for x in range(len(testSet)):
            if testSet[x][-1] == predictions[x]:
                    correct += 1
    return (correct/float(len(testSet))) * 100.0
	
if __name__=='__main__':

    # optional arguments for how many neighbors you want to poll and what test/train split you want
    parser = argparse.ArgumentParser()
    parser.add_argument('continuum', nargs='?', default=False)
    parser.add_argument('k', nargs='?', default=6)
    parser.add_argument('split', nargs='?', default=0.67)
    arg = parser.parse_args()
    print(arg)
    split = float(arg.split)
    k = arg.k

    trainingSet=[]
    testSet=[]

    loadDataset('data.pickle', split, trainingSet, testSet)
    print('Train set: ' + repr(len(trainingSet)))
    print('Test set: ' + repr(len(testSet)))

    # generate predictions
    predictions = []

    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)

        result = getResponse(neighbors)
        if arg.continuum == 'True':
           continuum = getContinuumResponse(neighbors)
           print('> predicted=' +repr(result)+ ', actual=' + repr(testSet[x][-1])+ 'continuum val= ' +repr(continuum)) 
        else:
           print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
        predictions.append(result)

    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')

