'''
Attributes:

name - string : 'Title'
size - tuple  : (x,y)
bg   - string : '#xxxxxx'
res  - tuple  : (bool,bool)
'''

import tkinter as tk

class App:
    def __init__(self,**options):
        self.name = options.get('name', 'Test')
        self.size = options.get('size',(100,100))
        self.bg = options.get('bg','#000000')
        self.res = options.get('res',(0,0))

        self.ui = tk.Tk()
        self.ui.geometry(str(self.size[0])+'x'+str(self.size[1]))
        self.ui['background'] = self.bg
        self.ui.resizable(self.res[0],self.res[1])
        tk.mainloop()
