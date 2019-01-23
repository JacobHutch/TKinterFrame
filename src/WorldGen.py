import random
import time
import math
from WorldColor import WorldColor

class World:
	def __init__(self,worldSize=(100,100)):
		self.worldSize=worldSize
		self.colorEngine = WorldColor()
		self.changedColors=[]

		self.colorReference = {
		'test':self.colorEngine.test,'void':self.colorEngine.void,
		'random':self.colorEngine.random,'grass':self.colorEngine.grass,
		'water':self.colorEngine.water
		}

	def worldGen(self):
		print('Generating world, please wait\n')
		self.worldGenTime = time.time()
		print('Loading defaults\n')
		self.mapInternal = [['void' for x in range(self.worldSize[0])] for y in range(self.worldSize[1])]
		self.mapExternal = [['#000000' for x in range(self.worldSize[0])] for y in range(self.worldSize[1])]
		self.timeTestCount = 0
		self.lakeConstraints = [(5,12),(4,8)]
		#self.random()
		self.grass()
		self.lakeCoords = []
		numlakes = 10
		for i in range(numlakes):
			self.lakeCoords.append((random.randint(0,self.worldSize[0]),random.randint(0,self.worldSize[1])))
		for i in self.lakeCoords:
			self.conic((i[0],i[1]),random.randint(self.lakeConstraints[0][0],self.lakeConstraints[0][1]),
			random.randint(self.lakeConstraints[1][0],self.lakeConstraints[1][1]),'water')
		#self.conic((12,12),8,5,'conicTest')
		self.colorChange()
		self.worldGenTime = format(time.time() - self.worldGenTime, '0.2f')
		print('Done in {} seconds.\n'.format(self.worldGenTime))

	def changeInternal(self,x,y,key):
		if x >= 0 and x < self.worldSize[0] and y >= 0 and y < self.worldSize[1]:
			self.mapInternal[y][x] = key
			if (x,y) not in self.changedColors:
				self.changedColors.append((x,y))

	def random(self):
		print('Loading random\n')
		for y in range(self.worldSize[1]):
			for x in range(self.worldSize[0]):
				self.changeInternal(x,y,'random')

	def grass(self):
		print('Loading grass\n')
		for y in range(self.worldSize[1]):
			for x in range(self.worldSize[0]):
				#if y % 2 == 0:
				self.changeInternal(x,y,'grass')

	def conic(self,center,a,b,type):
		temp = [[0 for x in range(a+1)] for y in range(b+1)]
		if a == b:
			print('Loading circle\n')
		else:
			print('Loading ellipse\n')
		step = 5
		#Parametric form t:[0,2pi],x=a*cos(t),y=b*sin(t)
		for t in range(180,271,step):
			temp[round(b*math.sin(math.radians(t)))+b][round(a*math.cos(math.radians(t)))+a]=1
		for y in range(b+1):
			fv = temp[y].index(1)
			for x in range(fv,a+1):
				temp[y][x]=1
			xel = temp[y].copy()
			xel.pop()
			xel.reverse()
			temp[y].extend(xel)
		yel = temp.copy()
		yel.pop()
		yel.reverse()
		temp.extend(yel)

		for y in range(b*2+1):
			for x in range(a*2+1):
				if temp[y][x]:
					self.changeInternal(x+center[0]-a,y+center[1]-b,type)

	def colorChange(self):
		print('Color Update\n')
		for i in self.changedColors:
			self.mapExternal[i[1]][i[0]] = self.colorReference[self.mapInternal[i[1]][i[0]]]()
			#print([i[0],i[1]]
		self.changedColors = []
