from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.filter.CommonFilters import CommonFilters
from direct.task import Task
import os, sys
from panda3d.core import loadPrcFileData, LineSegs, NodePath, MeshDrawer, LPoint3f, PointLight, AmbientLight
import numpy as np
from random import random, randint
import imageio

import rarities
import gif_compiler
from animation import MasterAnimation


class App(ShowBase):
    def __init__(self, maxGens, maxFrames, saveGif=False):
        ShowBase.__init__(self)
        self.maxGens = maxGens
        self.maxFrames = maxFrames
        self.saveGif = saveGif

        self.origin = NodePath(LineSegs().create())
        self.origin.reparentTo(render)
        self.origin.setPos(0.0,70.0,30.0)

        self.filters = CommonFilters(base.win, base.cam)

        self.genNumber = -1
        self.snakeHeads = []
        self.wireNodes = []
        self.lights=[]
        self.frameNumber = 0
        self.background = None
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.newGeneration()

    def newGeneration(self):
        self.genNumber += 1

        #reset values
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

        #RESET AND SET LIGHTING
        for i in range(len(self.lights)):
            render.clearLight(self.lights[0])
            self.lights.pop(0)
        if len(self.prop['lights']) > 0:
            for l in self.prop['lights']:
                if l[0] == 'p':
                    light = PointLight('plight')
                    light.setColor(l[1])
                    lightNodePath = render.attachNewNode(light)
                    lightNodePath.setPos(l[2], l[3], l[4])
                elif l[0] == 'a':
                    light = AmbientLight('alight')
                    light.setColor(l[1])
                    lightNodePath = render.attachNewNode(light)
                self.lights.append(lightNodePath)
        for l in self.lights:
            render.setLight(l)

        #SET LOOP BUFFER FRAMES
        if self.prop['post_process'] != '':
            self.loopBufferFrames = 0
        else:
            self.loopBufferFrames = 20

        #PREPARE DIRECTORY
        if self.saveGif:
            tempDir = os.path.join(os.getcwd(), r'images')
            saveDir = os.path.join(tempDir, str(self.genNumber))
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)

        #START ANIMATING
        self.cameraRoll = randint(0,360)
        self.anim = MasterAnimation(self.prop)
        self.taskMgr.add(self.updateAnimation, "UpdateSnakes")

    def renderFilter(self):
        #self.filters.setBloom(blend=(0.3,0.4,0.3,0.6), mintrigger=0.9, maxtrigger=1.0, desat=1.0, intensity=0.3, size="small")
        if len(self.prop['filter'])>0 and self.prop['filter'][0]>0:
            self.filters.setCartoonInk(self.prop['filter'][0])
        if len(self.prop['filter'])>1 and self.prop['filter'][1]>0:
            self.filters.setBloom(blend=(0.5,0.5,0.5,1), mintrigger=0.5, maxtrigger=1.0, desat=1.0, intensity=self.prop['filter'][1], size="large")
        if len(self.prop['filter'])>2 and self.prop['filter'][2]:
            if len(self.snakeHeads)>self.prop['num_snakes']:
                #for i in range(self.prop['num_snakes']):
                    #self.filters.setVolumetricLighting(caster=self.snakeHeads[len(self.snakeHeads)-1-i],decay=0.9)
                self.filters.setVolumetricLighting(caster=self.origin,decay=0.9)
        if self.prop['invert']:
            self.filters.setInverted()
        #self.filters.delVolumetricLighting()

        #self.filters.delAmbientOcclusion()

    def clearFilters(self):
        self.filters.delBloom()
        self.filters.delCartoonInk()
        self.filters.delInverted()
        self.filters.delVolumetricLighting()

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
        while(len(self.snakeHeads)>self.prop['num_nodes']):
            self.snakeHeads[0].removeNode()
            self.snakeHeads.pop(0)
        while(len(self.wireNodes)>self.prop['num_wireframes']):
            self.wireNodes[0].removeNode()
            self.wireNodes.pop(0)

    def updateAnimation(self, task):
        self.anim.nextFrame()

        #shrink the number of wireframes and nodes when approaching the end
        if (self.maxFrames - self.loopBufferFrames - self.frameNumber) <= 0:
            self.prop['num_nodes'] = 0
            self.prop['num_wireframes'] = 0
        elif self.prop['num_nodes'] > (self.maxFrames - self.loopBufferFrames - self.frameNumber) > 0:
            self.prop['num_nodes'] = (self.maxFrames  - self.loopBufferFrames - self.frameNumber)
            self.prop['num_wireframes'] = ((self.maxFrames  - self.loopBufferFrames - self.frameNumber)/self.prop['num_snakes'])+1

        #clear the filters each frame
        self.clearFilters()

        #for each snake...
        for s in range(self.prop['num_snakes']):
            #remove old snakes and wireframes node
            self.removeLimitedGraphics()

            #get position
            newPos = self.anim.getSnakeHead(s)

            #set model and textures (might want to make the model load only once)
            newNode = loader.loadModel('models/'+self.prop['model_type'])
            if self.prop['texture'] != None:
                newNode.setTexture(self.texture)
            newNode.setPos(newPos)
            if self.prop['rotate_model']:
                newNode.setHpr(newPos[0]*self.prop['model_spin'],newPos[1]*self.prop['model_spin'],newPos[2]*self.prop['model_spin'])

            #NODE COLORS
            if self.prop['color_pattern'] == 'gradient':
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
            elif self.prop['color_pattern'] == 'alternate':
                if self.currentColorSection >= self.numColors:
                    self.currentColorSection = 0
                self.currentColor=self.prop['colors'][self.currentColorSection]

            newNode.setColor(self.currentColor[0],self.currentColor[1],self.currentColor[2])

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

        #for alternating colors, update the colorsection for all snakes overall
        if self.prop['color_pattern'] == 'alternate':
            self.currentColorSection+=1

        #BACKGROUND COLOR
        bgColor=self.prop['background_color']
        if isinstance(bgColor, tuple):
            base.setBackgroundColor(bgColor[0],bgColor[1],bgColor[2])
        elif bgColor == 'opposite':
            base.setBackgroundColor(1-self.currentColor[0],1-self.currentColor[1],1-self.currentColor[2])
        else:
            averageGray = max([self.currentColor[0],self.currentColor[1],self.currentColor[2]])
            base.setBackgroundColor(averageGray,averageGray,averageGray)

        #render filter
        self.renderFilter()

        #save images for gif compiler
        if self.saveGif and (0 < self.frameNumber < self.maxFrames+1):
            file = 'images/'+str(self.genNumber)+'/'+str(self.frameNumber)+'.png'
            base.screenshot(file, None)
            #self.renderToPNM().write('images/'+str(self.genNumber)+'/'+str(self.frameNumber)+'.png')
        self.frameNumber += 1
        if self.frameNumber > self.maxFrames:
            self.clearFilters()
            if self.saveGif:
                self.generateGif()
            if self.genNumber < self.maxGens-1:
                self.newGeneration()
            return Task.done
        else:
            return Task.cont

    def generateGif(self):
        gif_compiler.generateGif(self.genNumber, self.maxFrames, self.prop)
        return Task.done

	# Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = self.frameNumber * self.prop['camera_spin']
        angleRadians = angleDegrees * (pi / 180.0)
        radius = 350 + 20 * cos(angleRadians/2)
        self.camera.setPos(radius * sin(angleRadians), -radius * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, self.cameraRoll)
        return Task.cont

loadPrcFileData('', 'win-size 350 350')
loadPrcFileData('', 'clock-mode limited')
loadPrcFileData('', 'clock-frame-rate 1')

#loadPrcFileData('', 'window-type offscreen')
app = App(1000, 400, True)
app.run()
