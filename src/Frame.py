#Made by Jacob Hutchison, Started 6/27/18

#Class App can import one game object into it's frame, tkinter game MUST inherit frame and use it as the game's root,
#   then add any other arguments as needed (width, height, etc). Menu can be inherited as well

#PyGame requires   os.environ["SDL_WINDOWID"]=str(self.frame.winfo_id())    in class App before initialization,
#   but no other prerequisites

import tkinter as tk
import os
from PyGameTestExperimental import testPygame
from Ball import collisionTest

class App:
    def __init__(self):
        #Initialize Window
        self.ui=tk.Tk()
        self.ui.title("Test")
        self.ui.geometry("600x600")
        self.ui["background"]="#3F3F3F"
        self.ui.resizable(1,1)

        #Initial Functions
        self.menuSetup()
        self.keyBinds()
        
        #Main Frame  (haha)
        self.width=500
        self.height=500
        self.frame=tk.Frame(bg="#FF0000", width=self.width, height=self.height)
        self.frame.pack_propagate(0)
        self.frame.pack(fill=tk.NONE, expand=1)

        #PyGame Prerequisite
        os.environ["SDL_WINDOWID"]=str(self.frame.winfo_id())

        #Game Object goes here
        #self.game = exampleProgram(gameFrame=self.frame, menuRoot=self.menu, width=self.width, height=self.height)
        #self.game = testPygame()
        self.game = collisionTest(gameFrame=self.frame, menuRoot=self.menu, width=self.width, height=self.height)        

    def endProgram(self, event):
        self.ui.destroy()

    def menuSetup(self):
        self.menu=tk.Menu(self.ui)
        self.ui["menu"]=self.menu

        self.menuFile = tk.Menu(self.menu, tearoff=0)
        
        self.menuFile.add_command(label="Quit", command=self.ui.destroy, underline=0, accelerator="Q")

        self.menu.add_cascade(label="File", underline=0, menu=self.menuFile)

    def keyBinds(self):
        self.ui.bind_all("<q>", self.endProgram)



class exampleProgram:
    def __init__(self, gameFrame, menuRoot, width=500, height=500):
        self.type="tkinter"
        self.frame=gameFrame
        self.menu=menuRoot
        self.width=width
        self.height=height

        self.gameTick=60
        
        self.canvas=tk.Canvas(self.frame)
        self.canvas["background"]="#001F4F"
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.ballRadius=10
        self.ballSpeed=5
        self.ballPosx1=self.width/2-self.ballRadius
        self.ballPosy1=self.height/2-self.ballRadius
        self.ballPosx2=self.width/2+self.ballRadius
        self.ballPosy2=self.height/2+self.ballRadius
        self.ball=self.canvas.create_oval(self.ballPosx1, self.ballPosy1,
                                          self.ballPosx2, self.ballPosy2,
                                          fill="#FFFFFF", tags=("ball"))
        self.ballPos(self.ballPosx1, self.ballPosy1, self.ballPosx2, self.ballPosy2)
        self.ball2Radius=10
        self.ball2Speed=5
        self.ball2Posx1=self.width/2-self.ball2Radius
        self.ball2Posy1=self.height/2-self.ball2Radius
        self.ball2Posx2=self.width/2+self.ball2Radius
        self.ball2Posy2=self.height/2+self.ball2Radius
        self.ball2=self.canvas.create_oval(self.ball2Posx1, self.ball2Posy1,
                                          self.ball2Posx2, self.ball2Posy2,
                                          fill="#FFFFFF", tags=("ball"))
        self.ball2Pos(self.ball2Posx1, self.ball2Posy1, self.ball2Posx2, self.ball2Posy2)
        self.menuSetup()
        self.keyBinds()

    def keyBinds(self):
        self.frame.bind_all("<r>", self.resetBall)
        self.frame.bind_all("<Up>", self.moveUp)
        self.frame.bind_all("<Down>", self.moveDown)
        self.frame.bind_all("<Left>", self.moveLeft)
        self.frame.bind_all("<Right>", self.moveRight)
        self.frame.bind_all("<e>", self.resetBall2)
        self.frame.bind_all("<w>", self.moveUp2)
        self.frame.bind_all("<s>", self.moveDown2)
        self.frame.bind_all("<a>", self.moveLeft2)
        self.frame.bind_all("<d>", self.moveRight2)

    def menuSetup(self):
        self.menuGame = tk.Menu(self.menu, tearoff=0)
        
        self.menuGame.add_command(label="Reset Ball", command=lambda:self.ballPos(self.ballPosx1, self.ballPosy1, self.ballPosx2, self.ballPosy2), underline=0, accelerator="R")
        
        self.menu.add_cascade(label="Game", underline=0, menu=self.menuGame)

    def ballPos(self, x1, y1, x2, y2):
        self.canvas.coords(self.ball, x1, y1, x2, y2)
        
    def resetBall(self, event):
        self.ballPos(self.ballPosx1, self.ballPosy1, self.ballPosx2, self.ballPosy2)

    def moveUp(self, event):
        self.canvas.move(self.ball, 0, -self.ballSpeed)

    def moveDown(self, event):
        self.canvas.move(self.ball, 0, self.ballSpeed)

    def moveLeft(self, event):
        self.canvas.move(self.ball, -self.ballSpeed, 0)

    def moveRight(self, event):
        self.canvas.move(self.ball, self.ballSpeed, 0)

    def ball2Pos(self, x1, y1, x2, y2):
        self.canvas.coords(self.ball2, x1, y1, x2, y2)
        
    def resetBall2(self, event):
        self.ball2Pos(self.ball2Posx1, self.ball2Posy1, self.ball2Posx2, self.ball2Posy2)

    def moveUp2(self, event):
        self.canvas.move(self.ball2, 0, -self.ballSpeed)

    def moveDown2(self, event):
        self.canvas.move(self.ball2, 0, self.ballSpeed)

    def moveLeft2(self, event):
        self.canvas.move(self.ball2, -self.ballSpeed, 0)

    def moveRight2(self, event):
        self.canvas.move(self.ball2, self.ballSpeed, 0)
        

class examplePygame:
    def __init__(self):
        pygame.display.init()
        self.board = pygame.display.set_mode((300,300))
        pygame.draw.rect(self.board, (0,255,255), (100,50,20,20))

if __name__=="__main__":
    app=App()
    app.ui.after(int(1000/app.game.gameTick), app.game.eventLoop)
    app.ui.mainloop()
    if app.game.type=="pygame":
         app.game.eventLoop()

