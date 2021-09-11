import imageio
from math import acos
from numpy import ceil
from shutil import rmtree
import os
def generateGif(genNumber, numFrames):

    filenames=[]
    padding=0.1
    midway = int(numFrames/2)
    for i in range(midway, numFrames):
        filenames.append('images/'+str(genNumber)+'/'+str(i+1)+'.png')
    for i in range(numFrames, midway, -1):
        filenames.append('images/'+str(genNumber)+'/'+str(i)+'.png')
    for i in range(midway, 2, -1):
        filenames.append('images/'+str(genNumber)+'/'+str(i)+'.png')
    for i in range(2, midway):
        filenames.append('images/'+str(genNumber)+'/'+str(i+1)+'.png')
    with imageio.get_writer('output/'+str(genNumber)+'.gif', mode='I',duration=(1/60)) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    tempDir = os.path.join(os.getcwd(), r'images')
    saveDir = os.path.join(tempDir, str(genNumber))
    rmtree(saveDir)
#
# for i in range(0,10):
#     generateGif(i, 200)
