import pygame as p
from main import Main
from settings import Settings

class Run:
    
    def __init__(self):
        self.main = Main()
        self.settings = Settings()
        self.process()
        
    def process(self):
        while self.main.active:
            self.main.run()
            self.main.events()
            if self.main.restart:
                self.main.restart = False
                p.quit()
                Run()
        
        
if __name__ == '__main__':
    Run()