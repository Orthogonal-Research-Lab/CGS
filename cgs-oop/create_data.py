import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
import numpy
import sys
import pickle
import random
import argparse
from skimage.feature import canny
import time


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
                        draw_hex.polygon([(i,j),(i+x,y-j),(i+x+x,y-j),(i+(3*x),j),(i+x+x,y+j),(i+x,y+j)], fill="white")

                        h = abs(j-y)
                        if(j != y-j and h >2 and h-(y-h) >= 0):
                            # print("({0},{1}),({2},{3}),({4},{5}),({6},{7}),({8},{9}),({10},{11}),({12},{13}),({14},{15})".format(x,y , x,h, i+x,h-(y-h), x+i+i,h-(y-h), x+(3*i),h ,x+(3*i),y, x+i+i,y+j, i+x,y+j))
                            draw_oct.polygon([(x,y),(x,h),(i+x,h-(y-h)),(x+i+i,h-(y-h)), (x+(3*i),h),(x+(3*i),y),(x+i+i,y+j),(i+x,y+j)], fill="white")

                        pix_hex = numpy.array(im_hex)
                        pix_rect = numpy.array(im_rect)
                        pix_circle = numpy.array(im_circle)
                        pix_oct = numpy.array(im_oct)

                        # algorithm to extract edges from picture
                        edges_hex = canny(pix_hex)
                        edges_rect = canny(pix_rect)
                        edges_circle = canny(pix_circle)
                        edges_oct = canny(pix_oct)

                        list_of_training_data.append((edges_rect,'Rectangle'))
                        list_of_training_data.append((edges_circle,'Circle'))
                        list_of_training_data.append((edges_hex,'Hexagon'))
                        list_of_training_data.append((edges_oct,'Octagon'))

    return list_of_training_data


# def benchmark_data():

if __name__=='__main__':

    # optional pixels argument
    script_start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('pixels', nargs='?', default=15)
    arg = parser.parse_args()

    dataset = create_data(int(arg.pixels))

    with open('data.pickle','wb') as f:
        pickle.dump(dataset,f)

    print("script finished in {} seconds".format(time.time() - script_start))
