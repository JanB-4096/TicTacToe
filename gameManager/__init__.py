import numpy as np
from gameEnums import GameStatus, FieldState
from player import HumanPlayer, NPCHeuristic, NPCRandom, NPCNeuralNet
import copy


class GameManager():
    
    def __init__(self):
        self.field = np.full((3,3), FieldState.EMPTY) # field is 3x3 and one state with 3 posibilities (X, O, empty)
        self.status = GameStatus.RUNNING
        self.currentPlayer = FieldState(np.random.randint(1, 3))
        if self.currentPlayer is FieldState.X:
            self.oppononentPlayer = FieldState.O
        else:
            self.oppononentPlayer = FieldState.X
        
    def printCurrentPlayer(self):
        print("Player " + self.currentPlayer.name + " starts\n")

    def printField(self):
        print("r\c  " + str(0) + "     | " + str(1) + "     | " + str(2))
        space1 = "     "
        space2 = "     "
        for row in range(self.field.shape[0]):
            space1 = "     "
            space2 = "     "
            if self.field[row, 0] is FieldState.EMPTY:
                space1 = " "
            if self.field[row, 1] is FieldState.EMPTY:
                space2 = " "
            print(str(row) + "    " + self.field[row, 0].name + space1 + "| " + self.field[row, 1].name + space2 + "| " + self.field[row, 2].name)
            row += 1
        print("\n")
        
    def checkVictory(self):

        # check vertically and horizontally
        counter = self.field.shape[0]-1
        while counter >= 0:
            if np.all([self.field[counter,ii] is FieldState.X for ii in range(self.field.shape[0])]) or \
                np.all([self.field[ii,counter] is FieldState.X for ii in range(self.field.shape[0])]):
                self.status = GameStatus.PLAYER_1_WON
                print("Player X wins!\n")
                return True
            elif np.all([self.field[counter,ii] is FieldState.O for ii in range(self.field.shape[0])]) or\
                np.all([self.field[ii,counter] is FieldState.O for ii in range(self.field.shape[0])]):
                self.status = GameStatus.PLAYER_2_WON
                print("Player O wins!\n")
                return True
                
            counter -= 1

        # check diagonally
        if np.all([self.field[ii,ii] is FieldState.X for ii in range(self.field.shape[0])]) or \
            np.all([self.field[ii,self.field.shape[0]-1-ii] is FieldState.X for ii in range(self.field.shape[0])]):
            self.status = GameStatus.PLAYER_1_WON
            print("Player X wins!\n")
            return True
        elif np.all([self.field[ii,ii] is FieldState.O for ii in range(self.field.shape[0])]) or \
            np.all([self.field[ii,self.field.shape[0]-1-ii] is FieldState.O for ii in range(self.field.shape[0])]):
            self.status = GameStatus.PLAYER_2_WON
            print("Player O wins!\n")
            return True

        # check for a draw
        if np.any(self.field == FieldState.EMPTY):
            self.status = GameStatus.RUNNING
            return False
        else:
            self.status = GameStatus.DRAW
            print("It is a DRAW!\n")
            return True

    def changePlayer(self):
        if self.currentPlayer is FieldState.X:
            self.oppononentPlayer = FieldState.X
            self.currentPlayer = FieldState.O
        elif self.currentPlayer is FieldState.O:
            self.oppononentPlayer = FieldState.O
            self.currentPlayer = FieldState.X
        
    def makeMove(self, row, column):
        if row > self.field.shape[0]-1 or column > self.field.shape[1]-1 or self.field[row, column] is not FieldState.EMPTY:
            print("Move [" + str(row) +"," + str(column) + "] not allowed!\n Try again Player " + self.currentPlayer.name)
            return False
        
        self.field[row, column] = self.currentPlayer
        print("Field [" + str(row) +"," + str(column) + "] is set with " + self.currentPlayer.name + " :\n")
        self.changePlayer()
        self.printField()
        return True
    
    
    
class GameOn():
    
    def __init__(self, training = False):
        self.gm = GameManager() 
        self.isTraining = training
        
    def setPlayers(self, x = 'human', o = 'random'):
        if x is 'human':
            self.p1 = HumanPlayer(self.gm)
            print("Player X is set to human ...\n")
        elif x is 'random':
            self.p1 = NPCRandom(self.gm)
            print("Player X is set to random ...\n")
        elif x is 'heuristic':
            self.p1 = NPCHeuristic(self.gm)
            print("Player X is set to heuristic ...\n")
        elif x is 'nn':
            self.p1 = NPCNeuralNet(self.gm)
            print("Player X is set to neural net ...\n")
        
        if o is 'human':
            self.p2 = HumanPlayer(self.gm)
            print("Player O is set to human ...\n")
        elif o is 'random':
            self.p2 = NPCRandom(self.gm)
            print("Player O is set to random ...\n")
        elif o is 'heuristic':
            self.p2 = NPCHeuristic(self.gm)
            print("Player O is set to heuristic ...\n")
        elif o is 'nn':
            self.p2 = NPCNeuralNet(self.gm)
            print("Player O is set to neural net ...\n")
            
    def createNewModel(self, player = 'p1', layers = []):
        if player is 'p1' and isinstance(self.p1, NPCNeuralNet):
            self.p1.createNewNN(layers)
        elif player is 'p2' and isinstance(self.p2, NPCNeuralNet):
            self.p2.createNewNN(layers) 
    
    def __run__(self):
        if self.isTraining:
            self.__train__()
        else:
            self.__play__()
            return(self.gm.status)
            
    def __play__(self):
        self.gm.printField()
        self.gm.printCurrentPlayer()
        
        gameFinished = False

        # game in progress
        while gameFinished is False:
            if self.gm.currentPlayer is FieldState.X:
                coord = self.p1.calculateMove()
                self.gm.makeMove(coord[0], coord[1])
            else:
                coord = self.p2.calculateMove()
                self.gm.makeMove(coord[0], coord[1])

            gameFinished = self.gm.checkVictory()

    def __train__(self):
        self.gm.printField()
        self.gm.printCurrentPlayer()
        
        gameFinished = False
        fieldP1 = []
        movesP1 = []
        fieldP2 = []
        movesP2 = []

        # game in progress
        while gameFinished is False:
            if self.gm.currentPlayer is FieldState.X:
                fieldP1.append(copy.deepcopy(self.gm.field))
                coord = self.p1.calculateMove()
                self.gm.makeMove(coord[0], coord[1])
                movesP1.append(coord)
            else:
                fieldP2.append(self.gm.field)
                coord = self.p2.calculateMove()
                self.gm.makeMove(coord[0], coord[1])
                movesP2.append(coord)

            gameFinished = self.gm.checkVictory()
            
        if self.gm.status is GameStatus.PLAYER_1_WON:
            rewardP1 = 1
            rewardP2 = 0
        elif self.gm.status is GameStatus.PLAYER_2_WON:
            rewardP1 = 0
            rewardP2 = 1
        elif self.gm.status is GameStatus.DRAW:
            rewardP1 = 0.01
            rewardP2 = 0.01
        if isinstance(self.p1, NPCNeuralNet):
            for idx in range(movesP1.__len__()):
                self.p1.train(fieldP1[idx], movesP1[idx], rewardP1)
        if isinstance(self.p2, NPCNeuralNet):
            for idx in range(movesP2.__len__()):
                self.p2.train(fieldP2[idx], movesP2[idx], rewardP2)
            
    def saveNN(self, fileName, player = 'p1'):
        if player is 'p1' and isinstance(self.p1, NPCNeuralNet):
            self.p1.saveNN(fileName)
        elif player is 'p2' and isinstance(self.p2, NPCNeuralNet):
            self.p2.saveNN(fileName)

    def loadNN(self, fileName, player = 'p1'):
        if player is 'p1' and isinstance(self.p1, NPCNeuralNet):
            self.p1.loadNN(fileName)
        elif player is 'p2' and isinstance(self.p2, NPCNeuralNet):
            self.p2.loadNN(fileName)

    def clearField(self):
        self.gm.field = np.full((3,3), FieldState.EMPTY)
