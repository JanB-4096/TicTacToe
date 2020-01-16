%% NOTES %%
TicTacToe is a little project to learn about reinforcment learning for classic games. 
I feel like the code is very messy as this was more of a quick and early approach.
There is a lot of room for improvement in computing performance, expanding the searchspace, 
code structur, learning efficiency and neural net architecture.
I only wanted to see the differences between different layer parameter.


%% HOW-TO %%
__main__ can be used play the game itself
__trainNNModel__ is used to create or train an existing neural net
__evaluate__ is used to measure the win rate of the net


%% TODO %%
- clean up code and architecture
- More layers do not increase the win rate vs Random Player --> use other NN structur
- More neurons do not increase the win rate vs Random Player --> use other NN structur
- As the heuristic player always plays the same way, use another opponent --> 
    NN vs NN might be the best (see AlphaGoZero)
- When NN is trained vs heuristic player the NN seems to overfit and learns to always play 
    the same 2 games depending on which player starts, but not win 
    (it is possible to win vs the heuristic player) --> evaluate loss history
- Training can be done in batches --> also helpfull for loss history
- Do not reward a draw - you want the NN to win?!


%% CONCLUSIONS %%
- I can still beat any of the NN ... so far
- More layers and more neurons help the NN to learn winning vs the Heuristic Player --> 
    parameter tuning is important and annoying --> use AutoML or something similar or 
    programm a little automation
- Training vs a variaty of players might help the NN getting better
- 10000 games for training might not be enough for a RandomPlayer as opponent but might 
    be too many for a HeuristicPlayer as opponent
- I need more practice in buildiung NN  --> there is so much more to discover in TensorFlow :-D