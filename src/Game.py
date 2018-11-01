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
import time as t

appOptions={'name':'Potential Walking Simulator',
			'res':(1,1),'bg':'#123456','size':(500,500)}

class Game:
	def __init__(self, App):
		self.frame = App

		#Dict format: 'char':function
		self.keyBinds={'q':self.kill,'t':self.bgColor}
		self.frame.bindKeys(**self.keyBinds)

		self.frame.ui.mainloop()

	def kill(self, event):
		self.frame.ui.destroy()

	def bgColor(self, event):
		self.frame.ui['background']='#'+''.join(str(t.time()*10**6)[-8:-2])

test = Game(tkf.App(**appOptions))
