import pygame, sys
from pygame.locals import *

class testPygame:
    def __init__(self, width=500, height=500):
        self.type="pygame"
        self.width=width
        self.height=height
        self.posx=int(self.width/2)
        self.posy=int(self.height/2)
        self.radius=10
        self.speed=10
        pygame.display.init()
        pygame.display.set_caption("**Meant For TKinter Embed**")
        self.board=pygame.display.set_mode((self.width,self.height))
        self.board.fill((0,31,79))
        self.circle=pygame.draw.circle(self.board, (255,255,255),
                            (self.posx,self.posy), self.radius)
        
    def clamp(self, low, high, num):
        self.clamped=max(min(num, high), low)
        return self.clamped

    def draw(self,x,y):
        self.posx=self.clamp(0,self.width,self.posx+x)
        self.posy=self.clamp(0,self.height,self.posy+y)
        self.circle=pygame.draw.circle(self.board, (255,255,255),
                            (self.posx,self.posy), self.radius)

    def eventLoop(self): #Called after tkinter mainloop
        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        self.draw(0,-self.speed)
                    if event.key == pygame.K_DOWN:
                        self.draw(0,self.speed)
                    if event.key == pygame.K_LEFT:
                        self.draw(-self.speed,0)
                    if event.key == pygame.K_RIGHT:
                        self.draw(self.speed,0)

'''
ball = pygame.Rect(0,0,10,10)
while True:
    mainSurface.fill((0,0,0))
    pygame.draw.circle(display,(255,255,255),ball.center,5)
    ball.move_ip(1,1)
    pygame.display.update()'''

if __name__=="__main__":
    game = testPygame()
    game.eventLoop()
