'''
!- Keep in mind I have no idea what I'm doing in terms of writing
	professionally clean code -!

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
		self.name = options.get('name', 'Test')
		self.size = options.get('size',(100,100))
		self.bg = options.get('bg','#000000')
		self.res = options.get('res',(0,0))

		#Main window creation
		self.ui = tk.Tk()
		self.ui.title(self.name)
		self.ui.geometry(str(self.size[0])+'x'+str(self.size[1]))
		self.ui['background'] = self.bg
		self.ui.resizable(self.res[0],self.res[1])

	def bindKeys(self,**keyBindList):
		for char in keyBindList:
			self.ui.bind_all('<'+char+'>',keyBindList[char])

	def clamp(self, num, min, max):
		return max(min(num,max),min)
