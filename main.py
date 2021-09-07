from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import os
from panda3d.core import LineSegs, NodePath, MeshDrawer, AntialiasAttrib
import numpy as np

class Snake():
    def __init__(self, size=10, thickness=10, start_angles=np.array([0,0,0,0]),
                angle_vel=np.array([0,5,5,5]), lengths=[0.67,0.47,0.87]):
        self.size = size
        self.thickness = thickness
        self.ls = LineSegs()
        self.node = None
        self.points = []
        self.ls.setThickness(thickness)
        self.angles = np.deg2rad(start_angles)
        self.angle_vel = np.deg2rad(angle_vel)
        self.l = lengths
        self.frame_number = 0
        #self.speed = speed

    def next_frame(self):
        #update angles
        for t in range(len(self.angles)):
            self.angles[t] += self.angle_vel[t]
        self.points.append(self.getHeadPosition())
        #self.ls.reset()
        #self.ls.setThickness(1000)
        for a in self.points:
            self.ls.drawTo(a)
        self.node = NodePath(self.ls.create(True))
        self.node.setAntialias(AntialiasAttrib.MLine)
        if len(self.points) > self.size:
            self.points.pop(0)
        return self.node

    def getHeadPosition(self):
        x=0
        y=0
        z=0
        x_temp=0
        for t in range(1,len(self.angles)):
            x_temp+=self.l[t-1]*sin(self.angles[t])
            z+=self.l[t-1]*cos(self.angles[t])
        x=x_temp*cos(self.angles[0])
        y=x_temp*sin(self.angles[0])
        return (x,y,z)


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
    	#Set background color of scene (dark purple)
        base.setBackgroundColor(0.1,0,0.2,1.0)
        self.taskMgr.add(self.spin_camera_task, "SpinCameraTask")
        self.taskMgr.add(self.update_snakes, "UpdateSnakes")
        start_angles = np.array([10,10,10])
        self.snake = Snake(1000, 5, start_angles)
        self.camera_spin_speed = 80
        self.currentNode = None

    def update_snakes(self, task):
        if self.currentNode:
            self.currentNode.removeNode()
        self.currentNode = self.snake.next_frame()
        self.currentNode.reparentTo(self.render)
        return Task.cont

	# Define a procedure to move the camera.
    def spin_camera_task(self, task):
        angleDegrees = task.time * self.camera_spin_speed
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(10 * sin(angleRadians), -10 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = App()
app.run()
