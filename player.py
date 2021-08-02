import pygame as p
from settings import Settings
import os

class Player(p.sprite.Sprite):
    
    def __init__(self, side):
        super().__init__()
        self.side = side
        self.settings = Settings()
        self.image = p.image.load(self.getImagePath())
        self.image = p.transform.scale(self.image, (self.settings.W // 3, self.settings.H // 3))
        self.rect = self.image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        
    
    def getImagePath(self):
        filepath = os.path.dirname(__file__)
        return os.path.join(filepath, "img", self.side + ".png")
    
