import pygame as p

class Settings:
    
    def __init__(self):
        self.W = 900
        self.H = 900
        self.screen = p.display.set_mode((self.W, self.H))