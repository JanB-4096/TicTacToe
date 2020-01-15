from gameManager import GameOn
import time

start = time.time()

go = GameOn(training = True) # training mode is true
go.setPlayers('nn', 'random')
#go.setPlayers('nn', 'heuristic')
go.createNewModel('p1', [90, 360, 1080, 180]) # only deep layers have to be defined for ne NN
#go.loadNN(nnModel//TTT_L18_L36_G10000_VSRandom.h5', 'p1') # continue training

numberOfTrainingGames = 10000
counter = 0
while counter < numberOfTrainingGames:
    # TODO: evaluate loss history to evade over-fitting
    go.__run__()
    go.clearField()
    counter += 1
    
go.saveNN('nnModel//TTT_L90_L360_L1080_L180_G10000_VSRandom.h5', 'p1')

end = time.time()  
print("Finished Training! Time elapsed in [s]: " + str(end-start))