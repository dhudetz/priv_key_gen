import numpy as np
from math import pi, sin, cos
from random import random

class Snake():
    def __init__(self, startAngles,
    angleSpeeds, lengths):
        self.angles = np.deg2rad(startAngles)
        self.angleSpeeds = np.deg2rad(angleSpeeds)
        self.l = lengths

    def nextFrame(self):
        #update angles with angle speeds
        for t in range(len(self.angles)):
            self.angles[t] += self.angleSpeeds[t]
        self.calculateHeadPosition()

    def getHeadPosition(self):
        return self.headPosition

    def calculateHeadPosition(self):
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
        self.headPosition = (x,y,z)

class MasterAnimation():
    def __init__(self, prop):
        self.prop = prop
        self.snakes = []
        self.wireframe = []
        for i in range(prop['num_snakes']):
            snakeProps = self.generateSnakeProps()
            self.snakes.append(Snake(snakeProps[0],snakeProps[1],snakeProps[2]))

    def generateSnakeProps(self):
        totalLength = 46
        angleRange = (0, 360)
        lengthRange = (0,20) #2
        startAngles=[]
        startSpeeds=[]
        startLengths=[]
        for j in range(4):
            startAngles.append(random()*(angleRange[1]-angleRange[0])+angleRange[0])
        for j in range(4):
            # if j == 0:
            #     startSpeeds.append(0)
            # else:
            startSpeeds.append(random()*(self.prop['speed_range'][1]-self.prop['speed_range'][0])+self.prop['speed_range'][0])
        for j in range(2):
            startLengths.append(random()*(lengthRange[1]-lengthRange[0])+lengthRange[0])
        startLengths.append(totalLength - (startLengths[0]+startLengths[1]))
        return (startAngles,startSpeeds,startLengths)

    def clearWireframe(self):
        self.wireframe = []

    def nextFrame(self):
        for s in self.snakes:
            s.nextFrame()
        if self.prop['draw_wireframe']:
            self.calculateWireframe()

    def calculateWireframe(self):
        numSnakes = self.prop['num_snakes']
        self.wireframe = []
        for i in range(numSnakes-1):
            for j in range(i+1, numSnakes):
                self.wireframe.append((self.snakes[i].getHeadPosition(), self.snakes[j].getHeadPosition()))

    def getWireframe(self):
        if self.prop['draw_wireframe']:
            return self.wireframe
        else:
            return None

    def getSnakeHead(self, index):
        return self.snakes[index].getHeadPosition()
