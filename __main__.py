from gameManager import GameOn

if __name__ == '__main__':
    retry = True
    while retry:
        go = GameOn()
        go.setPlayers('nn', 'heuristic')
        go.loadNN('nnModel//tttModel.h5', 'p1') # decide which NN should play
        go.__run__()
        
        again = True
        while again:
            decision = input('Retry? [y/n] ')
            if decision is 'y':
                retry = True
                again = False
            elif decision is 'n':
                retry = False
                again = False
            else:
                print('Incorrect input. Please enter <y> or <n>.')
                again = True
            