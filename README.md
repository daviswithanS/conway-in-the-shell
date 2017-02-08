# Conway in the Shell
A version of Conway's Game of Life, written in Python, that works in the command line.

## create_board.py
Use this program to create custom boards (stored in /boards) that are usable in the main conway.py program.

## conway.py
This program will run the main simulation, using sample_board.p by default. If a board is not found, then it will generate a random grid of dots to carry out the simulation.

This program can be run with a number of flags to load custom boards or change the nature of the simulation.  

-b [name]  

>Use the file [name].p in /boards to load the board.  

-w  

>Wrap the simulation screen so that cells on the edge of the screen interact  ith those on the opposite edge.  

-d  

>Run the sumulation in debug mode.  
