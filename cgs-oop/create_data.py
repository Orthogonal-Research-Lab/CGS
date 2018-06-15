import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
import numpy
import sys
import pickle
from skimage.feature import canny

list_of_training_data = []

for i in range(0,20):
    im = Image.new("1", (20,20))
    draw = ImageDraw.Draw(im)
    for j in range(i, 20):
        for x in range(i,20 - i):
            for y in range(j,20 -j):
                if i > 3 and j > 3:
                    draw.rectangle(((i,j),(x+i,y+j)), fill= "white")
                    pix = numpy.array(im)
                    edges2 = canny(pix)
                    list_of_training_data.append((edges2,'Rectangle'))

for i in range(0,20):
    im = Image.new("1", (20,20))
    draw = ImageDraw.Draw(im)
    for j in range(i, 20):
        for x in range(i,20 - i):
            for y in range(j,20 -j):
                if i > 3 and j > 3:
                    draw.ellipse(((i,j),(x+i,y+j)), fill= "white")
                    pix = numpy.array(im)
                    edges2 = canny(pix)
                    list_of_training_data.append((edges2,'Circle'))

with open('data.pickle','wb') as f:
    pickle.dump(list_of_training_data,f)
