import pygame as p
from settings import Settings

p.init()
class Main:
    
    def __init__(self):
        self.settings = Settings()
        self.screen = self.settings.screen
        
        
    def run(self):
        self.screen.fill((255, 255, 255))
        
        p.display.flip()