'''
Documentation Todo
'''

import random
import time
import math
from WorldColor import WorldColor

class World:
	def __init__(self,worldSize):
		self.__worldSize = worldSize
		self.__colorEngine = WorldColor()
		self.__mapInternal = [['void' for x in range(self.__worldSize[0])] for y in range(self.__worldSize[1])]
		self.__mapExternal = [['#000000' for x in range(self.__worldSize[0])] for y in range(self.__worldSize[1])]
		self.__changedColors=[]
		self.__colorReference = {
			'test':self.__colorEngine.test,'void':self.__colorEngine.void,
			'random':self.__colorEngine.random,'grass':self.__colorEngine.grass,
			'water':self.__colorEngine.water
		}

		print('Generating world, please wait\n')
		worldGenTime = time.time()
		print('Loading defaults\n')
		lakeConstraints = [(5,12),(4,8)]
		self.__grassGen()
		lakeCoords = []
		numlakes = 10
		for i in range(numlakes):
			lakeCoords.append((random.randint(0,self.__worldSize[0]),random.randint(0,self.__worldSize[1])))
		for i in lakeCoords:
			self.__conicGen((i[0],i[1]),random.randint(lakeConstraints[0][0],lakeConstraints[0][1]),
			random.randint(lakeConstraints[1][0],lakeConstraints[1][1]),'water')
		self.__colorChange()
		worldGenTime = format(time.time() - worldGenTime, '0.2f')
		print('Done in {} seconds.\n'.format(worldGenTime))

	def getMap(self):
		return self.__mapExternal

	def __changeInternal(self,x,y,key):
		if x >= 0 and x < self.__worldSize[0] and y >= 0 and y < self.__worldSize[1]:
			self.__mapInternal[y][x] = key
			if (x,y) not in self.__changedColors:
				self.__changedColors.append((x,y))

	def __colorChange(self):
		print('Color Update\n')
		for i in self.__changedColors:
			self.__mapExternal[i[1]][i[0]] = self.__colorReference[self.__mapInternal[i[1]][i[0]]]()
		self.__changedColors = []

	def __randomGen(self):
		print('Loading random\n')
		for y in range(self.__worldSize[1]):
			for x in range(self.__worldSize[0]):
				self.__changeInternal(x,y,'random')

	def __grassGen(self):
		print('Loading grass\n')
		for y in range(self.__worldSize[1]):
			for x in range(self.__worldSize[0]):
				self.__changeInternal(x,y,'grass')

	def __conicGen(self,center,a,b,type):
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
					self.__changeInternal(x+center[0]-a,y+center[1]-b,type)
