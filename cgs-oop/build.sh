#!/bin/bash


blender=/Applications/Blender/blender.app/Contents/MacOS/blender

$blender -b oop-blender-demo.blend -P model.py -- $1
$blender -b oop-blender-demo.blend -a
