import numpy as np
from math import pi, sin, cos
from random import random

class Megarm():
    def __init__(self, angles, angleSpeeds, lengths, numJoints = 3):
        self.angles = angles
        self.angleSpeeds = angleSpeeds
        self.lengths = lengths
        self.numJoints = numJoints

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
            x_temp+=self.lengths[t-1]*sin(angle_temp)
            z+=self.lengths[t-1]*cos(angle_temp)
        x=x_temp*cos(self.angles[0])
        y=x_temp*sin(self.angles[0])
        self.headPosition = (x,y,z)

class MasterAnimation():
    def __init__(self, prop):
        self.prop = prop
        self.snakes = []
        self.wireframe = []

        #special boi
        numSnakes = prop['num_snakes']
        mirror = prop['mirror']

        totalLength = 46
        if numSnakes < 0:
            incrementalLength = int(totalLength/numSnakes-1)
            for i in range(numSnakes):
                geom = self.generateGeom((0, 360), prop['base_speed_range'], prop['joint_speed_range'], (numSnakes-i)*incrementalLength, 3)
                self.snakes.append(Megarm(geom[0], geom[1], geom[2]))
        else:
            for i in range(numSnakes):
                geom = self.generateGeom((0, 360), prop['base_speed_range'], prop['joint_speed_range'], totalLength, 3)
                self.snakes.append(Megarm(geom[0], geom[1], geom[2]))

    def generateGeom(self, angleRange, baseSpeedRange, jointSpeedRange, totalLength, numJoints = 3):
        lengthRange = (0,totalLength/numJoints) #2
        startAngles=[]
        startSpeeds=[]
        startLengths=[]
        for j in range(numJoints+1):
            startAngles.append(random()*(angleRange[1]-angleRange[0])+angleRange[0])
        startSpeeds.append(random()*(baseSpeedRange[1]-baseSpeedRange[0])+baseSpeedRange[0])
        for j in range(1, numJoints):
            startSpeeds.append(random()*(jointSpeedRange[1]-jointSpeedRange[0])+jointSpeedRange[0])
        tempSpeed = 0
        for s in startSpeeds:
            tempSpeed += np.abs(s)
        startSpeeds.append(jointSpeedRange[1]*4 - tempSpeed)
        if numJoints > 1:
            for j in range(numJoints-1):
                startLengths.append(random()*(lengthRange[1]-lengthRange[0])+lengthRange[0])
            tempLength = 0
            for l in startLengths:
                tempLength += l
            startLengths.append(totalLength - tempLength)
        else:
            startLengths.append(totalLength)
        return(np.deg2rad(startAngles),np.deg2rad(startSpeeds),startLengths)

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
