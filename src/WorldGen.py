import random as rand
import time
import math

class WorldColor:
	def __init__(self):
		self.cra = [0,127,0,127,40,127]
	def colorTest(self):
		return '#2f9f9f'
	def colorTimeTest(self):
		self.timeTestCount+=1
		return '#'+hex(self.timeTestCount*1024).split('x')[-1].zfill(6)
	def colorVoid(self):
		return '#000000'
	def colorRandom(self):
		return '#{}{}{}'.format(hex(rand.randint(self.cra[0],self.cra[1])).split('x')[-1].zfill(2),hex(rand.randint(self.cra[2],self.cra[3])).split('x')[-1].zfill(2),hex(rand.randint(self.cra[4],self.cra[5])).split('x')[-1].zfill(2))
	def colorGrass(self):
		g = rand.randint(127,187)
		r = g+rand.randint(-127,0)
		b = rand.randint(27,77)
		r = hex(r).split('x')[-1].zfill(2)
		g = hex(g).split('x')[-1].zfill(2)
		b = hex(b).split('x')[-1].zfill(2)
		color = '#'+r+g+b
		return color

class World(WorldColor):
	def __init__(self,worldSize=(100,100)):
		#Eventually the other stuff will be here and the entire world stuff will hopefully be here
		self.worldSize=worldSize
		self.changedColors=[]
		self.cra = [0,127,0,127,40,127]
		self.colorReference = {
		'void':self.colorVoid,'random':self.colorRandom,'grass':self.colorGrass,'conicTest':self.colorTest
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
			self.lakeCoords.append((rand.randint(0,self.worldSize[0]),rand.randint(0,self.worldSize[1])))
		print(self.lakeCoords)
		for i in self.lakeCoords:
			self.conic((i[0],i[1]),rand.randint(self.lakeConstraints[0][0],self.lakeConstraints[0][1]),
			rand.randint(self.lakeConstraints[1][0],self.lakeConstraints[1][1]),'conicTest')
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

	def randColor(self):
		color = '#{}{}{}'.format(hex(rand.randint(self.cra[0],self.cra[1])).split('x')[-1].zfill(2),hex(rand.randint(self.cra[2],self.cra[3])).split('x')[-1].zfill(2),hex(rand.randint(self.cra[4],self.cra[5])).split('x')[-1].zfill(2))
		return color

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
