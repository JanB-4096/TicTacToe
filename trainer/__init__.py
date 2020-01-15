import tensorflow as tf
import numpy as np
from gameEnums import FieldState
import copy


class NNModel():  
    def __init__(self, gm):
        self.gm = gm      
    
    def createNewNN(self, layers = []):
        # create sequential NN and add first layer with 9 inputs
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Flatten())
        
        # add layers from input
        for index in range(layers.__len__()):
            self.model.add(tf.keras.layers.Dense(layers[index], activation='relu', kernel_initializer = tf.keras.initializers.RandomNormal()))
        self.model.add(tf.keras.layers.Dense(9, activation='softmax', kernel_initializer = tf.keras.initializers.RandomNormal()))

        # add last layer for output
        self.model.add(tf.keras.layers.Flatten())
        
        # set compiler parameter
        self.model.compile(optimizer='adam', loss = 'binary_crossentropy', metrics=['accuracy'])
                
                
    def loadNN(self, fileName):   
        self.model = tf.keras.models.load_model(fileName)
        
    def saveNN(self, fileName):
        self.model.compile(optimizer='adam', loss = 'binary_crossentropy', metrics=['accuracy'])
        self.model.save(fileName)
        
    def train(self, field, move, reward, epochs = 10):
        normalizedField = self.normalizeField(field)
        normalizedMove = self.normalizeMove(move, reward)
        self.model.fit(x=normalizedField, y=normalizedMove, epochs = epochs)

    def predict(self):
        # predict the best move with the given field state
        normalizedField = self.normalizeField(self.gm.field)
        prediction = self.model.predict(normalizedField)
        
        return(prediction.reshape(3,3))
        
    def normalizeField(self, field):
        # transform the game field, so that the current player always uses the same number 1
        normalizedField = copy.deepcopy(field)
        normalizedField[normalizedField == self.gm.currentPlayer] = 1
        normalizedField[normalizedField == self.gm.oppononentPlayer] = -1
        normalizedField[normalizedField == FieldState.EMPTY] = 0
        return(normalizedField.reshape(1,9))
    
    def normalizeMove(self, move, reward = 1):
        if reward != 0:
            moveField = np.full((3,3), 0)
            moveField[move[0],move[1]] = reward
        else:
            moveField = np.full((3,3), 0)
            moveField[self.gm.field == FieldState.EMPTY] = 0.125 # every empty field is better then the chosen one because it lead to a loss
            moveField[move[0],move[1]] = 0
        return (moveField.reshape(1,9))