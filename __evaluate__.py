from gameManager import GameOn
import time
from gameEnums import GameStatus

start = time.time()

go = GameOn()
go.setPlayers('nn', 'random')
#go.setPlayers('nn', 'heuristic')
go.loadNN('nnModel//TTT_L90_L360_L1080_L180_G10000_VSRandom.h5', 'p1')

numberOfEvalGames = 1000
numberOfWinsP1 = 0
numberOfWinsP2 = 0
numberOfDraws = 0

counter = 0
while counter < numberOfEvalGames:
    status = go.__run__()
    go.clearField()
    counter += 1
    if status is GameStatus.PLAYER_1_WON:
        numberOfWinsP1 +=1
    elif status is GameStatus.PLAYER_2_WON:
        numberOfWinsP2 +=1
    elif status is GameStatus.DRAW:
        numberOfDraws +=1
    
print("Number of Games played vs " + type(go.p2).__name__ + " Player: " + str(numberOfEvalGames))
print("Games won: " + str(numberOfWinsP1) + "   -->   Win rate: " + str(numberOfWinsP1/numberOfEvalGames))
print("Games lost: " + str(numberOfWinsP2) + "   -->   Loss rate: " + str(numberOfWinsP2/numberOfEvalGames))
print("Games drawes: " + str(numberOfDraws) + "   -->   Draw rate: " + str(numberOfDraws/numberOfEvalGames))
end = time.time()  
print("Finished Evaluation! Time elapsed in [s]: " + str(end-start))