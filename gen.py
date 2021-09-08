from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import os, sys
from panda3d.core import loadPrcFileData, LineSegs, NodePath, MeshDrawer, AntialiasAttrib,PNMImage
import numpy as np
from random import random, randint
import imageio
from panda3d.core import loadPrcFileData

class Snake():
    def __init__(self, start_angles=[0,0,0,0],
    angleSpeeds=[1,1,1,1], lengths=[10,10,10], color=(1,1,1)):
        self.color = color
        self.angles = np.deg2rad(start_angles)
        self.angleSpeeds = np.deg2rad(angleSpeeds)
        self.l = lengths
        #self.speed = speed

    def getColor(self):
        return self.color

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
    def __init__(self, maxGens, maxFrames):
        ShowBase.__init__(self)
        self.maxGens = maxGens
        self.maxFrames = maxFrames

        self.genNumber = -1
        self.nodes = []
        self.snakes = []
        self.images = []
        self.cameraSpinSpeed = 0
        self.currentNode = None
        self.frameNumber = 0
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.newGeneration()

    def newGeneration(self):
        self.genNumber += 1
        #reset
        self.currentNode = None
        self.frameNumber = 0
        for n in self.nodes:
            n.removeNode()
        self.nodes = []
        self.snakes = []
        self.images = []

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
        modelSize = random()+1 #3
        numNodes = randint(100,200) #4
        backgroundColor = (0,0,0) #5
        if random() > 0.4:
            transparency = True #6
        else:
            transparency = False
        #if numSnakes == 2 and random() > 0.2:
        if random() > 0.5:
            mirror = True #7
        else:
            mirror = False
        specialCaseSeed = random()
        if specialCaseSeed > 0.85:
            specialCase = 1
        elif specialCaseSeed > 0.75:
            specialCase = 2
        else:
            specialCase = 0

        spinSeed = random()
        if spinSeed > 0.9:
            spinSpeed = 1000
        elif spinSeed > 0.5:
            spinSpeed = 65
        elif spinSeed > 0.1:
            spinSpeed = 10
        else:
            spinSpeed = 0
            #none, zebra, multi
        #color type
        #gradients
        #shrinking
        #specialCases (zebra, rainbow, cotton_candy, leapord)
        prop=[numSnakes,speedRange,lengthRange,modelSize,numNodes,backgroundColor,
            transparency, mirror, specialCase, spinSpeed]
        self.startSnakes(prop)
        tempDir = os.path.join(os.getcwd(), r'images')
        saveDir = os.path.join(tempDir, str(self.genNumber))
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)

    def startSnakes(self, prop):
        self.prop = prop

        totalLength = 45
        base.setBackgroundColor(prop[5][0],prop[5][1],prop[5][2])
        angleRange = (0, 360)
        self.numSnakes = prop[0]
        speedRange = prop[1]
        lengthRange = prop[2]
        self.modelSize = prop[3]
        self.numNodes = prop[4]
        self.transparency = prop[6]
        self.mirror = prop[7]
        self.specialCase = prop[8]
        self.cameraSpinSpeed = prop[9]

        for i in range(self.numSnakes):
            startAngles=[]
            startSpeeds=[]
            startLengths=[]
            for j in range(4):
                startAngles.append(random()*(angleRange[1]-angleRange[0])+angleRange[0])
            for j in range(4):
                startSpeeds.append(random()*(speedRange[1]-speedRange[0])+speedRange[0])
            for j in range(2):
                startLengths.append(random()*(lengthRange[1]-lengthRange[0])+lengthRange[0])
            startLengths.append(totalLength - (startLengths[0]+startLengths[1]))
            color = (random(), random(), random())
            self.snakes.append(Snake(startAngles,startSpeeds,startLengths,color))
        self.taskMgr.add(self.updateSnakes, "UpdateSnakes")

    def renderToPNM(self):
        base.graphicsEngine.renderFrame()
        image = PNMImage()
        dr = base.camNode.getDisplayRegion(0)
        dr.getScreenshot(image)
        return image

    # def exportGif(self):
    #     imageio.mimsave('images/movie.gif', img_as_uint(self.images))

    def specialColor(self):
        if self.specialCase == 1:
            if self.frameNumber%6 == 0:
                return (0.9,0,0)
            elif self.frameNumber%5 == 0:
                return (0.9,0.4,0.00)
            elif self.frameNumber%4 == 0:
                return (0.95,0.9,0.05)
            elif self.frameNumber%3 == 0:
                return (0.2,0.95,0.2)
            elif self.frameNumber%2 == 0:
                return (0.2,0.2,0.95)
            else:
                return (.55,.2,1)
            #return (random(),random(),random())
        elif self.specialCase == 2:
            if self.frameNumber%2 == 0:
                return (0.05,0.05,0.05)
            else:
                return (1,1,1)

    def updateSnakes(self, task):
        for s in range(len(self.snakes)):
            if len(self.nodes)>self.numNodes-1:
                self.nodes[0].removeNode()
                self.nodes.pop(0)
            if self.mirror and s == 1:
                mirrorPos = self.snakes[0].getHeadPosition()
                newPosition = (-mirrorPos[0], -mirrorPos[1], -mirrorPos[2])
            else:
                newPosition = self.snakes[s].nextFrame()
            newNode = loader.loadModel("\\models\\Icosahedron.egg")
            #new_position = (-new_position[0], -new_position[1], -new_position[2])
            newNode.setPos(newPosition)
            if self.specialCase == 0:
                nodeColor = self.snakes[s].getColor()
            else:
                nodeColor = self.specialColor()
            newNode.setColor(nodeColor[0],nodeColor[1],nodeColor[2])

            newNode.setTransparency(self.transparency)
            newNode.reparentTo(self.render)
            self.nodes.append(newNode)
            for i in range(len(self.nodes)):
                self.nodes[i].setScale(self.modelSize*i/len(self.nodes),self.modelSize*i/len(self.nodes),self.modelSize*i/len(self.nodes))
                self.nodes[i].setAlphaScale(i/len(self.nodes))
        #print(self.saveDir+'\\'+str(self.frameNumber)+'.png')
        if 0 < self.frameNumber < self.maxFrames+1:
            self.renderToPNM().write('images/'+str(self.genNumber)+'/'+str(self.frameNumber)+'.png')
        self.frameNumber += 1
        if self.frameNumber > self.maxFrames and self.genNumber < self.maxGens-1:
            self.newGeneration()
            return Task.done
        else:
            return Task.cont

	# Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * self.cameraSpinSpeed
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(200 * sin(angleRadians), -200 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

loadPrcFileData('', 'win-size 400 400')
app = App(100, 200)
app.run()
