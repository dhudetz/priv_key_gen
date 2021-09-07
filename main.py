from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import os, sys
from panda3d.core import loadPrcFileData, LineSegs, NodePath, MeshDrawer, AntialiasAttrib,PNMImage
import numpy as np
from random import random
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
    def __init__(self):
        ShowBase.__init__(self)

        #Set properties
        self.numSnakes = 1
        angleRange = (0, 360)
        speedRange = (-5, 5)
        lengthRange = (10,18)
        self.modelSize = 1.3


        #globalClock.setMode(ClockObject.MLimited)
        #globalClock.setFrameRate(1)

    	#Set background color of scene (dark purple)
        base.setBackgroundColor(1,0,0)
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.updateSnakes, "UpdateSnakes")
        self.nodes = []
        self.numNodes = 150
        self.snakes = []
        self.images = []
        for i in range(self.numSnakes):
            startAngles=[]
            startSpeeds=[]
            startLengths=[]
            for j in range(4):
                startAngles.append(random()*(angleRange[1]-angleRange[0])+angleRange[0])
            for j in range(4):
                startSpeeds.append(random()*(speedRange[1]-speedRange[0])+speedRange[0])
            for j in range(3):
                startLengths.append(random()*(lengthRange[1]-lengthRange[0])+lengthRange[0])
            color = (random(), random(), random())
            self.snakes.append(Snake(startAngles,startSpeeds,startLengths,color))
        self.cameraSpinSpeed = 0
        self.currentNode = None
        self.frameNumber = 0
        #base.movie(namePrefix='frame', duration=10, fps=30, format='png')

    def renderToPNM(self):
        base.graphicsEngine.renderFrame()
        image = PNMImage()
        dr = base.camNode.getDisplayRegion(0)
        dr.getScreenshot(image)
        return image

    # def exportGif(self):
    #     imageio.mimsave('images/movie.gif', img_as_uint(self.images))

    def updateSnakes(self, task):
        self.frameNumber += 1
        #base.movie(namePrefix=str(self.frameNumber), duration=1, fps=1, format='png')

        #self.images.append(self.renderToPNM())
        for s in range(len(self.snakes)):
            if len(self.nodes)>self.numNodes-1:
                self.nodes[0].removeNode()
                self.nodes.pop(0)
            new_position = self.snakes[s].nextFrame()
            new_node = loader.loadModel("\\models\\Icosahedron.egg")
            #new_position = (-new_position[0], -new_position[1], -new_position[2])
            new_node.setPos(new_position)
            color = self.snakes[s].getColor()
            #new_node.setColor(color[0]-(self.frameNumber/150),color[1],color[2])
            new_node.setColor(1,1,1)
            new_node.setTransparency(True)
            new_node.reparentTo(self.render)
            self.nodes.append(new_node)
            for i in range(len(self.nodes)):
                self.nodes[i].setScale(self.modelSize*i/len(self.nodes),self.modelSize*i/len(self.nodes),self.modelSize*i/len(self.nodes))
                self.nodes[i].setAlphaScale(i/len(self.nodes))
        if 1 < self.frameNumber < 360:
            self.renderToPNM().write('images/'+str(self.frameNumber)+'.png')
        return Task.cont

	# Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * self.cameraSpinSpeed
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(200 * sin(angleRadians), -200 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

loadPrcFileData('', 'win-size 400 400')
app = App()
app.run()
