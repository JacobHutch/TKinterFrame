import tkinter as tk
import time as t
import math as m
class collisionTest:
     def __init__(self, gameFrame, menuRoot, width=500, height=500):
          self.type="tkinter"
          self.frame=gameFrame
          self.menu=menuRoot
          self.width=width
          self.height=height
          self.radius=8

          self.canvas=tk.Canvas(self.frame)
          self.canvas["background"]="#001F4F"
          self.canvas.pack(fill=tk.BOTH, expand=1)

          self.keyBinds()

          self.p=[self.width/2,self.height/2]
          self.v=[50,m.pi/6]

          #Configs
          self.rotateMagnitude=m.pi/12
          self.gameTick=60
          self.lineRadius=50

     def keyBinds(self):
          self.frame.bind_all("<r>", self.reset)
          self.frame.bind_all("<Left>", self.rotateLeft)
          self.frame.bind_all("<Right>", self.rotateRight)

     def reset(self, event):
          self.p=[self.width/2,self.height/2]

     def rotateLeft(self, event):
          self.v[1]-=self.rotateMagnitude

     def rotateRight(self, event):
          self.v[1]+=self.rotateMagnitude

     def speed(self, event):
          self.v[0]=self.clamp(self.v[0]+10,0,100)

     def slow(self, event):
          self.v[0]=self.clamp(self.v[0]-10,0,100)

     def eventLoop(self):
          self.canvas.delete("ball","line")
          self.ball=self.canvas.create_oval(self.p[0]-self.radius,
                                            self.p[1]-self.radius,
                                            self.p[0]+self.radius,
                                            self.p[1]+self.radius,
                                            fill="#FFFFFF", tags=("ball"))
          self.line=self.canvas.create_line(self.p[0],self.p[1],
                                            self.p[0]+self.lineRadius*m.cos(self.v[1]),
                                            self.p[1]+self.lineRadius*m.sin(self.v[1]),
                                            fill="#ffffff", tags=("line"))
          
          self.p[0] += (self.v[0] * m.cos(self.v[1]) * 1/self.gameTick)
          self.p[1] += (self.v[0] * m.sin(self.v[1]) * 1/self.gameTick)
          self.frame.after(int(1000/self.gameTick), self.eventLoop)

     def clamp(self, num, low, high):
          return max(min(num, high), low)
