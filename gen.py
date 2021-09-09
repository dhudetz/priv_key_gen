from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import os, sys
from panda3d.core import loadPrcFileData, LineSegs, NodePath, MeshDrawer, AntialiasAttrib,PNMImage
import numpy as np
from random import random, randint
import imageio
from panda3d.core import loadPrcFileData
import gif_compiler

class Snake():
    def __init__(self, start_angles=[0,0,0,0],
    angleSpeeds=[1,1,1,1], lengths=[10,10,10]):
        self.angles = np.deg2rad(start_angles)
        self.angleSpeeds = np.deg2rad(angleSpeeds)
        self.l = lengths
        #self.speed = speed

    def nextFrame(self):
        #update angles
        for t in range(len(self.angles)):
            self.angles[t] += self.angleSpeeds[t]
        return self.getHeadPosition()

    def getHeadPosition(self):
        x=0
        y=0
        z=0
        x_temp=0
        angle_temp=0

        for t in range(1,len(self.angles)):
            angle_temp+=self.angles[t]
            x_temp+=self.l[t-1]*sin(angle_temp)
            z+=self.l[t-1]*cos(angle_temp)
        x=x_temp*cos(self.angles[0])
        y=x_temp*sin(self.angles[0])
        return (x,y,z)


class App(ShowBase):
    def __init__(self, maxGens, maxFrames, saveImages=True, saveGif=False):
        ShowBase.__init__(self)
        self.maxGens = maxGens
        self.maxFrames = maxFrames
        self.saveImages = saveImages
        self.saveGif = saveGif

        self.genNumber = -1
        self.nodes = []
        self.snakes = []
        self.images = []
        self.currentNode = None
        self.frameNumber = 0
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.newGeneration()

    def generateNewProps(self):
        numSeed = random()
        if numSeed > 0.95:
            numSnakes=5 #0
        elif numSeed > 0.85:
            numSnakes=4
        elif numSeed > 0.7:
            numSnakes=3
        elif numSeed >0.4:
            numSnakes=2
        else:
            numSnakes=1
            #if numSnakes > 2, multicolor specialcase could happen
        speedSeed = random()
        if speedSeed > 0.8:
            speedRange = (-100,100) #1
        elif speedSeed > 0.5:
            speedRange = (-15,15) #1
        else:
            speedRange = (-5,5) #1
            #extreme speeds case
        lengthRange = (0,20) #2

        modelSeed = random()
        if modelSeed > 0.95:
            sizeNormalizer = 8
            modelType = 'monkey'
        elif modelSeed > 0.5:
            sizeNormalizer = 2
            modelType = 'Icosahedron'
        else:
            sizeNormalizer = 5
            modelType = 'box'
        sizeSeed = random()
        if sizeSeed > 0.5:
            modelSize = sizeNormalizer
            numNodes = randint(100,200)
        else:
            modelSize = sizeNormalizer*2
            numNodes = randint(50,100)

        if random() > 0.4:
            transparency = True #6
        else:
            transparency = False
        #if numSnakes == 2 and random() > 0.2:
        if random() > 0.5:
            mirror = True #7
        else:
            mirror = False

        #COLORS
        colorSeed = random()
        colors=[]
        if colorSeed > 0.85:
            colors.append((0,0,0))
            colors.append((1,1,1))
            colors.append((0,0,0))
            colors.append((1,1,1))
            colors.append((0,0,0))
            colors.append((1,1,1))
        elif colorSeed > 0.75:
            colors.append((0.9,0,0))
            colors.append((0.9,0.4,0))
            colors.append((0.95,0.9,0.05))
            colors.append((0.2,0.95,0.2))
            colors.append((0.2,0.2,0.95))
            colors.append((.55,.2,1))
            colors.append((0.9,0,0))
            colors.append((0.9,0.4,0))
            colors.append((0.95,0.9,0.05))
            colors.append((0.2,0.95,0.2))
            colors.append((0.2,0.2,0.95))
            colors.append((.55,.2,1))
            colors.append((0.9,0,0))
            colors.append((0.9,0.4,0))
            colors.append((0.95,0.9,0.05))
            colors.append((0.2,0.95,0.2))
            colors.append((0.2,0.2,0.95))
            colors.append((.55,.2,1))
        elif colorSeed > 0.55:
            colors.append((0,0,0))
            colors.append((1,0,0))
            colors.append((0,0,0))
            colors.append((0,0,1))
            colors.append((0,0,0))
            colors.append((0,1,0))
        else:
            colors.append((random(),random(),random()))
            colors.append((random(),random(),random()))

        #SPINNING
        spinSeed = random()
        if spinSeed > 0.95:
            spinSpeed = 200
        elif spinSeed > 0.7:
            spinSpeed = 55
        else:
            spinSpeed = 20
            #none, zebra, multi

        #BACKGROUND
        backgroundSeed = random()
        if backgroundSeed > 0.95:
            backgroundType = 'white'
        elif backgroundSeed > 0.8:
            backgroundType = 'gray_scale'
        elif backgroundSeed > 0.2:
            backgroundType = 'opposite'
        else:
            backgroundType = 'black'

        #color type
        #gradients
        #shrinking
        #specialCases (zebra, rainbow, cotton_candy, leapord), PURE FIRE
        self.prop={
            'num_snakes' : numSnakes,
            'speed_range' : speedRange,
            'model_size' : modelSize,
            'num_nodes' : numNodes,
            'model_type' : modelType,
            'colors' : colors,
            'transparency' : transparency,
            'mirror' : mirror,
            'spin_speed' : spinSpeed,
        }

    def newGeneration(self):
        self.genNumber += 1
        #I like circles.jpg
        self.texture = loader.loadTexture('tex/fuck.png')
        #reset
        self.currentNode = None
        self.frameNumber = 0
        for n in self.nodes:
            n.removeNode()
        self.nodes = []
        self.snakes = []
        self.images = []

        self.generateNewProps()

        #COLOR SECTION
        self.currentColorSection=0
        self.colorSectionSize=np.floor(self.maxFrames/(len(self.prop['colors'])))

        self.startSnakes()
        tempDir = os.path.join(os.getcwd(), r'images')
        saveDir = os.path.join(tempDir, str(self.genNumber))
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)

    def startSnakes(self):

        totalLength = 45
        #base.setBackgroundColor(self.prop['background_color'][0],self.prop['background_color'][1],self.prop['background_color'][2])
        angleRange = (0, 360)
        lengthRange = (0,20) #2

        for i in range(self.prop['num_snakes']):
            startAngles=[]
            startSpeeds=[]
            startLengths=[]
            for j in range(4):
                startAngles.append(random()*(angleRange[1]-angleRange[0])+angleRange[0])
            for j in range(4):
                startSpeeds.append(random()*(self.prop['speed_range'][1]-self.prop['speed_range'][0])+self.prop['speed_range'][0])
            for j in range(2):
                startLengths.append(random()*(lengthRange[1]-lengthRange[0])+lengthRange[0])
            startLengths.append(totalLength - (startLengths[0]+startLengths[1]))
            self.snakes.append(Snake(startAngles,startSpeeds,startLengths))
        self.taskMgr.add(self.updateSnakes, "UpdateSnakes")

    def saveImage(self, file):
        base.screenshot(file, None)

    def updateSnakes(self, task):
        for s in range(len(self.snakes)):
            if len(self.nodes)>self.prop['num_nodes']-1:
                self.nodes[0].removeNode()
                self.nodes.pop(0)
            if self.prop['mirror'] and s == 1:
                mirrorPos = self.snakes[0].getHeadPosition()
                newPosition = (-mirrorPos[0], -mirrorPos[1], -mirrorPos[2])
            else:
                newPosition = self.snakes[s].nextFrame()
            newNode = loader.loadModel('models/'+self.prop['model_type']+'.egg')
            newNode.setTexture(self.texture)
            newNode.setPos(newPosition)
            if (self.frameNumber>(self.colorSectionSize*(self.currentColorSection+1)) and self.currentColorSection != len(self.prop['colors'])-1):
                self.currentColorSection+=1
            if self.currentColorSection < len(self.prop['colors'])-1:
                currentIndex = self.currentColorSection
                nextIndex = self.currentColorSection+1
            else:
                currentIndex = self.currentColorSection
                nextIndex = 0
            colorR = self.prop['colors'][currentIndex][0]+(self.prop['colors'][nextIndex][0]-self.prop['colors'][currentIndex][0])*((self.frameNumber-self.colorSectionSize*self.currentColorSection)/self.colorSectionSize)
            colorG = self.prop['colors'][currentIndex][1]+(self.prop['colors'][nextIndex][1]-self.prop['colors'][currentIndex][1])*((self.frameNumber-self.colorSectionSize*self.currentColorSection)/self.colorSectionSize)
            colorB = self.prop['colors'][currentIndex][2]+(self.prop['colors'][nextIndex][2]-self.prop['colors'][currentIndex][2])*((self.frameNumber-self.colorSectionSize*self.currentColorSection)/self.colorSectionSize)
            nodeColor = (colorR,colorG,colorB)
            base.setBackgroundColor(1-nodeColor[0],1-nodeColor[1],1-nodeColor[2])
            newNode.setColor(nodeColor[0],nodeColor[1],nodeColor[2])

            newNode.setTransparency(self.prop['transparency'])
            newNode.reparentTo(self.render)
            self.nodes.append(newNode)
            for i in range(len(self.nodes)):
                self.nodes[i].setScale(self.prop['model_size']*i/len(self.nodes),
                    self.prop['model_size']*i/len(self.nodes),self.prop['model_size']*i/len(self.nodes))
                self.nodes[i].setAlphaScale(i/len(self.nodes))
#UNDO THIS'
        if self.saveImages and (0 < self.frameNumber < self.maxFrames+1):
            self.saveImage('images/'+str(self.genNumber)+'/'+str(self.frameNumber)+'.png')
            #self.renderToPNM().write('images/'+str(self.genNumber)+'/'+str(self.frameNumber)+'.png')
        self.frameNumber += 1
        if self.frameNumber > self.maxFrames and self.genNumber < self.maxGens-1:
            self.newGeneration()
            if self.saveGif:
                self.taskMgr.add(self.generateGif, "generateGif")
            return Task.done
        else:
            return Task.cont

    def generateGif(self, task):
        gif_compiler.generateGif(self.genNumber-1, self.maxFrames)
        return Task.done

	# Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * self.prop['spin_speed']
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(200 * sin(angleRadians), -200 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

loadPrcFileData('', 'win-size 200 200')
#loadPrcFileData('', 'window-type offscreen')
app = App(100, 400, True, False)
app.run()
