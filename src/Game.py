'''
Concept: A top-down walking simulator
'''

import tkinter as tk
import random as rand
from Frame import App
from WorldGen import World
from CommandCenter import Commander

class Game:
	def __init__(self,resolution=(500,500),worldSize=(100,100),tileAmount=25):
		self.__canvasSize = resolution
		self.__worldSize = worldSize
		self.__displaySize = tileAmount
		self.__appOptions = {
			'name':'Potential Walking Simulator','res':(1,1),
			'bg':'#123456','size':(self.__canvasSize[0]+2,self.__canvasSize[1]+23)
		}
		self.__base = App(**self.__appOptions)
		self.__com = Commander(self)
		rand.seed(1)

		#Dict format: 'char':function
		self.__movementKeyBinds={'Up':self.movement,'Down':self.movement,'Left':self.movement,
								'Right':self.movement}
		self.__base.bindKeys(**self.__movementKeyBinds)

		self.__mosaic = 0 #Temp

		self.__world = World(self.__worldSize)

		self.__displayDiff = [self.__worldSize[0]-self.__displaySize,self.__worldSize[1]-self.__displaySize]
		self.__screenDiff = self.__displaySize//2+1
		self.__playerPos = [self.__worldSize[0]//2,self.__worldSize[1]//2]
		self.__squareSize = max(self.__canvasSize) // self.__displaySize
		self.__tileList = {}

		self.__topLabel=tk.Label(self.__base.getUi(), background='#cfcfcf',
								text='X: {}\tY: {}'.format(self.__playerPos[0],self.__playerPos[1]))
		self.__topLabel.grid(row=0,column=0,sticky='we')
		self.__canvas=tk.Canvas(self.__base.getUi(), width=self.__canvasSize[0], height=self.__canvasSize[1],background=self.__base.getBg(),highlightthickness=0)
		self.__canvas.grid(row=1,column=0,padx=1,pady=1)
		self.__base.getUi().grid_columnconfigure(0,weight=1)
		self.__base.getUi().grid_rowconfigure(1,weight=1)

		self.__createTiles()
		self.colorWorld()

		self.__base.getUi().mainloop()

	def __createTiles(self):
		for y in range(self.__displaySize):
			for x in range(self.__displaySize):
				self.__tileList[str(x)+'x'+str(y)] = self.__canvas.create_rectangle(self.__squareSize*x+self.__mosaic,self.__squareSize*y+self.__mosaic,
					self.__squareSize*(x+1)-self.__mosaic,self.__squareSize*(y+1)-self.__mosaic,
					fill='#ffffff',outline='',tags=('tile'))
		self.drawPlayer()

	def colorWorld(self):
		self.__xDiff = min(max(self.__playerPos[0] - self.__screenDiff,0),self.__displayDiff[0])
		self.__yDiff = min(max(self.__playerPos[1] - self.__screenDiff,0),self.__displayDiff[1])
		for y in range(self.__displaySize):
			for x in range(self.__displaySize):
				self.__canvas.itemconfig(self.__tileList[str(x)+'x'+str(y)],
					fill=self.__world.getMap()[min(max(y+self.__yDiff,0),self.__worldSize[1]-1)][min(max(x+self.__xDiff,0),self.__worldSize[0]-1)])
		self.__topLabel['text'] = 'X: {}\tY: {}'.format(self.__playerPos[0],self.__playerPos[1])
		self.averageColor()

	def drawPlayer(self):
		negativeRadius = 2
		pos = [1,1]
		for i in range(2):
			if self.__playerPos[i] > self.__worldSize[i] - self.__screenDiff:
				pos[i] = self.__playerPos[i]-self.__displayDiff[i]
			elif self.__playerPos[i] <= self.__worldSize[i] - self.__screenDiff and self.__playerPos[i] >= self.__screenDiff:
				pos[i] = self.__screenDiff
			else:
				pos[i] = self.__playerPos[i]

		x1,x2,y1,y2 = (self.__squareSize*(pos[0]-1)+negativeRadius,self.__squareSize*pos[0]-negativeRadius,
						self.__squareSize*(pos[1]-1)+negativeRadius,self.__squareSize*pos[1]-negativeRadius)
		self.__canvas.delete('player')
		self.__canvas.create_rectangle(x1,y1,x2,y2,fill='#ffffff',outline='',tags=('player'))

	def movement(self, event=None):
		if event.keysym == 'Up':
			self.__playerPos[1] = max(self.__playerPos[1]-1,1)
		elif event.keysym == 'Down':
			self.__playerPos[1] = min(self.__playerPos[1]+1,self.__worldSize[1])
		elif event.keysym == 'Left':
			self.__playerPos[0] = max(self.__playerPos[0]-1,1)
		elif event.keysym == 'Right':
			self.__playerPos[0] = min(self.__playerPos[0]+1,self.__worldSize[0])
		self.colorWorld()
		self.drawPlayer()

	def averageColor(self, event=None):
		leng = len(self.__tileList)
		r,g,b = 0,0,0
		for i in self.__tileList:
			initCol=list(self.__canvas.itemcget(self.__tileList[i],'fill').split('#')[-1])
			r+=int(initCol[0]+initCol[1],16)
			g+=int(initCol[2]+initCol[3],16)
			b+=int(initCol[4]+initCol[5],16)
		r,g,b = round(r/leng),round(g/leng),round(b/leng)
		color='#{}{}{}'.format(hex(r).split('x')[-1].zfill(2),hex(g).split('x')[-1].zfill(2),hex(b).split('x')[-1].zfill(2))
		self.__base.getUi()['background']=color
		self.__canvas['background']=color

	def getCanvas(self):
		return self.__canvas

	def getBase(self):
		return self.__base

	def getWorldSize(self):
		return self.__worldSize

	def getTileList(self):
		return self.__tileList

	def setPlayerPos(self,coords):
		self.__playerPos = coords

	def swapMosaic(self):
		self.__mosaic = int(not(bool(self.__mosaic)))
		self.__canvas.delete('tile')
		self.__createTiles()
		self.colorWorld()

	def eventLoop(self): #Available to implement, if/when is TBD
		self.colorWorld()
		self.__base.getUi().after(int(1000/60),self.eventLoop)

WalkingSimulator = Game((500,500),(100,100),25)
