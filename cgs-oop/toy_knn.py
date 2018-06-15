import csv
import random
import math
import matplotlib.pyplot as plt
import operator
from skimage.feature import canny
import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
import numpy
import pickle
import sys

def loadDataset(filename, split, trainingSet=[] , testSet=[]):
    # with open(filename, 'rb') as csvfile:
        # lines = csv.reader(csvfile)
        # dataset = list(lines)
    filed = open('data.pickle','rb')
    list_of_training_data = pickle.load(filed)
    for edges in list_of_training_data:
        # for y in range(4):
            # dataset[x][y] = float(dataset[x][y])
        if random.random() < split:
            trainingSet.append(edges)
        else:
            testSet.append(edges)

def euclideanDistance(instance1, instance2, length):
    distance = 1024
    for x in range(length):
        for y in range(length):
            if(instance1[0][x,y]==instance2[0][x,y]):
                distance -=1
        # distance += pow((instance1[x] - instance2[x]), 2)
# return math.sqrt(distance)
    return distance

def getNeighbors(trainingSet, testInstance, k):
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
    classVotes = {}
    for x in range(len(neighbors)):
            response = neighbors[x][-1]
            if response in classVotes:
                    classVotes[response] += 1
            else:
                    classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
            if testSet[x][-1] == predictions[x]:
                    correct += 1
    return (correct/float(len(testSet))) * 100.0
	
def main():
	# prepare data
    trainingSet=[]
    testSet=[]
    split = 0.67
    loadDataset('data.pickle', split, trainingSet, testSet)
    print('Train set: ' + repr(len(trainingSet)))
    print('Test set: ' + repr(len(testSet)))
    # generate predictions
    predictions = []
    k = 6
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')

main()
