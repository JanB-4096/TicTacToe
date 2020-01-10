from gameEnums import FieldState
import numpy as np
import itertools
import copy



class Player():
        
    def checkValidity(self, row, col):
        if self.gm.field[row,col] is FieldState.EMPTY:
            return True
        else:
            return False
        
    def getNeighbours(self, row, col):
        rowNeigh = [row]
        colNeigh = [col]
        if row+1 < self.gm.field.shape[0]:
            rowNeigh.append(row+1)
        if row-1 >= 0:
            rowNeigh.append(row-1)
        if col+1 < self.gm.field.shape[1]:
            colNeigh.append(col+1)
        if col-1 >= 0:
            colNeigh.append(col-1)
        
        return list(itertools.product(rowNeigh, colNeigh))
        
        
class HumanPlayer(Player):
    def __init__(self, gm):
        self.gm = gm
    
    def calculateMove(self):
        again = True
        while again:
            row = int(input('Please enter a row: '))
            col = int(input('Please enter a column: '))
            
            if row >= 0 and row <=2 and col >= 0 and col <= 2:
                again = False
            else:
                print('Incorrect input. Please try again Player ' + self.gm.currentPlayer.name)
                again = True
        
        return [row, col]
    
    
            
class NPCHeuristic(Player):
    def __init__(self, gm):
        self.gm = gm
            
    def calculateValueOfField(self, row, col):
        # heuristic is not set to be optimal and can loose - a NN shall try 
        # to beat this heuristic player later
        if self.gm.field[row, col] is FieldState.EMPTY:
            
            # reward a set of 2 next to each other with
            neighbours = self.getNeighbours(row, col)
            valueNeigh = 0
            for pos in neighbours:
                if self.gm.field[pos[0], pos[1]] is self.gm.currentPlayer:
                    valueNeigh += 0.2
            
            # reward setting a field where the opponent has 2 next to it
            valueBacklash = 0
            if self.gmCopy.currentPlayer is FieldState.X:
                self.gmCopy.field[row, col] = FieldState.O
            elif self.gmCopy.currentPlayer is FieldState.O:
                self.gmCopy.field[row, col] = FieldState.X
            if self.gmCopy.checkVictory():
                valueBacklash = 0.6
            self.gmCopy.field[row, col] = FieldState.EMPTY # set field back to empty
            
            
            # reward getting the middle if none else is reasonable
            valueMiddle = 0.1 * int(row is 1) * int(col is 1)
            
            # reward getting 3 in on direction the most
            if self.gm.checkVictory() is True:
                valueWin = 1
            else:
                valueWin = 0
                
            return valueMiddle + valueWin + valueNeigh + valueBacklash
        else:
            return 0
    
    def calculateMove(self):
        self.gmCopy = copy.deepcopy(self.gm)
        
        value = np.full((3,3), 0.0)
        for row in range(0, self.gm.field.shape[0]):
            for col in range(0, self.gm.field.shape[1]):
                value[row, col] = self.calculateValueOfField(row, col)
                
        if np.any(value.__eq__(0) == False):
            coord = np.where(value == np.max(value))
            return [coord[0][0], coord[1][0]]
        else:
            return NPCRandom.calculateMove(self)
    

    
class NPCRandom(Player):
    def __init__(self, gm):
        self.gm = gm
        
    def calculateMove(self):
        isValidMove = False
        while not isValidMove:
            row = np.random.randint(0, 3)
            col = np.random.randint(0, 3)
            isValidMove = self.checkValidity(row, col)
            
        return [row, col]
    
    
    
class NPCSearch(Player):
    # TODO: explore whole workspace and take the best chances
    def __init__(self, gm):
        self.gm = gm
        
    def calculateMove(self):
        isValidMove = False
        while not isValidMove:
            
            row = np.random.randint(0, 3)
            col = np.random.randint(0, 3)
            
            
            isValidMove = self.checkValidity(row, col)
            
        return [row, col]
        



