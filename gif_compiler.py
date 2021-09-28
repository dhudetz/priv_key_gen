import imageio
from math import acos
from numpy import ceil
from shutil import rmtree
from random import randint
import os
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image, ImageFilter
from random import randint

class Sticker():
    def __init__(self, stickerID, backgroundSize):
        self.foreground = Image.open('stickers/'+str(stickerID)+'.png')
        self.foregroundSize = self.foreground.size
        self.backgroundSize = backgroundSize
        side = randint(0,3)
        if side == 0:     #TOP
            x = randint(0,self.backgroundSize[0]-self.foregroundSize[0])
            y = 0
        elif side == 1:     #BOTTOM
            x = randint(0,self.backgroundSize[0]-self.foregroundSize[0])
            y = self.backgroundSize[1]-self.foregroundSize[1]
        elif side == 2:     #LEFT
            x = 0
            y = randint(0,self.backgroundSize[1]-self.foregroundSize[1])
        else:     #RIGHT
            x = self.backgroundSize[0]-self.foregroundSize[0]
            y = randint(0,self.backgroundSize[1]-self.foregroundSize[1])
        self.x = x
        self.y = y

    def pasteSticker(self, background):
        background.paste(self.foreground, (self.x, self.y), self.foreground)
        return background

    def jigglePosition(self, strength=1):
        direction = randint(0,10)
        if direction == 0:
            self.x += strength
        elif direction == 1:
            self.x -= strength
        elif direction == 2:
            self.y += strength
        elif direction == 3:
            self.y -= strength



def load_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img

# MAKE SURE TO GIVE CREDIT AND FOLLOW LICENSE: https://creativecommons.org/licenses/by/3.0/
# https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2
styleModel = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
def getImage(path, postProcess):
    global styleModel
    #add postprocessing
    if postProcess == '':
        return Image.open(path).convert('RGBA')
    elif postProcess == 'contour':
        return Image.open(path).convert('RGBA').filter(ImageFilter.CONTOUR)
    else:
        content_image = load_image(path)
        style_image = load_image('neural_style/'+postProcess)
        stylized_image = styleModel(tf.constant(content_image), tf.constant(style_image))[0]
        stylized_image = cv2.cvtColor(np.squeeze(stylized_image)*255, cv2.COLOR_BGR2RGB)
        #stylized_image = np.squeeze(stylized_image)*255
        stylized_image = stylized_image.astype(np.uint8)
        return Image.fromarray(stylized_image)
        #cv2.imwrite(path, cv2.cvtColor(np.squeeze(stylized_image)*255, cv2.COLOR_BGR2RGB))

def generateGif(genNumber, numFrames, prop):
    global style_image
    images=[]
    padding=0.1
    midway = int(numFrames/3)
    for i in range(midway, numFrames):
        images.append(getImage('images/'+str(genNumber)+'/'+str(i+1)+'.png', prop['post_process']))
    for i in range(1, midway):
        images.append(getImage('images/'+str(genNumber)+'/'+str(i+1)+'.png', prop['post_process']))
    if prop['num_stickers'] > 0:
        prevIDs = []
        totalStickers = 6
        for i in range(prop['num_stickers']):
            stickerID = randint(0,totalStickers-1)
            if len(prevIDs) > 0:
                while (stickerID in prevIDs):
                    stickerID = randint(0,totalStickers-1)
            sticker = Sticker(stickerID, images[0].size)
            prevIDs.append(stickerID)
            for i in range(len(images)):
                images[i] = sticker.pasteSticker(images[i])
                sticker.jigglePosition()
    images[0].save('output/'+str(genNumber)+'.gif',
        save_all=True, append_images=images[1:], optimize=False, duration=20, loop=0)
    tempDir = os.path.join(os.getcwd(), r'images')
    saveDir = os.path.join(tempDir, str(genNumber))
    rmtree(saveDir)
