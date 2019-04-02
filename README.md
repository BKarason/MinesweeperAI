# MinesweeperAI

## About MineSweeperAI
A minsweeper solving agent, that solves minsweeper using basic logic and a tank solver algorithm. Written in Python

## Running MinesweeperAI
Run MineSweeper.py, this will run mineSweeper on a beginner board (9\*9 board with 10 bombs) 100 times and tell you how many times he won and how many times he lost.

## Changing the grid size , bomb count, and how many times it runs
To change the size of the grid you have to modify the gridsize variable in the playgame function (line 149), to change the amount of bombs you have to change the numberofmines variable in the playgame function (line 150), and to change the how many times the agent solves the board you have to change two lines, on lines 206 and line 224 there are identical lines that at first say "if i != 99" you have to change 99 to your desired value - 1, i.e. to run 10 times you change 99 to 9.