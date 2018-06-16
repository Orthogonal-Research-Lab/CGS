import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
import numpy
import sys
import pickle
import random
import argparse
from skimage.feature import canny


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
        for j in range(i, pixels):
            for x in range(i,pixels - i):
                for y in range(j,pixels -j):
                    if i > 3 and j > 3:

                        if(random.random() < .0001):
                            draw_rect.rectangle(((i,j),(x+i,y+j)), fill= "white")
                            draw_circle.ellipse(((i,j),(x+i,y+j)), fill= "white")

                            pix_rect = numpy.array(im_rect)
                            pix_circle = numpy.array(im_circle)

                            # algorithm to extract edges from picture
                            edges_rect = canny(pix_rect)
                            edges_circle = canny(pix_circle)

                            list_of_training_data.append((edges_rect,'Rectangle'))
                            list_of_training_data.append((edges_circle,'Circle'))
                            if(i%2==0):
                                half = i/2
                                difference = i-half
                                z = half/2
                                draw_hex.polygon([(z/3,i),(z,half),(z*3,half),(i,i),(z*3,i+difference),(z,i+difference)], fill="white")
                                print(z/3,i)
                                pix_hex = numpy.array(im_hex)
                                edges_hex = canny(pix_hex)
                                list_of_training_data.append((edges_hex,'Hexagon'))


    # # hexagons
    # for i in range(0,pixels):
    #     im = Image.new("1", (pixels,pixels))
    #     draw = ImageDraw.Draw(im)
    #     for j in range(i, pixels):
    #         for x in range(i,pixels - i):
    #             for y in range(j,pixels -j):
    #                 if i > 3 and j > 3:
    #                     draw.ellipse(((i,j),(x+i,y+j)), fill= "white")
    #                     pix = numpy.array(im)
    #                     # algorithm to extract edges from picture
    #                     edges2 = canny(pix)
    #                     list_of_training_data.append((edges2,'Circle'))
    # # dodecagons
    # for i in range(0,pixels):
    #     im = Image.new("1", (pixels,pixels))
    #     draw = ImageDraw.Draw(im)
    #     for j in range(i, pixels):
    #         for x in range(i,pixels - i):
    #             for y in range(j,pixels -j):
    #                 if i > 3 and j > 3:
    #                     draw.ellipse(((i,j),(x+i,y+j)), fill= "white")
    #                     pix = numpy.array(im)
    #                     # algorithm to extract edges from picture
    #                     edges2 = canny(pix)
    #                     list_of_training_data.append((edges2,'Circle'))

    return list_of_training_data

if __name__=='__main__':

    # optional pixels argument
    parser = argparse.ArgumentParser()
    parser.add_argument('pixels', nargs='?', default=15)
    arg = parser.parse_args()

    dataset = create_data(int(arg.pixels))

    with open('data.pickle','wb') as f:
        pickle.dump(dataset,f)
