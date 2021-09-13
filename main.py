from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task
import os, sys
from panda3d.core import loadPrcFileData, LineSegs, NodePath, MeshDrawer, LPoint3f
import numpy as np
from random import random, randint
import imageio
from panda3d.core import loadPrcFileData

import rarities
import gif_compiler
from animation import MasterAnimation


class App(ShowBase):
    def __init__(self, maxGens, maxFrames, saveGif=False):
        ShowBase.__init__(self)
        self.maxGens = maxGens
        self.maxFrames = maxFrames
        self.saveGif = saveGif

        self.origin = LPoint3f((0,0,0))

        self.genNumber = -1
        self.currentNode = None
        self.snakeHeads = []
        self.wireNodes = []
        self.frameNumber = 0
        self.background = None
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.newGeneration()

    def newGeneration(self):
        self.genNumber += 1

        #reset values
        self.currentNode = None
        self.frameNumber = 0
        for n in self.snakeHeads:
            n.removeNode()
        self.snakeHeads = []
        for n in self.wireNodes:
            n.removeNode()
        self.wireNodes = []
        self.images = []
        if self.background != None:
            self.background.destroy()
            self.background = None

        #populate self.prop[]
        self.prop = rarities.generate()

        #SET TEXTURE
        if self.prop['texture'] != None:
            self.texture = loader.loadTexture('tex/' + self.prop['texture'])

        #COLOR SECTIONING
        self.currentColorSection=0
        self.numColors = len(self.prop['colors'])
        if self.numColors > 1:
            self.colorSectionSize=np.floor(self.maxFrames/(self.numColors-1))

        #SET BACKGROUND
        if self.prop['background_image'] != None:
            self.background = OnscreenImage(parent=render2dp, image='background/'+self.prop['background_image']) # Load an image object
            base.cam2dp.node().getDisplayRegion(0).setSort(-20)

        #START ANIMATING
        self.anim = MasterAnimation(self.prop)
        self.taskMgr.add(self.updateAnimation, "UpdateSnakes")

        #PREPARE DIRECTORY
        if self.saveGif:
            tempDir = os.path.join(os.getcwd(), r'images')
            saveDir = os.path.join(tempDir, str(self.genNumber))
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)

    def renderWireframe(self, wireframe):
        lines = LineSegs()
        for wire in wireframe:
            lines.setColor(self.currentColor[0],self.currentColor[1],self.currentColor[2])
            lines.moveTo(wire[0][0],wire[0][1],wire[0][2])
            lines.drawTo(wire[1][0],wire[1][1],wire[1][2])
            lines.setThickness(2)
        node = lines.create()

        nodePath = NodePath(node)
        nodePath.reparentTo(render)
        self.anim.clearWireframe()
        self.wireNodes.append(nodePath)

    def removeLimitedGraphics(self):
        if len(self.snakeHeads)>self.prop['num_snake_heads']-1:
            self.snakeHeads[0].removeNode()
            self.snakeHeads.pop(0)
        if len(self.wireNodes)>self.prop['num_wireframes']-1:
            self.wireNodes[0].removeNode()
            self.wireNodes.pop(0)

    def updateAnimation(self, task):
        self.anim.nextFrame()
        for s in range(self.prop['num_snakes']):
            #remove old snakes and wireframes node
            self.removeLimitedGraphics()
            #set mirror prop and positions
            if self.prop['mirror'] and s == 1:
                mirrorPos = self.anim.getSnakeHead(0)
                newPos = (-mirrorPos[0], -mirrorPos[1], -mirrorPos[2])
            else:
                newPos = self.anim.getSnakeHead(s)

            #set model and textures (might want to make the model load only once)
            newNode = loader.loadModel('models/'+self.prop['model_type'])
            if self.prop['texture'] != None:
                newNode.setTexture(self.texture)
            newNode.setPos(newPos)
            newNode.setHpr(newPos[0]*self.prop['model_spin'],newPos[1]*self.prop['model_spin'],newPos[2]*self.prop['model_spin'])

            #NODE COLORS
            if self.numColors > 1:
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
                self.currentColor = (colorR,colorG,colorB)
            else:
                self.currentColor = self.prop['colors'][0]
            newNode.setColor(self.currentColor[0],self.currentColor[1],self.currentColor[2])

            #BACKGROUND COLOR
            bgColor=self.prop['background_color']
            if isinstance(bgColor, tuple):
                base.setBackgroundColor(bgColor[0],bgColor[1],bgColor[2])
            elif bgColor == 'opposite':
                base.setBackgroundColor(1-self.currentColor[0],1-self.currentColor[1],1-self.currentColor[2])
            else:
                averageGray = max([self.currentColor[0],self.currentColor[1],self.currentColor[2]])
                base.setBackgroundColor(averageGray,averageGray,averageGray)

            newNode.setTransparency(self.prop['transparency'])
            if self.prop['draw_snakes']:
                newNode.reparentTo(self.render)
            self.snakeHeads.append(newNode)
            for i in range(len(self.snakeHeads)):
                alphaMod = i/len(self.snakeHeads)
                scaleMod = i/len(self.snakeHeads)
                finalScale = (self.prop['model_scale'][0]*scaleMod, self.prop['model_scale'][1]*scaleMod, self.prop['model_scale'][2]*scaleMod)
                self.snakeHeads[i].setScale(finalScale[0],finalScale[1],finalScale[2])
                self.snakeHeads[i].setAlphaScale(alphaMod)

            if self.prop['draw_wireframe'] and self.frameNumber%1==0:
                self.renderWireframe(self.anim.getWireframe())
        if self.saveGif and (0 < self.frameNumber < self.maxFrames+1):
            file = 'images/'+str(self.genNumber)+'/'+str(self.frameNumber)+'.png'
            base.screenshot(file, None)
            #self.renderToPNM().write('images/'+str(self.genNumber)+'/'+str(self.frameNumber)+'.png')
        self.frameNumber += 1
        if self.frameNumber > self.maxFrames:
            if self.genNumber < self.maxGens-1:
                self.newGeneration()
            if self.saveGif:
                self.taskMgr.add(self.generateGif, "generateGif")
            return Task.done
        else:
            return Task.cont

    def generateGif(self, task):
        gif_compiler.generateGif(self.genNumber-1, self.maxFrames, self.prop['num_stickers'])
        return Task.done

	# Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = self.frameNumber * self.prop['camera_spin']
        angleRadians = angleDegrees * (pi / 180.0)
        radius = 210 + 40 * cos(angleRadians/2)
        self.camera.setPos(radius * sin(angleRadians), -radius * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

loadPrcFileData('', 'win-size 240 240')
loadPrcFileData('', 'clock-mode limited')
loadPrcFileData('', 'clock-frame-rate 1')

#loadPrcFileData('', 'window-type offscreen')
app = App(1000, 200, True)
app.run()
