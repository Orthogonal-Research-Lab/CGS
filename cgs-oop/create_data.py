import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
import sys
import pickle
import random
import argparse
from skimage.feature import canny
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def create_data(pixels):
# function creates dataset
# parameters-
# pixels: integer for number of MxM pixels the pictures will be

    list_of_training_data = []

    # creating rectangles and circles
    for i in range(0,pixels):
        im_rect = Image.new("1", (pixels,pixels))
        draw_rect = ImageDraw.Draw(im_rect)
        im_circle = Image.new("1", (pixels,pixels))
        draw_circle = ImageDraw.Draw(im_circle)
        im_hex = Image.new("1",(pixels,pixels))
        draw_hex = ImageDraw.Draw(im_hex)

        im_oct = Image.new("1",(pixels,pixels))
        draw_oct = ImageDraw.Draw(im_oct)

        for j in range(i, pixels):
            for x in range(i,pixels - i):
                for y in range(j,pixels -j):
                    if i > 3 and j > 3:
                        draw_rect.rectangle(((i,j),(x+i,y+j)), fill= "white")
                        draw_circle.ellipse(((i,j),(x+i,y+j)), fill= "white")
                        if( j-1 > y-j):
                            draw_hex.polygon([(i,j),(i+x,y-j),(i+x+x,y-j),(i+(3*x),j),(i+x+x,y+j),(i+x,y+j)], fill="white")
                            pix_hex = numpy.array(im_hex)
                            edges_hex = canny(pix_hex)
                            list_of_training_data.append((edges_hex,'Hexagon',random.random()))

                        h = abs(j-y)
                        if(j != y-j and h >2 and h-(y-h) >= 0):
                            draw_oct.polygon([(x,y),(x,h),(i+x,h-(y-h)),(x+i+i,h-(y-h)), (x+(3*i),h),(x+(3*i),y),(x+i+i,y+j),(i+x,y+j)], fill="white")
                            pix_oct = numpy.array(im_oct)
                            edges_oct = canny(pix_oct)
                            list_of_training_data.append((edges_oct,'Octagon',random.random()))

                        pix_rect = numpy.array(im_rect)
                        pix_circle = numpy.array(im_circle)

                        # algorithm to extract edges from picture
                        edges_rect = canny(pix_rect)
                        edges_circle = canny(pix_circle)

                        list_of_training_data.append((edges_rect,'Rectangle',random.random()))
                        list_of_training_data.append((edges_circle,'Circle',random.random()))

    return list_of_training_data

# print("({0},{1}),({2},{3}),({4},{5}),({6},{7}),({8},{9}),({10},{11}),({12},{13}),({14},{15})".format(x,y , x,h, i+x,h-(y-h), x+i+i,h-(y-h), x+(3*i),h ,x+(3*i),y, x+i+i,y+j, i+x,y+j))
# print("({0},{1}),({2},{3}),({4},{5}),({6},{7}),({8},{9}),({10},{11})".format(i,j,i+x,y-j,i+x+x,y-j,i+(3*x),j,i+x+x,y+j,i+x,y+j))

def benchmark_data(plot_data,key):
    
    fig = plt.figure()
    N=100
    ax = fig.add_subplot(1, 1, 1)
    data  = np.random.random((N, 7))

    x =[key[data_point[1]] for data_point in plot_data]
    y =[data_point[2] for data_point in plot_data]
    x_vals = ["Circle","Octagon","Hexagon","Rectangle"]

    points = data[:,2:4]
    # color is the length of each vector in `points` color = np.sqrt((points**2).sum(axis = 1))/np.sqrt(2.0)
    color = np.sqrt((points**2).sum(axis = 1))/np.sqrt(2.0)
    rgb = plt.get_cmap('summer')(color)

    plt.xticks([0,0.4,0.6,1.0],x_vals)
    plt.xlabel("Polygon")
    plt.ylabel("RGB Color Value")
    ax.scatter(x, y, color = rgb)

    plt.show()

if __name__=='__main__':

    # optional pixels argument
    script_start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('pixels', nargs='?', default=15)
    arg = parser.parse_args()

    dataset = create_data(int(arg.pixels))
 
    with open('data.pickle','wb') as f:
        pickle.dump(dataset,f)

    key = {"Circle":0, "Octagon":0.4,"Hexagon":0.6,"Rectangle":1}

    benchmark_data(dataset,key)

print("script finished in {} seconds".format(time.time() - script_start))
