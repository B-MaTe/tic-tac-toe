import pygame as p
from settings import Settings
from player import Player
from math import ceil

p.init()
class Main:
    
    def __init__(self):
        self.settings = Settings()
        self.screen = self.settings.screen
        self.active = True
        self.figures = p.sprite.Group()
        self.turn = "x"
        self.filledPositions = []
        self.gameEnd = False
        self.restart = False
        self.winFound = False
        self.level = None
        self.computerSide = self.settings.computerSide
        
        
    def createTable(self):
        # COLUMNS
        p.draw.line(self.screen, self.settings.lineColor, (self.settings.W / 3, 0), (self.settings.W / 3, self.settings.H), self.settings.lineW)
        p.draw.line(self.screen, self.settings.lineColor, (2 * self.settings.W / 3, 0), (2 * self.settings.W / 3, self.settings.H), self.settings.lineW)
        
        # ROWS
        p.draw.line(self.screen, self.settings.lineColor, (0, self.settings.H / 3), (self.settings.W, self.settings.H / 3), self.settings.lineW)
        p.draw.line(self.screen, self.settings.lineColor, (0, 2 * self.settings.H / 3), (self.settings.W, 2 * self.settings.W / 3), self.settings.lineW)
        
    
    def makeMove(self, x, y, computerMove = False):
        
        figure = Player(self.turn)
        
        if computerMove:
            figure.x, figure.y = x * self.settings.W / 3, y * self.settings.H / 3
            figure.rect.x, figure.rect.y = figure.x, figure.y
            self.figures.add(figure)
            
            ### Add to filled positions
            self.filledPositions.append([x, y, self.turn])
            
            ### Change turn
            self.changeTurn()
        else:
            figure.x, figure.y, x, y = self.moveToPosition(x, y)
            if not self.checkColission(x, y):
                figure.rect.x, figure.rect.y = figure.x, figure.y
                self.figures.add(figure)
                
                ### Add to filled positions
                self.filledPositions.append([x, y, self.turn])
                
                ### Change turn
                self.changeTurn()
                
            else:
                figure.kill()
                    
    
    def changeTurn(self):
        self.turn = self.settings.swapTurn[self.turn]
        winner = self.checkGameEnd()
       
        if winner:
            self.gameEnd = True
            if winner == "tie":
                self.gameEndFont = self.settings.gameEndFont.render(f"It's a draw!", True, (self.settings.fontColor))
            else:
                self.gameEndFont = self.settings.gameEndFont.render(f"{self.settings.sides[winner]} won!", True, (self.settings.fontColor))

 
    
    def checkColission(self, x, y):
        if self.filledPositions:
            for pos in self.filledPositions:
                if pos[0] == x and pos[1] == y:
                    return True
        return False
        
    
    def moveBack(self, move, side):
        self.filledPositions.remove([move[0], move[1], side])

    
    def getPossibleMoves(self):
        possibleMoves = []
        for i in range(3):
            for j in range(3):
                found = False
                for pos in self.filledPositions:
                    if [pos[0], pos[1]] == [i, j]:
                        found = True
                if not found:
                    possibleMoves.append([i, j])
        return possibleMoves
                
                
    def minimax(self, depth, isMaximising, side):
        result = self.checkGameEnd()
        if result:
            return self.settings.scores[result]
        
        moves = self.getPossibleMoves()
        
        if isMaximising:
            bestMove = -9999
            for move in moves:
                self.filledPositions.append([move[0], move[1], side])
                newMove = self.minimax(depth - 1, not isMaximising, side)
                self.moveBack(move, side)
                if newMove == 1:
                    return newMove
                bestMove = max(bestMove, newMove)
            return bestMove
        
        else:
            bestMove = 9999
            for move in moves:
                self.filledPositions.append([move[0], move[1], self.settings.swapTurn[side]])
                newMove = self.minimax(depth - 1, not isMaximising, side)
                self.moveBack(move, self.settings.swapTurn[side])
                if newMove == -1:
                    return newMove
                bestMove = min(bestMove, newMove)
            return bestMove
                
                
    def minimaxRoot(self, depth, isMaximising, side):
        moves = self.getPossibleMoves()
        bestMoveVal = -9999
        bestMove = None
        for move in moves:
            self.filledPositions.append([move[0], move[1], side])
            newMove = self.minimax(depth - 1, not isMaximising, side)
            self.moveBack(move, side)
            if newMove == 1:
                return move
            elif newMove >= bestMoveVal:
                    bestMoveVal = newMove
                    bestMove = move
        return bestMove
            
    
    def getBestMove(self, level, side):
       move = self.minimaxRoot(level, True, side)
       return move
   
        
    def computerMove(self, side, level):
        if self.turn == side:
            if not level:
                level = 10 - len(self.figures)
            move = self.getBestMove(level, side)
            self.makeMove(move[0], move[1], True)
        
        
    def checkGameEnd(self):        
        ### ROWS
        for i in range(3):
            team = None
            figureCounter = 0
            for pos in self.filledPositions:
                if pos[1] == i:
                    if not team:
                        team = pos[-1]
                        figureCounter += 1
                    elif pos[-1] == team:
                        figureCounter += 1
                    else:
                        break
            if figureCounter == 3:
                return team
        ### COLUMNS
        for k in range(3):
            team = None
            figureCounter = 0
            for pos in self.filledPositions:
                if pos[0] == k:
                    if not team:
                        team = pos[-1]
                        figureCounter += 1
                    elif pos[-1] == team:
                        figureCounter += 1
                    else:
                        break
            if figureCounter == 3:
                return team
        ### DIAGONALS
        team = None
        figureCounter = 0
        foundL = False
        if [0,0, 'x'] in self.filledPositions:
            team = "x"
            foundL = True
        elif [0,0, 'o'] in self.filledPositions:
            team = "o"
            foundL = True
            ### LEFT TO RIGHT DIAGONAL
        if foundL:
            for pos in self.filledPositions:
                if [pos[0], pos[1]] == [1,1]:
                    if pos[-1] == team:
                        figureCounter += 1
                    else:
                        break
                elif [pos[0], pos[1]] == [2,2]:
                    if pos[-1] == team:
                        figureCounter += 1
                    else:
                        break
            if figureCounter == 2:
                return team
        figureCounter = 0
        foundR = False
        if [2,0, 'x'] in self.filledPositions:
            team = "x"
            foundR = True
        elif [2,0, 'o'] in self.filledPositions:
            team = "o"
            foundR = True
            ### RIGHT TO LELT DIAGONAL
        if foundR:
            for pos in self.filledPositions:
                if [pos[0], pos[1]] == [1,1]:
                    if pos[-1] == team:
                        figureCounter += 1
                    else:
                        break
                elif [pos[0], pos[1]] == [0,2]:
                    if pos[-1] == team:
                        figureCounter += 1
                    else:
                        break
            if figureCounter == 2:
                return team
            
        if len(self.filledPositions) == 9:
            return "tie"
        return False
                    
    
    def moveToPosition(self, x, y):
        if x < self.settings.W / 3:
            x = 0
        elif self.settings.W / 3 < x < 2 * self.settings.W / 3:
            x = 1
        else:
            x = 2
        if y < self.settings.H / 3:
            y = 0
        elif self.settings.H / 3 < y < 2 * self.settings.H / 3:
            y = 1
        else:
            y = 2
        return x * self.settings.W / 3, y * self.settings.H / 3, x, y
    
    
    
    def events(self):
        if self.turn == self.computerSide:
            if not self.gameEnd:
                if len(self.figures) < 9:
                    self.computerMove(self.computerSide, self.level)
                    
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.gameEnd:
                        self.makeMove(event.pos[0], event.pos[1])
                        
            elif event.type == p.QUIT:
                self.active = False
                
            elif event.type == p.KEYDOWN:
                if event.key == p.K_p:
                    self.active = False
                elif event.key == p.K_r:
                    self.restart = True
    
    def run(self):
       
        ### BG
        self.screen.fill(self.settings.bgColor)
        
        ### ADD FIGURES
        self.figures.draw(self.screen)
        self.figures.update()
         ### GameEnd
        if self.gameEnd:
            self.screen.blit(self.gameEndFont, (self.screen.get_width() / 3, self.screen.get_height() / 3))
        ### BOARD
        self.createTable()
        
        
        p.display.flip()

p.quit()