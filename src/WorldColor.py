'''
Colors are created inside the functions that call them, and are not stored/kept as variables.
I don't think this is bad methodology but maybe it is. The only variable kept is '__randomColorParams',
the parameters for the random color function. It's kept open for changes, and the layout can be
seen in the modification function.
'''

import random

class WorldColor:
	def __init__(self):
		self.__randomColorParams = [0,127,0,127,40,127]

	#Misc.
	def changeRandomParameters(self,rmin,rmax,gmin,gmax,bmin,bmax):
		self.__randomColorParams = [rmin,rmax,gmin,gmax,bmin,bmax]

	#Colors
	def test(self):
		return '#2f9f9f'
	def timeTest(self):
		timeTestCount+=1
		return '#'+hex(timeTestCount*1024).split('x')[-1].zfill(6)
	def void(self):
		return '#000000'
	def random(self):
		return '#{}{}{}'.format(hex(random.randint(self.__randomColorParams[0],self.__randomColorParams[1])).split('x')[-1].zfill(2),hex(random.randint(self.__randomColorParams[2],self.__randomColorParams[3])).split('x')[-1].zfill(2),hex(random.randint(self.__randomColorParams[4],self.__randomColorParams[5])).split('x')[-1].zfill(2))
	def grass(self):
		g = random.randint(127,187)
		r = g+random.randint(-127,0)
		b = random.randint(27,77)
		r = hex(r).split('x')[-1].zfill(2)
		g = hex(g).split('x')[-1].zfill(2)
		b = hex(b).split('x')[-1].zfill(2)
		return '#'+r+g+b
	def water(self):
		return '#1f4f9f'
