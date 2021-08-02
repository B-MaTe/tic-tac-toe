import pygame as p
from main import Main

class Run:
    
    def __init__(self):
        self.main = Main()
        self.active = True
        self.process()
        
    def process(self):
        while self.active:
            self.main.run()
        
        
if __name__ == '__main__':
    Run()