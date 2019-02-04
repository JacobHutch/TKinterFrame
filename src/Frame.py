'''
Simple TKinter Base Frame Object

Options:
name - string : 'Title'
size - tuple  : (x,y)
bg   - string : '#xxxxxx'
res  - tuple  : (bool,bool)
'''

import tkinter as tk

class App:
	def __init__(self,**options):

		#Option variables initialization
		self.__name = options.get('name', 'Test')
		self.__size = options.get('size',(100,100))
		self.__bg = options.get('bg','#000000')
		self.__res = options.get('res',(0,0))

		#Main window creation
		self.__ui = tk.Tk()
		self.__ui.title(self.__name)
		self.__ui.geometry(str(self.__size[0])+'x'+str(self.__size[1]))
		self.__ui['background'] = self.__bg
		self.__ui.resizable(self.__res[0],self.__res[1])

	def bindKeys(self,**keyBindList):
		for char in keyBindList:
			self.__ui.bind_all('<'+char+'>',keyBindList[char])

	def getUi(self):
		return self.__ui

	def getBg(self):
		return self.__bg

	def setSize(self, size=None):
		if size == None:
			size = str(self.__size[0])+'x'+str(self.__size[1])
		self.__ui.geometry(size)
