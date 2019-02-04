'''
Menu and Commands
'''

from tkinter import simpledialog
from tkinter import colorchooser

class Commander:
    def __init__(self,parent):
        self.__parent = parent
        self.__keyBinds = {
            'q':self.__kill,'b':self.__bgColor,'m':self.__mosaicChange,
            'c':self.__coordChange,'r':self.__resetWindowSize
        }
        self.__configOpen = False
        self.__parent.getBase().bindKeys(**self.__keyBinds)

    def __kill(self, event=None):
        self.__parent.getBase().getUi().destroy()

    def __bgColor(self, event=None):
        if not(self.__configOpen):
            self.__configOpen = True
            initCol=list(self.__parent.getCanvas()['background'].split('#')[-1])
            initR=int(initCol[0]+initCol[1],16)
            initG=int(initCol[2]+initCol[3],16)
            initB=int(initCol[4]+initCol[5],16)
            color=colorchooser.askcolor(title='New Background Color',initialcolor=(initR,initG,initB))[1]
            self.__parent.getBase().getUi()['background']=color
            self.__parent.getCanvas()['background']=color
            self.__configOpen = False

    def __mosaicChange(self, event=None):
        self.__parent.swapMosaic()

    def __coordChange(self, event=None):
        if not(self.__configOpen):
            self.__configOpen = True
            newcoords = simpledialog.askstring(title='Coord Change',prompt='New Coords x,y:')
            if type(newcoords) == str:
                newcoords = newcoords.split(',')
                newcoords = [min(max(int(x),1),self.__parent.getWorldSize()[newcoords.index(x)]) for x in newcoords]
                self.__parent.setPlayerPos(newcoords)
                self.__parent.colorWorld()
            self.__configOpen = False

    def __resetWindowSize(self, event=None):
        self.__parent.getBase().setSize()
