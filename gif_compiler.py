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

def addSticker(background, stickerID):
    foreground = Image.open('stickers/'+str(stickerID)+'.png')
    background.paste(foreground, (0, 0), foreground)
    return background

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

def generateGif(genNumber, numFrames, postProcess='', numStickers=0):
    global style_image
    images=[]
    padding=0.1
    midway = int(numFrames/3)
    for i in range(midway, numFrames):
        images.append(getImage('images/'+str(genNumber)+'/'+str(i+1)+'.png', postProcess))
    for i in range(1, midway):
        images.append(getImage('images/'+str(genNumber)+'/'+str(i+1)+'.png', postProcess))
    if numStickers > 0:
        prevIDs = []
        totalStickers = 4
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
