import imageio
from math import acos
from numpy import ceil
from shutil import rmtree
from random import randint
import os
from PIL import Image

def addSticker(background, stickerID):
    foreground = Image.open('stickers/'+str(stickerID)+'.png')
    background.paste(foreground, (0, 0), foreground)
    return background

def generateGif(genNumber, numFrames, numStickers=0):
    images=[]
    padding=0.1
    midway = int(numFrames/2)
    for i in range(midway, numFrames):
        images.append(Image.open('images/'+str(genNumber)+'/'+str(i+1)+'.png').convert('RGBA'))
    for i in range(numFrames, midway, -1):
        images.append(Image.open('images/'+str(genNumber)+'/'+str(i)+'.png').convert('RGBA'))
    for i in range(midway, 2, -1):
        images.append(Image.open('images/'+str(genNumber)+'/'+str(i)+'.png').convert('RGBA'))
    for i in range(2, midway):
        images.append(Image.open('images/'+str(genNumber)+'/'+str(i+1)+'.png').convert('RGBA'))
    if numStickers > 0:
        prevIDs = []
        totalStickers = 5
        for i in range(numStickers):
            stickerID = randint(0,totalStickers-1)
            if len(prevIDs) > 0:
                while (stickerID in prevIDs):
                    stickerID = randint(0,totalStickers-1)
            prevIDs.append(stickerID)
            for i in range(len(images)):
                images[i] = addSticker(images[i], stickerID)
    images[0].save('output/'+str(genNumber)+'.gif',
        save_all=True, append_images=images[1:], optimize=False, duration=20, loop=0)
    tempDir = os.path.join(os.getcwd(), r'images')
    saveDir = os.path.join(tempDir, str(genNumber))
    rmtree(saveDir)
#
# for i in range(0,10):
#     generateGif(i, 200)
