import bpy
from random import random, uniform,randint
import mathutils
from subprocess import Popen, PIPE, run
from mathutils import Vector
import math
import sys
import time
import io
import importlib
import os


class graphics_factory(object):
    
    # this method creates everything to be displayed
    # meant as abstraction layer between user and creation of objects
    @staticmethod
    def create(tuples,num_of_cultures,tuple_names):

    # function that takes care of creating graphics
    # parameters - 
    # tuples: integer of tuple amount specified by user
    # num_of_cultures: number of cultures user wants to see in simulation
    # tuple_names: name of tuples 
        culture_list=[]
        
        if(tuples == 2):
            shape = "Rectangle" 
        elif(tuples==3):
            shape = "Triangle"
        elif(tuples == 4):
            shape = "Square"
        elif(tuples == 5):
            shape = "Cone"
        elif(tuples == 8):
            shape = "Cube"

        lamp = graphics_factory.create_lamp("Lampika",shape)
        cam = graphics_factory.create_camera("Kamerka",shape)
        if(shape=="Square" or shape=="Cube" or shape=="Cone"):
            radius = 2.0
        else:
            radius = 0.7
        kernel = graphics_factory.create_kernel("kernel",radius,shape)
        for i in range(0,num_of_cultures):
            culture_list.append(graphics_factory.create_culture("culture_{}".format(i),(0,0,0),shape))
        graphics_factory.create_text(shape,tuple_names)
        
        return lamp,cam,kernel,culture_list
        
    @staticmethod
    def create_culture(name,origin,shape):
    # function creates cultures specified by user
    # parameters-
    # name: name of cultures used by blender to keep track of objects
    # origin: coordinate where culture starts in simulation
    # shape: string that determines what type of polygon culture will be
        
        if(shape=="Rectangle"):
            make_rectangle(0.2,origin)
        else:
            make_circle(0.2,origin)
     
        culture = bpy.context.object
        culture.name = name
        culture.show_name = True
        data = culture.data
        data.name = name+'Mesh'
        mat = bpy.data.materials.new("some")
        #randomizes colors
        mat.diffuse_color = (random(),random(),random())
        

        culture.active_material = mat
        culture.scale = (1.2, 0.2, 0)
        
        return culture

    @staticmethod
    def create_camera(name,shape):
    # function creates camera object that user views simulation from
    # parameters-
    # name: name of camera used by blender
    # shape: string to abstract knowledge of other objects away from camera
        
        cam_data = bpy.data.cameras.new(name="cam")  
        cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
        scene.objects.link(cam_ob)
        cam_ob.rotation_euler = (0,0,0)  
        cam = bpy.data.cameras[cam_data.name]  
        cam.lens = 10
        #camera changes depending on tuples, do we want more than one camera?
        if(shape=="Rectangle" or shape=="Square"):
            cam_ob.location = (0,0,3.5)
        elif(shape=="Triangle"):
            cam_ob.location = (2,3,4.5)
        elif(shape=="Cone"):
            cam_ob.location = (0,-1.5,2.8)
            cam_ob.rotation_euler = (math.radians(30),0,math.radians(10))
        elif(shape=="Cube"):
            cam_ob.location = (2,-3.5,4)
            cam_ob.rotation_euler = (math.radians(45), 0.0, math.radians(30))

        return cam_ob
    @staticmethod
    def create_lamp(name,shape):
    # function creates lamp object that user views simulation from
    # parameters-
    # name: name of lamp object used by blender
    # shape: string to abstract knowledge of other objects away from camera
        data = bpy.data.lamps.new(name="lampa", type='POINT')  
        lamp = bpy.data.objects.new(name=name, object_data=data)  
        scene.objects.link(lamp)
        if(shape=="Rectangle" or shape=="Square"):
            lamp.location = (1,0,4.5)
        elif(shape=="Triangle"):
            lamp.location = (4,5,4.5)
        elif(shape=="Cone"):
            lamp.location =(0,0,5)
        elif(shape=="Cube"):
            lamp.location = (6,6,6)
        return lamp

    @staticmethod
    def create_kernel(name,radius,shape):
    # function creates kernel
    # parameters-
    # name: name of kernel used by blender
    # shape: string to abstract knowledge of other objects away from kernel
    # radius: integer radius of kernel
        origin = (0,0,0)
        if(shape=="Rectangle"):
            make_rectangle(radius,origin)
            kernel = bpy.context.object
            kernel.scale = (0.33, 3, 0)
        elif(shape=="Triangle"):
            kernel = make_triangle(origin)
        elif(shape=="Square"):
            kernel = make_square(radius,origin)
            kernel = bpy.context.object
        elif(shape=="Cone"):
            origin =(0,0,1)
            kernel = make_cone(radius,origin)
            kernel = bpy.context.object
        elif(shape=="Cube"):
            kernel = make_cube(radius,origin)
            kernel = bpy.context.object
            

        kernel.name = name
        kernel.show_name = True
        data = kernel.data
        data.name = name+'Mesh'
        mat = bpy.data.materials.new("kernel_color")
        mat.diffuse_color = (1,1,1)
        if(shape == "Cube" or shape == "Cone"):
            # in case kernel is 3-d make it more transparent
            mat.diffuse_color = (1,0,0)
            mat.use_transparency = True
            mat.transparency_method = 'Z_TRANSPARENCY'
            mat.alpha = 0.3
        kernel.active_material = mat
        
        return kernel
    
    @staticmethod
    def create_text(shape,names=None):
    # function creates text for all objects
    # parameters-
    # name: list of names given by user
    # shape: string to abstract knowledge of other objects away from text
        mat = bpy.data.materials.new("text_color")
        mat.diffuse_color = (0,0,0)
        
        if(shape=="Rectangle"):
            bpy.ops.object.text_add(location=(-1,2.3,0))
            ob = bpy.context.object
            ob.data.body = names[0]
            ob.active_material = mat
        
            bpy.ops.object.text_add(location=(-1,-3,0))
            ob = bpy.context.object
            ob.data.body = names[1]
            ob.active_material = mat
                
        elif(shape=="Triangle"):
            bpy.ops.object.text_add(location=(0,-1,0))
            ob = bpy.context.object
            ob.data.body = names[0]
            ob.active_material = mat
            
            bpy.ops.object.text_add(location = (2.5,5,0))
            ob = bpy.context.object
            ob.data.body = names[1]
            ob.active_material = mat
            
            bpy.ops.object.text_add(location = (5,-1,0))
            ob = bpy.context.object
            ob.data.body = names[2]
            ob.active_material = mat
                
        elif(shape=="Square"):
            vertices = [(-2.5,2.3,0),(-2.5,-3,0),(1.5,-3,0),(1.5,2.3,0)]
            
            for i in range(0,4):
                bpy.ops.object.text_add(location=vertices[i])
                ob = bpy.context.object
                ob.data.body = names[i]
                ob.active_material = mat
                
        elif(shape=="Cone"):
            vertices = [(0,0,2.1),(1.6,-.3,0),(-.4,2.4,0),(-1,-2,0),(-3,0,0)]
            for i in range(0,5):
                bpy.ops.object.text_add(location = vertices[i])
                ob = bpy.context.object
                ob.data.body = names[i]
                ob.active_material = mat      
                                
        elif(shape=="Cube"):
            
            vertices = [(-2.5,2.3,1),(-2.5,-2.3,1),(1.5,-2.3,1),(1.5,2.3,1),(-2.5,2.3,0),(-2.5,-2.3,0),(1.5,2.3,0),(1.5,-2.3,0)]
                   
            for i in range(0,8):
                bpy.ops.object.text_add(location = vertices[i])
                ob = bpy.context.object
                ob.data.body = names[i]
                ob.active_material = mat            
            
def make_rectangle(radius,origin):
    # helper function that creates rectangles
    # parameters-
    # radius: radius of rectangle to be made
    # origin: where rectangle will be placed

    bpy.ops.mesh.primitive_plane_add(
    radius = radius,
    location= origin, 
    rotation=(0, 0, 0))
        
def make_square(radius,origin):
    # helper function that creates squares
    # parameters-
    # radius: radius of squares to be made
    # origin: where squares will be placed
    bpy.ops.mesh.primitive_plane_add(
    radius = radius,
    location = origin,
    rotation = (0,0,0))
        
def make_circle(radius,origin):
    # helper function that creates circle
    # parameters-
    # radius: radius of circle to be made
    # origin: where circle will be placed
    bpy.ops.mesh.primitive_circle_add(
        radius = radius,
        location = (0,1,1),
        fill_type = "TRIFAN")

def make_triangle(origin):
    # helper function that creates triangle
    # parameters-
    # origin: where triangle will be placed
    vert = [(0,0,0),(5,0,0),(2.5,5,0)]
    face = [(0,1,2)]
    edge = [(0,1),(1,2),(2,0)]
    
    my_mesh = bpy.data.meshes.new("Triangle")
    ob = bpy.data.objects.new("Triangle",my_mesh)
    
    ob.location = origin
    bpy.context.scene.objects.link(ob)
    
    my_mesh.from_pydata(vert,[],face)
    my_mesh.update(calc_edges=True)
    
    return ob

def make_cube(radius,origin):
    # helper function that creates cube
    # parameters-
    # radius: radius of cube to be made
    # origin: where cube will be placed
    bpy.ops.mesh.primitive_cube_add(location=origin)
    
def make_cone(radius,origin):
    # helper function that creates cone
    # parameters-
    # radius: radius of cone to be made
    # origin: where cone will be placed
    bpy.ops.mesh.primitive_cone_add(
        vertices=4, 
        radius1=radius,
        location=origin)

def get_slope(vertex1,vertex2):
    # calculates slope
    return (vertex2[1]-vertex1[1])/(vertex2[0]-vertex1[0])
    
def get_triangle_constraints(vertices):
    # calculates where points can go based on kernel outline
    # parameters-
    # vertices of triangle

    a = get_slope(vertices[0],vertices[2])
    b = get_slope(vertices[2],vertices[1])

    y = 100
    x = 1
    while y > a * x or y > (b*x)+ 10:
        y = uniform(0,5.0)
        x = uniform(0,5.0)

    return (x,y,0)

def clear_screen():
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' or obj.type=='FONT' or obj.type=='CAMERA' or obj.type=='LAMP':
            obj.select = True
        else:
            obj.select = False
    bpy.ops.object.delete()
    
def clear_heirarchy():
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

def parse_file():   
    # function parses input file to determine proper parameters

    f = open("input.txt","r")
    # dir = os.path.dirname(bpy.data.filepath)
    # if not dir in sys.path:
        # sys.path.append(dir )
    # import knn
    # from skimage.feature import canny
    
    num_years = f.readline()
    tuples_def = f.readline()
    trye = tuples_def.split(':')
    tuples_def = ''.join(trye)
    num_cultures = f.readline()
    script = f.readline()
    type_of_ml = f.readline()
    years_per_frame = f.readline()
    
    script = script.split()
    ml = type_of_ml.split()
    tuple_names = [x.strip() for x in tuples_def.split(',')]
    cultures = int(num_cultures.split(' ', 1)[1])
    years = int(num_years.split(' ', 1)[1])
    year_multiple = int(years_per_frame.split(': ',1)[1])
    
    f.close()
    return years,tuple_names,cultures,script, year_multiple, ml

if __name__=="__main__":
    
    # benchmark script total time
    
    script_start = time.time()
    # make sure screen is cleared from last simulation
    clear_screen()
    clear_heirarchy()
    scene = bpy.context.scene

    years,tuple_names,cultures,end_script,years_per_frame,ml = parse_file()
    
    tuples = len(tuple_names)
    script = ["python3", "google-ngrams/getngrams.py"]
    type_of_ml = ["python3"]
    type_of_ml.extend(ml)
    if(end_script[0]!= "None"):
        script.extend(end_script)
        p = Popen(script, stdout=PIPE, bufsize=1, universal_newlines=True)
    
    if ml[0]=='knn.py':
        Popen(["python3", "create_data.py"],stdout=None)
    else:
        type_of_ml.extend([str(years)])
        print(type_of_ml)

    run_ml = Popen(type_of_ml,stdout=PIPE,bufsize=1,universal_newlines=True)

    scene.frame_start = 0
    rounded_year = years - (years % 20)
    scene.frame_end = (rounded_year/years_per_frame)
    
    lamp, cam, kernel, culture_list = graphics_factory.create(tuples,cultures,tuple_names)
    
    positions = []
    
    # random points for modeling purposes, this will change to data later
    for i in range(200):
        if(tuples==2):
            y = uniform(-2.0,2.0)
            positions.append((0,y,0))
        elif(tuples==4):
            x = uniform(-2.0,2.0)
            y = uniform(-2.0,2.0)
            positions.append((x,y,0))
        elif(tuples ==8):
            x = uniform(-0.7,0.7)
            y = uniform(-0.7,0.7)
            z = uniform(-0.7,-0.7)
            positions.append((x,y,z))
        else:
            positions.append(get_triangle_constraints(
                [(0,0,0),(5,0,0),(2.5,5,0)]))


    number_of_frame = 0  
    # makes cultures move around
    while number_of_frame < scene.frame_end:
        
        scene.frame_set(number_of_frame)
        if(tuples==8 or tuples==5):
            # make kernel transparent if 3 dimensional
            kernel.active_material.keyframe_insert(data_path="alpha")
        for culture in culture_list:
            culture.location = positions[randint(0,100)]
            culture.keyframe_insert(data_path="location")

        # move next 10 frames forward - Blender will figure out what to do between this time
        number_of_frame += 5

    # bpy.ops.wm.save_as_mainfile(filepath = '~/Documents/CGS/oop-blender-demo.blend')
    print("script finished in {} seconds".format(time.time() - script_start))

    for line in run_ml.stdout:
        print(line)
# uncomment this if you want to see benchmark graph from n grams data

    # print("opening benchmark graph")
    # for line in p.stdout:
        # if "Data" in line:
            # csv = line.split()
            # csv = csv[-1]
#             
    # csv=csv.replace(".csv",".png")
    # run(["open", csv])
    # print("finished everything in {}".format(time.time() - script_start))

