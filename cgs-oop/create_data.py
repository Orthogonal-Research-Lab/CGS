import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
import numpy
import sys
import pickle
import argparse
from skimage.feature import canny


def create_data(pixels):

    list_of_training_data = []

    for i in range(0,pixels):
        im = Image.new("1", (pixels,pixels))
        draw = ImageDraw.Draw(im)
        for j in range(i, pixels):
            for x in range(i,pixels - i):
                for y in range(j,pixels -j):
                    if i > 3 and j > 3:
                        draw.rectangle(((i,j),(x+i,y+j)), fill= "white")
                        pix = numpy.array(im)
                        edges2 = canny(pix)
                        list_of_training_data.append((edges2,'Rectangle'))

    for i in range(0,pixels):
        im = Image.new("1", (pixels,pixels))
        draw = ImageDraw.Draw(im)
        for j in range(i, pixels):
            for x in range(i,pixels - i):
                for y in range(j,pixels -j):
                    if i > 3 and j > 3:
                        draw.ellipse(((i,j),(x+i,y+j)), fill= "white")
                        pix = numpy.array(im)
                        edges2 = canny(pix)
                        list_of_training_data.append((edges2,'Circle'))

    return list_of_training_data

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('pixels', nargs='?', default=15)
    arg = parser.parse_args()

    dataset = create_data(arg.pixels)

    with open('data.pickle','wb') as f:
        pickle.dump(dataset,f)
