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
			'res':(1,1),'bg':'#123456','size':(550,550)}

class Game:
	def __init__(self, App):
		self.base = App
		self.menuSetup()

		#Dict format: 'char':function
		self.keyBinds={'q':self.kill,'t':self.bgColor,
		'Up':self.movement,'Down':self.movement,'Left':self.movement,
		'Right':self.movement,'r':self.movement}
		self.base.bindKeys(**self.keyBinds)

		self.worldSize=(90,90)
		self.worldInit(500,500)
		self.worldDisplay()

		self.base.ui.mainloop()

	#Probably where all the world gen will be
	def worldInit(self,width,height):
		self.playerOrigin = (5,5)
		self.playerPos = [self.playerOrigin[0],self.playerOrigin[1]]
		self.xDiff = 0
		self.yDiff = 0
		self.displaySize = 30
		self.squareSize = max(appOptions['size']) // self.displaySize

		self.topLabel=tk.Label(self.base.ui, background='#cfcfcf',
								text=('X: '+str(self.playerPos[0])+'\tY: '+str(self.playerPos[1])))
		self.topLabel.pack(fill=tk.BOTH, expand=0)
		self.canvas=tk.Canvas(self.base.ui, width=width, height=height,background='#555555',highlightthickness=0)
		self.canvas.pack(fill=tk.NONE, expand=1)

		self.world = [[0 for x in range(self.worldSize[0])] for y in range(self.worldSize[1])]
		r,c=0,0
		for x in self.world:
			for y in x:
				self.world[r][c] = '#'+str(rand.randint(10,99))+str(rand.randint(10,99))+str(rand.randint(10,99))
				c+=1
			c=0
			r+=1
		print(self.world)

	def worldDisplay(self):
		for x in range(self.displaySize):
			for y in range(self.displaySize):
				self.canvas.create_rectangle(self.squareSize*x,self.squareSize*y,
				self.squareSize*(x+1),self.squareSize*(y+1),
				fill=self.world[x+self.xDiff][y+self.yDiff],outline='',tags=('tile'))



	#Game Commands
	def kill(self, event=None):
		self.base.ui.destroy()

	def bgColor(self, event=None):
		self.base.ui['background']='#'+''.join(str(time.time()*10**6)[-8:-2])

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
		self.xDiff = self.playerPos[0] - 5
		self.yDiff = self.playerPos[1] - 5
		self.canvas.delete('tile')
		self.worldDisplay()



	#Menu has to be last for the sake of it
	def menuSetup(self):
		self.menu = tk.Menu(self.base.ui)
		self.base.ui['menu'] = self.menu

		self.menuFile = tk.Menu(self.menu, tearoff=0)
		self.menuFile.add_command(label='Quit', command=self.kill, underline=0, accelerator='Q')
		self.menu.add_cascade(label='File', underline=0, menu=self.menuFile)

		self.menuGame = tk.Menu(self.menu, tearoff=0)
		self.menuGame.add_command(label='Change Color', command=self.bgColor, underline=0, accelerator='T')
		self.menuGame.add_command(label='Reset Player', command=self.movement,underline=0, accelerator='R')
		self.menu.add_cascade(label='Game', underline=0, menu=self.menuGame)

test = Game(tkf.App(**appOptions))
