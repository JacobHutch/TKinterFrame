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
import time
import random as rand

rand.seed(1)
appOptions={'name':'Potential Walking Simulator',
			'res':(1,1),'bg':'#123456','size':(502,523)}

class Game:
	def __init__(self, App):
		self.base = App
		self.menuSetup()

		#Dict format: 'char':function
		self.keyBinds={'q':self.kill,#'t':self.bgColor,
		'Up':self.movement,'Down':self.movement,'Left':self.movement,
		'Right':self.movement,'r':self.movement}
		self.base.bindKeys(**self.keyBinds)

		self.canvasSize=(500,500)
		self.worldSize=(100,100)
		self.worldInit(self.canvasSize[0],self.canvasSize[1])
		self.worldDisplay()

		self.base.ui.mainloop()

	#Probably where all the world gen will be   --probably not anymore, I'll make a worldGen function later
	def worldInit(self,width,height):
		self.displaySize = 25	#This needs to be odd or I'll cry
		self.playerOrigin = (self.displaySize//2+1,self.displaySize//2+1)
		self.playerPos = [self.playerOrigin[0],self.playerOrigin[1]]
		self.xDiff = 0
		self.yDiff = 0
		self.squareSize = max(self.canvasSize) // self.displaySize

		self.topLabel=tk.Label(self.base.ui, background='#cfcfcf',
								text=('X: '+str(self.playerPos[0])+'\tY: '+str(self.playerPos[1])))
		self.topLabel.pack(fill=tk.BOTH, expand=0)
		self.canvas=tk.Canvas(self.base.ui, width=width, height=height,background=self.base.bg,highlightthickness=0)
		self.canvas.pack(fill=tk.NONE, expand=1)

		self.world = [[0 for x in range(self.worldSize[0])] for y in range(self.worldSize[1])]
		r,c=0,0
		for x in self.world:
			for y in x:
				self.world[r][c] = '#'+hex(rand.randint(0,255)).split('x')[-1].zfill(2)+hex(rand.randint(0,255)).split('x')[-1].zfill(2)+hex(rand.randint(0,255)).split('x')[-1].zfill(2)
				c+=1
			c=0
			r+=1
		print(self.world)

	def worldDisplay(self):
	#x and y are flipped from array to display because of math, and the flip should be isolated to the display so the array changing doesn't need extra thinking
		for x in range(self.displaySize):
			for y in range(self.displaySize):
				self.canvas.create_rectangle(self.squareSize*x,self.squareSize*y,
				self.squareSize*(x+1),self.squareSize*(y+1),
				fill=self.world[min(max(y+self.yDiff,0),self.worldSize[1]-1)][min(max(x+self.xDiff,0),self.worldSize[0]-1)],outline='',tags=('tile'))

	def drawPlayer(self):
		self.canvas.create_rectangle(self.squareSize*(self.playerOrigin[0]-1),self.squareSize*(self.playerOrigin[1]-1),
										self.squareSize*self.playerOrigin[0],self.squareSize*self.playerOrigin[1],
										fill='#000000',outline='',tags=('player'))



	#Game Commands
	def kill(self, event=None):
		self.base.ui.destroy()

	def bgColor(self, event=None):
		self.base.ui['background']='#'+hex(rand.randint(0,16777215)).split('x')[-1].zfill(6)

	def movement(self, event=None):
		if event == None:
			self.playerPos = [self.playerOrigin[0],self.playerOrigin[1]]
		elif event.keysym == 'r':
			self.playerPos = [self.playerOrigin[0],self.playerOrigin[1]]
		elif event.keysym == 'Up':
			self.playerPos[1] = max(self.playerPos[1]-1,0)
		elif event.keysym == 'Down':
			self.playerPos[1] = min(self.playerPos[1]+1,self.worldSize[1])
		elif event.keysym == 'Left':
			self.playerPos[0] = max(self.playerPos[0]-1,0)
		elif event.keysym == 'Right':
			self.playerPos[0] = min(self.playerPos[0]+1,self.worldSize[0])
		self.topLabel['text'] = ('X: '+str(self.playerPos[0])+'\tY: '+str(self.playerPos[1]))
		print(self.playerPos)
		self.xDiff = self.playerPos[0] - self.playerOrigin[0]
		self.yDiff = self.playerPos[1] - self.playerOrigin[1]
		self.canvas.delete('tile')
		self.worldDisplay()
		self.drawPlayer()



	#Menu has to be last for the sake of it
	def menuSetup(self):
		self.menu = tk.Menu(self.base.ui)
		self.base.ui['menu'] = self.menu

		self.menuFile = tk.Menu(self.menu, tearoff=0)
		self.menuFile.add_command(label='Quit', command=self.kill, underline=0, accelerator='Q')
		self.menu.add_cascade(label='File', underline=0, menu=self.menuFile)

		self.menuGame = tk.Menu(self.menu, tearoff=0)
		#self.menuGame.add_command(label='Change Color', command=self.bgColor, underline=0, accelerator='T')
		self.menuGame.add_command(label='Reset Player', command=self.movement,underline=0, accelerator='R')
		self.menu.add_cascade(label='Game', underline=0, menu=self.menuGame)

test = Game(tkf.App(**appOptions))
