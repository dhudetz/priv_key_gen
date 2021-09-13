import numpy as np
from math import pi, sin, cos
from random import random, randint

class Megarm():
    def __init__(self, angles=[0,0], angleSpeeds=[0,0], lengths=[0,0], numJoints = 3, mirrorPair = None):
        self.angles = angles
        self.angleSpeeds = angleSpeeds
        self.lengths = lengths
        self.numJoints = numJoints
        self.mirrorPair = mirrorPair

    def nextFrame(self):
        #update angles with angle speeds
        for t in range(len(self.angles)):
            self.angles[t] += self.angleSpeeds[t]
        self.calculateHeadPosition()

    def getHeadPosition(self):
        return self.headPosition

    def calculateHeadPosition(self):
        if self.mirrorPair == None:
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
        else:
            mirrorPos = self.mirrorPair.getHeadPosition()
            self.headPosition = (-mirrorPos[0], -mirrorPos[1], -mirrorPos[2])

class MasterAnimation():
    def __init__(self, prop):
        self.prop = prop
        self.snakes = []
        self.wireframe = []

        #special boi
        numSnakes = prop['num_snakes']
        mirror = prop['mirror']

        totalLength = 46
        numJoints = 3
        if mirror and numSnakes == 2:
            geom = self.generateGeom((0, 360), prop['base_speed_range'], prop['joint_speed_range'], totalLength, numJoints)
            parentSnake = Megarm(geom[0], geom[1], geom[2])
            self.snakes.append(parentSnake)
            self.snakes.append(Megarm(mirrorPair = parentSnake))
        elif mirror and numSnakes > 2:
            geom = self.generateGeom((0, 360), prop['base_speed_range'], prop['joint_speed_range'], totalLength, numJoints)
            for i in range(numSnakes):
                newgeom = []
                for j in range(len(geom)):
                    newgeom.append([])
                    for k in geom[j]:
                        newgeom[j].append(k)
                newgeom[0][0] = ((2*pi)/numSnakes)*i
                #newgeom[0][1] = ((2*pi)/numSnakes)*i
                self.snakes.append(Megarm(newgeom[0], newgeom[1], newgeom[2]))
        else:
            for i in range(numSnakes):
                geom = self.generateGeom((0, 360), prop['base_speed_range'], prop['joint_speed_range'], totalLength, numJoints)
                self.snakes.append(Megarm(geom[0], geom[1], geom[2]))

    def generateGeom(self, angleRange, baseSpeedRange, jointSpeedRange, totalLength, numJoints = 3):
        lengthRange = (0,totalLength/numJoints) #2
        startAngles=[]
        startSpeeds=[]
        startLengths=[]
        dir = [-1,1]
        for j in range(numJoints+1):
            startAngles.append(dir[randint(0,1)]*random()*(angleRange[1]-angleRange[0])+angleRange[0])
        startSpeeds.append(dir[randint(0,1)]*random()*(baseSpeedRange[1]-baseSpeedRange[0])+baseSpeedRange[0])
        for j in range(1, numJoints+1):
            startSpeeds.append(dir[randint(0,1)]*random()*(jointSpeedRange[1]-jointSpeedRange[0])+jointSpeedRange[0])
        tempSpeed = 0
        #for s in startSpeeds:
        #    tempSpeed += np.abs(s)
        #startSpeeds.append(jointSpeedRange[1]*2.5 - tempSpeed)
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
