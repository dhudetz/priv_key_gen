from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import os, sys
from panda3d.core import LineSegs, NodePath, MeshDrawer, AntialiasAttrib
import numpy as np

class Snake():
    def __init__(self, start_angles=[0,0,0,0],
    angle_vel=[0.5324,0.33094,0.93234,0.4583240], lengths=[25,25,15]):
        self.angles = np.deg2rad(start_angles)
        self.angle_vel = np.deg2rad(angle_vel)
        self.l = lengths
        self.frame_number = 0
        #self.speed = speed

    def next_frame(self):
        #update angles
        for t in range(len(self.angles)):
            self.angles[t] += self.angle_vel[t]

        #self.node = NodePath(self.ls.create(True))
        #self.node.setAntialias(AntialiasAttrib.MLine)
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


    	#Set background color of scene (dark purple)
        base.setBackgroundColor(1,1,1)
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.updateSnakes, "UpdateSnakes")
        self.nodes = []
        self.numNodes = 100
        self.snakes = []
        self.snakes.append(Snake())
        self.snakes.append(Snake())
        self.cameraSpinSpeed = 0
        self.currentNode = None

    def updateSnakes(self, task):
        for s in range(len(self.snakes)):
            if len(self.nodes)>self.numNodes-1:
                self.nodes[0].removeNode()
                self.nodes.pop(0)
            new_position = self.snakes[s].next_frame()
            new_node = loader.loadModel("\\models\\Icosahedron.egg")
            if s == 1:
                new_position = (-new_position[0], -new_position[1], -new_position[2])
            new_node.setPos(new_position)
            if s == 0:
                new_node.setColor(1,0,0)
            else:
                new_node.setColor(0,0,1)
            new_node.setTransparency(True)
            new_node.reparentTo(self.render)
            self.nodes.append(new_node)
            for i in range(len(self.nodes)):
                self.nodes[i].setScale(i/len(self.nodes),i/len(self.nodes),i/len(self.nodes))
                self.nodes[i].setAlphaScale(i/len(self.nodes))
        return Task.cont

	# Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * self.cameraSpinSpeed
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(300 * sin(angleRadians), -300 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = App()
app.run()
