'''
Concept: A top-down walking simulator

So I think what I'm gonna do is have the frame app, which the game app will pass
through as an argument
Ex:
From Frame import App
class test:
	def __init__(self, Frame)
'''

import Frame as tkf
import tkinter as tk
from tkinter import simpledialog
from tkinter import colorchooser
import random as rand
from WorldGen import World


rand.seed(1)
appOptions={'name':'Potential Walking Simulator',
			'res':(1,1),'bg':'#123456','size':(502,523)}

class Game:
	def __init__(self, App):
		self.base = App
		self.menuSetup()

		#Dict format: 'char':function
		self.keyBinds={'q':self.kill,'t':self.mosaicChange,'b':self.bgColor,
		'Up':self.movement,'Down':self.movement,'Left':self.movement,
		'Right':self.movement,'r':self.movement,'c':self.coordChange
		}
		self.base.bindKeys(**self.keyBinds)
		self.gameTick = 60  #Ticks per second

		self.fullscreenBool = False
		self.mosaicBool = False
		self.mosaic = int(self.mosaicBool)

		self.canvasSize=(500,500)
		self.worldSize=(100,100)
		self.world = World(self.worldSize)
		self.world.worldGen()
		self.worldInit(self.canvasSize[0],self.canvasSize[1])
		self.worldDisplay()
		self.drawPlayer()

		self.eventLoop()

		self.base.ui.mainloop()


	def worldInit(self,width=500,height=500):
		self.displaySize = 25	#The all-controlling independent variable - This needs to be odd or I'll cry
		self.displayDiff = [self.worldSize[0]-self.displaySize,self.worldSize[1]-self.displaySize]
		self.playerOrigin = (self.displaySize//2+1,self.displaySize//2+1)
		self.playerPos = [self.playerOrigin[0],self.playerOrigin[1]]
		self.xDiff = 0
		self.yDiff = 0
		self.squareSize = max([width,height]) // self.displaySize

		self.topLabel=tk.Label(self.base.ui, background='#cfcfcf',
								text='X: {}\tY: {}'.format(self.playerPos[0],self.playerPos[1]))
		self.topLabel.pack(fill=tk.BOTH, expand=0)
		self.canvas=tk.Canvas(self.base.ui, width=width, height=height,background=self.base.bg,highlightthickness=0)
		self.canvas.pack(fill=tk.NONE, expand=1)

	def worldDisplay(self):
		for y in range(self.displaySize):
			for x in range(self.displaySize):
				self.canvas.create_rectangle(self.squareSize*x+self.mosaic,self.squareSize*y+self.mosaic,
				self.squareSize*(x+1)-self.mosaic,self.squareSize*(y+1)-self.mosaic,
				fill=self.world.mapExternal[min(max(y+self.yDiff,0),self.worldSize[1]-1)][min(max(x+self.xDiff,0),self.worldSize[0]-1)],outline='',tags=('tile'))

	def drawPlayer(self):
		radius = 2
		pos = [1,1]
		for i in range(2):
			if self.playerPos[i] > self.worldSize[i] - self.playerOrigin[i]:
				pos[i] = self.playerPos[i]-self.displayDiff[i]
			elif self.playerPos[i] <= self.worldSize[i] - self.playerOrigin[i] and self.playerPos[i] >= self.playerOrigin[i]:
				pos[i] = self.playerOrigin[i]
			else:
				pos[i] = self.playerPos[i]

		x1,x2,y1,y2 = (self.squareSize*(pos[0]-1)+radius,self.squareSize*pos[0]-radius,
						self.squareSize*(pos[1]-1)+radius,self.squareSize*pos[1]-radius)
		self.canvas.create_rectangle(x1,y1,x2,y2,fill='#ffffff',outline='',tags=('player'))

	def redraw(self):
		self.xDiff = min(max(self.playerPos[0] - self.playerOrigin[0],0),self.displayDiff[0])
		self.yDiff = min(max(self.playerPos[1] - self.playerOrigin[1],0),self.displayDiff[1])
		self.canvas.delete('tile','player')
		self.worldDisplay()
		self.drawPlayer()
		self.topLabel['text'] = 'X: {}\tY: {}'.format(self.playerPos[0],self.playerPos[1])



	#Game Commands
	def kill(self, event=None):
		self.base.ui.destroy()

	def fullscreen(self, event=None):
		if self.fullscreenBool:
			self.base.ui.wm_state('normal')
		else:
			self.base.ui.wm_state('zoomed')
		self.fullscreenBool = not(self.fullscreenBool)

	def bgColor(self, event=None):
		initCol=list(self.canvas['background'].split('#')[-1])
		initR=int(initCol[0]+initCol[1],16)
		initG=int(initCol[2]+initCol[3],16)
		initB=int(initCol[4]+initCol[5],16)
		color=colorchooser.askcolor(title='New Background Color',initialcolor=(initR,initG,initB))[1]
		self.base.ui['background']=color
		self.canvas['background']=color

	def movement(self, event=None):
		if event == None:
			self.playerPos = [self.playerOrigin[0],self.playerOrigin[1]]
		elif event.keysym == 'r':
			self.playerPos = [self.playerOrigin[0],self.playerOrigin[1]]
		elif event.keysym == 'Up':
			self.playerPos[1] = max(self.playerPos[1]-1,1)
		elif event.keysym == 'Down':
			self.playerPos[1] = min(self.playerPos[1]+1,self.worldSize[1])
		elif event.keysym == 'Left':
			self.playerPos[0] = max(self.playerPos[0]-1,1)
		elif event.keysym == 'Right':
			self.playerPos[0] = min(self.playerPos[0]+1,self.worldSize[0])
		print(self.playerPos)
		self.redraw()

	def mosaicChange(self, event=None):
		self.mosaicBool = not(self.mosaicBool)
		self.mosaic = int(self.mosaicBool)
		self.redraw()

	def coordChange(self, event=None):
		newcoords = simpledialog.askstring(title='Coord Change',prompt='New Coords x,y:')
		newcoords = newcoords.split(',')
		newcoords = [min(max(int(x),1),self.worldSize[newcoords.index(x)]) for x in newcoords]
		self.playerPos = newcoords
		self.redraw()




	#Menu has to be last for the sake of it
	def menuSetup(self):
		self.menu = tk.Menu(self.base.ui)
		self.base.ui['menu'] = self.menu

		self.menuFile = tk.Menu(self.menu, tearoff=0)
		self.menuFile.add_command(label='Quit', command=self.kill, underline=0, accelerator='Q')
		self.menu.add_cascade(label='File', underline=0, menu=self.menuFile)

		self.menuGame = tk.Menu(self.menu, tearoff=0)
		#self.menuGame.add_command(label='Change Color', command=self.bgColor, underline=0, accelerator='B')
		self.menuGame.add_command(label='Reset Player', command=self.movement,underline=0, accelerator='R')
		self.menu.add_cascade(label='Game', underline=0, menu=self.menuGame)

	def eventLoop(self): #Waiting to implement, idk if I'll do it though
		pass
		#Which one would be best?:
		#self.eventLoop()
		#self.base.ui.after(int(1000/self.gameTick),self.eventLoop)

test = Game(tkf.App(**appOptions))
