import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
import numpy
import sys
import pickle
from skimage.feature import canny

list_of_training_data = []

for i in range(0,32):
    im = Image.new("1", (32,32))
    draw = ImageDraw.Draw(im)
    for j in range(i, 32):
        for x in range(i,32 - i):
            for y in range(j,32 -j):
                draw.rectangle(((i,j),(x+i,y+j)), fill= "white")
                pix = numpy.array(im)
                edges2 = canny(pix)
                list_of_training_data.append((edges2,'Rectangle'))

for i in range(0,32):
    im = Image.new("1", (32,32))
    draw = ImageDraw.Draw(im)
    for j in range(i, 32):
        for x in range(i,32 - i):
            for y in range(j,32 -j):
                draw.ellipse(((i,j),(x+i,y+j)), fill= "white")
                pix = numpy.array(im)
                edges2 = canny(pix)
                list_of_training_data.append((edges2,'Circle'))

filehandler = open('training.obj',"wb")
pickle.dump(list_of_training_data,filehandler)
filehandler.close()
