import pygame as p

class Settings:
    
    def __init__(self):
        self.W = 700
        self.H = 700
        self.screen = p.display.set_mode((self.W, self.H))
        self.bgColor = (200,200,200)
        self.lineColor = (0, 0, 0)
        self.lineW = 5
        self.swapTurn = {
            "o" : "x",
            "x" : "o"
        }
        self.fontSize = 70
        self.fontColor = (27, 22, 156)
        p.font.init()
        self.gameEndFont = p.font.SysFont("leelawadeeuisemilight", self.fontSize, True, True)
        self.scores = {
            "x" : 1,
            "o" : -1,
            "tie" : 0
        }
        
        self.sides = {
            "x" : "MSZP",
            "o" : "FIDESZ"
        }
        
        
    def setWH(self, w, h):
        self.W = w
        self.H = h