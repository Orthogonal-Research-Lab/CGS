import random
import math
import operator
from skimage.feature import canny
import argparse
import pickle
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

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
        response = neighbors[x][1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getContinuumResponse(neighbors):
    key = {"Circle":-0.3, "Octagon":0.4,"Hexagon":0.6,"Rectangle":1}

    summed = 0
    for x in range(len(neighbors)):
        response = neighbors[x][1]
        summed += key[response]

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
            if testSet[x][1] == predictions[x]:
                    correct += 1
    return (correct/float(len(testSet))) * 100.0
	
def benchmark_data(plot_data, predictions):

    fig = plt.figure()
    N=100
    ax = fig.add_subplot(1, 1, 1)
    data  = np.random.random((N, 7))

    x = [data_point for data_point in predictions]
    y =[data_point[2] for data_point in plot_data]
    x_vals = ["Circle","Octagon","Hexagon","Rectangle"]

    points = data[:,2:4]
    # color is the length of each vector in `points` color = np.sqrt((points**2).sum(axis = 1))/np.sqrt(2.0)
    color = np.sqrt((points**2).sum(axis = 1))/np.sqrt(2.0)
    rgb = plt.get_cmap('summer')(color)

    plt.xticks([0,0.4,0.6,1.0],x_vals)
    plt.xlabel("Polygon")
    plt.ylabel("RGB Color Value")
    plt.title("Predicted results on continuum")
    ax.scatter(x, y, color = rgb)

    plt.show()

def main(classify=False, k = 6, split = 0.67):

    # optional arguments for how many neighbors you want to poll and what test/train split you want
    # parser = argparse.ArgumentParser()
    # parser.add_argument('k', nargs='?', default=6)
    # parser.add_argument('-c', action='store_true')
    # parser.add_argument('split', nargs='?', default=0.67)
    # arg = parser.parse_args()
    # print(arg)
    # split = float(arg.split)
    # k = arg.k
    # classify = arg.c

    trainingSet=[]
    testSet=[]

    loadDataset('data.pickle', split, trainingSet, testSet)
    print('Train set: ' + repr(len(trainingSet)))
    print('Test set: ' + repr(len(testSet)))

    # generate predictions
    classified_predictions = []
    continuum_predictions = []

    for x in range(len(testSet)):

        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        if classify == False:
            continuum = getContinuumResponse(neighbors)
            print('actual=' + repr(testSet[x][1])+ ', continuum val= ' +repr(continuum)) 
        else:
            print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][1]))

        classified_predictions.append(result)
        continuum_predictions.append(continuum)

    accuracy = getAccuracy(testSet, classified_predictions)
    benchmark_data(testSet,continuum_predictions)
    print('Accuracy: ' + repr(accuracy) + '%')

if __name__ =='__main__':
    main()
