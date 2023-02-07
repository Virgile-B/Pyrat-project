# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 19:08:12 2019

@author: Virgile
"""

TEAM_NAME = "DFS"

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###############################
import random
import numpy
###############################
visitedCells=[]
inf=100
a=0
###############################
def randomMove():
    moves = [MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP]
    return moves[random.randint(0,3)]

#returns the list of the moves the player can perform
def neighbors(location,maze):
    res=[]
    for neighbor in maze[location]:
        res.append(neighbor)
    return res

def moveFromLocations(sourceLocation, targetLocation) :
    difference = tuple(numpy.subtract(targetLocation, sourceLocation))
    if difference == (0, -1) :
        return MOVE_DOWN
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (-1, 0) :
        return MOVE_LEFT
    else :
        raise Exception("Impossible move")



def dead_end(neighbor,maze,pieces_of_cheese,):#returns whether or not the next move will lead to a dead_end
    #check the length of maze[neighbor] : if it is 1, it is a dead_end, now we also check if there is a cheese there...
    if len(maze[neighbor])==1 and neighbor not in pieces_of_cheese:
        return True
    else:
        return False

def listDiscoveryMoves(location, maze,pieces_of_cheese) : #returns the list of the unvisited places
    moves = []
    for neighbor in maze[location] :
        #if the neighbor wasnt't yet visited and isn't an empty dead_end...
        if neighbor not in visitedCells :
            #we go to this location
            moves.append(neighbor)
    return moves

# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is not expected to return anything
def preprocessing(maze, width, height, player1_location, player2_location, pieces_of_cheese, turn_time):
    pass
    # Example prints that appear in the shell only at the beginning of the game
    # Remove them when you write your own program

#get_steps_number = lambda turn: sum(1 for line in open(turn) if 'return' in line)
###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int, int)
# playerScore : float
# opponentScore : float
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is expected to return a move




def turn(maze, width, height, player1_location, player2_location, score1, score2, pieces_of_cheese, turn_time):
    #global visitedCells
    if player1_location not in visitedCells :
        visitedCells.append(player1_location)

    # v-- new code (we get the moves leading to a new cell and apply one of them at random if possible)
    moves = listDiscoveryMoves(player1_location,maze,pieces_of_cheese)
    #si moves n'est pas vide:
    if moves:
        return moveFromLocations(player1_location,moves[random.randint(0,len(moves)-1)])
        #return moveFromLocations(player1_location,moves[random.randint(0,len(moves)-1)])
    else :
#        alternative=chemin[1][player1_location]
#        return moveFromLocations(player1_location,alternative)
        return randomMove()