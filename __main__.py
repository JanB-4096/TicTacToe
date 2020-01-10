'''
Created on 08.01.2020

@author: jberger
'''
from gameManager import GameOn

if __name__ == '__main__':
    retry = True
    while retry:
        go = GameOn()
        go.setPlayers('random', 'heuristic')
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
            