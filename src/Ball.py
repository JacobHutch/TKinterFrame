import tkinter as tk
import time as t
import math as m
class collisionTest:
     def __init__(self, gameFrame, menuRoot, width=500, height=500):
          self.type="tkinter"
          self.frame=gameFrame
          self.menu=menuRoot
          self.width=400
          self.height=400
          self.radius=8

          self.labelTest = tk.Label(self.frame, text="Test", background="#FFFFFF")
          self.labelTest.pack(fill=tk.BOTH, expand=0)

          self.canvas=tk.Canvas(self.frame, background="#001F4F",
                                width=self.width,height=self.height)
          #self.canvas["background"]="#001F4F"
          self.canvas.pack(fill=tk.NONE, expand=0)

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
          self.frame.bind_all("<Up>", self.speed)
          self.frame.bind_all("<Down>", self.slow)
          self.frame.bind_all("<t>", self.config)

     def reset(self, event):
          self.p=[self.width/2,self.height/2]

     def rotateLeft(self, event):
          self.v[1]-=self.rotateMagnitude

     def rotateRight(self, event):
          self.v[1]+=self.rotateMagnitude

     def speed(self, event):
          self.v[0]=self.clamp(self.v[0]+10,-100,100)

     def slow(self, event):
          self.v[0]=self.clamp(self.v[0]-10,-100,100)

     def config(self, event):
          self.conf=tk.Tk()
          self.conf.title("Config")
          self.conf.geometry("200x200")
          self.conf["background"]="#123456"
          self.conf.resizable(0,0)

     def eventLoop(self):
          self.labelTest["text"]=(
               "X:"+str(int(self.p[0]))+"\tY:"+str(int(self.p[1]))+
               "\t\tV:"+str(int(self.v[0]))+"\tA:"+str(int((self.v[1]*180/m.pi%360)+.5)))
          self.canvas.delete("ball","line")

          self.nline=self.canvas.create_line(self.p[0],self.p[1],
                                            self.p[0]+self.lineRadius*m.cos(self.v[1]),
                                            self.p[1]+self.lineRadius*m.sin(self.v[1]),
                                            fill="#FF0000", tags=("line"))

          self.sline=self.canvas.create_line(self.p[0],self.p[1],
                                            self.p[0]+self.lineRadius/2*-m.cos(self.v[1]),
                                            self.p[1]+self.lineRadius/2*-m.sin(self.v[1]),
                                            fill="#FFFFFF", tags=("line"))

          self.ball=self.canvas.create_oval(self.p[0]-self.radius,
                                            self.p[1]-self.radius,
                                            self.p[0]+self.radius,
                                            self.p[1]+self.radius,
                                            fill="#FFFFFF", tags=("ball"))

          self.p[0] = self.clamp(self.p[0]+(self.v[0] * m.cos(self.v[1]) *
                                            1/self.gameTick),0,self.width)
          self.p[1] = self.clamp(self.p[1]+(self.v[0] * m.sin(self.v[1]) *
                                            1/self.gameTick),0,self.height)
          self.frame.after(int(1000/self.gameTick), self.eventLoop)

     def clamp(self, num, low, high):
          return max(min(num, high), low)
