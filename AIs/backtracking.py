# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 07:37:31 2019

@author: Virgile
"""
TEAM_NAME = "backtracking"

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
import heapq
###############################
visitedCells=[] #list of visited vertex
inf=10000 #infinity

###############################
#returns a random move
def randomMove():
    moves = [MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP]
    return moves[random.randint(0,3)]

#returns the list of the moves the player can perform
def neighbors(location,maze):
    res=[]
    # for neighbors around the actual rat's location :
    for neighbor in maze[location]:
        res.append(neighbor)
    return res

#
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


#returns whether or not the next move will lead to a dead_end
def dead_end(neighbor,maze,pieces_of_cheese,):
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


#path returns the path to go from A to B using BFS/DFS
def path(end,begin):
    #we initialize the path list with the end
    the_path=[end]
    #we initialize the immaginary location we are on
    location=end
    #while we didn't reach the end:
    while location!=begin:
        #we add the child of the actual vertex to path
        the_path.append(actual_dijkstra[0][location])
        #we change location so it stops
        location=actual_dijkstra[0][location]
    return list(reversed(the_path))

#this function will be called at the begin then each time a cheese is taken
#clothes_cheese returns 
#def closest_cheese(position,pieces_of_cheese):
#    closest=chemin[1][pieces_of_cheese[0]]
#    cheese_index=0
#    for i in range(len(pieces_of_cheese)):
#          if chemin[1][pieces_of_cheese[i]]<closest:
#              closest=chemin[1][pieces_of_cheese[i]]
#              cheese_index+=1
#    pieces_of_cheese.pop(cheese_index)

def add_or_replace(heap,couple):
    exists=False
    for i in range(len(heap)):
        if heap[i][0]==couple[0]:
            exists=True
            if heap[i][1]>couple[1]:
                heap[i]=couple
    if exists==False:
        heapq.heappush(heap,couple)

#returns the shortest path from an initial vertex to every vertex of the map and the distance between those 2 vertex.                
def dijkstra(maze, start_vertex):
    # initialize every distances between the starting vertex and the rest of the graph as inifnite 
    distances={location:inf for location in maze}
    #we define what will be our routing table as a dictionnary
    road={}  
    #we initialize our min_heap as an empty list
    min_heap=[]
    #we add the sart_vertex to the min_heap with the heap method
    heapq.heappush(min_heap,(start_vertex,0))
    #we initialise the distance from the start_ertex to the start_vertex as 0
    distances[start_vertex]=0
    # while the min_heap isn't empty:
    while min_heap!=[]:
        #the tackled vertex v and the distance from the current vertex to the new one (v_distance) are defined
       v ,v_distance= heapq.heappop(min_heap)
       #for every neighbor of v:
       for neighbor in maze[v]:
           #the total distance from start_vertex to v is defined as the sum of the previous distance plus the new one
            distance_through_v = v_distance + maze[v][neighbor]
            #is this distance is smaller than the other possibilities purposed by the neighbors:
            if distance_through_v < distances[neighbor]:
                #we keep v as the child of neighbor
                road[neighbor]=v
                #and we keep distance_through_v as the smallest distance from start_vertex to v
                distances[neighbor]=distance_through_v
                #we apply heap append to this couple
                add_or_replace(min_heap,(neighbor,distance_through_v))
    return road,distances

#has 2 arguments:the location and the map
#returns the distance from the location defined in the Dijsktra currently used (the current "chemin")
def length(location,maze):
    return actual_dijkstra[1][location]

#returns the graph containing the rat location and the list of the positions of all cheeses and returns the etagraph of those elements
# so it basicly returns the paths and lengths between every 2 elements of the list [cheeses,player1_location]
def metagraph(location,maze,pieces_of_cheese):
    # we defined our list containing all cheeses and rat location with the cheeses:
    l_pos=pieces_of_cheese[:]
    #we also add the rat_location
    l_pos.append(location)
    #we must define our mgraph as a dictionary
    mgraph={}
    #i will add the path for all couples in l_pos
    for vertex in l_pos:
        #again, mgraph[vertex] has to be a dictionnary
        mgraph[vertex]={}
        #we compute a dijkstra for every pieces in l_pos
        global actual_dijkstra
        actual_dijkstra=dijkstra(maze,vertex)
        for vertex2 in l_pos:
            #if the 2nd vertex isn't the same as the 1st one
            if vertex2!=vertex:
                # we add both the path and the length to the travel (vertex,vertex2)
                actual_path=path(vertex2,vertex)
                #actual_dijkstra[1][vertex2] if the length to go from vertex to vertex2
                mgraph[vertex][vertex2]=actual_path,actual_dijkstra[1][vertex2]
    return mgraph


best=inf
best_path=[]       
#backtracking is pretty much the same as bruteforce but with an "if" condition       
def backtracking(remaining, vertex, path, weight, trajet,player1_location):
    global best
    global best_path
    #to gain time, we compare weight with best
    if weight<best:
        #if remaining (which countain pieces of cheese at the beginning) is empty
        if not remaining:
            #we compare the final weight of the path with the best weight
            if weight<best:
                #if the final weight for this path is smaller than the best weight so far
                best=weight
                #the best path is changed as the actual path
                best_path = path
        else:
            #if the remaining list isn't empty for each vertex v in remaining:
            for v in remaining:
                    #we delete the vertex from remaining
                    remaining_withoutv = remaining[:]
                    del remaining_withoutv[remaining_withoutv.index(v)]
                    #we compute bruteforce for the new "remaining" list and the path plus the vertex, and the weight + the weight to go to vertex to v
                    backtracking(remaining_withoutv, v, path+[v], weight+ trajet[vertex][v][1], trajet,player1_location)


#preprocessing is called at the beginning of the pyrat game
def preprocessing(maze, width, height, player1_location, player2_location, pieces_of_cheese, turn_time):
    #we will use chemin in turn so it has to be global
 #   global chemin
    # same as chemin
    global trajet
    global destination

    #chemin is the complete DFS with the path and the routing table
    #trajet is the actual path that our rat will take to go to the location
   # print(destination)
   #necessary because without this sleep time, "key error" issues
    trajet=metagraph(player1_location,maze,pieces_of_cheese)
    backtracking(pieces_of_cheese, player1_location, [], 0, trajet,player1_location)
    best_path.append(player1_location)
    print(best_path)
    

    
 #turn is called for each move of the rat/python   
def turn(maze, width, height, player1_location, player2_location, score1, score2, pieces_of_cheese, turn_time):
#        while we didn't reach the next vertex to be visited:
    if len(trajet[best_path[-1]][best_path[-2]][0])>1:
        #our move is defined as the move to get closer to best_path[-2] which is the next vertex to be visited
        move=trajet[best_path[-1]][best_path[-2]][0].pop(1)
        return moveFromLocations(player1_location,move)
    else :
        #if we reached our destination:
        #we deleete the just-visited vertex of best_path
        best_path.pop()
        #and we do the same thing as before
        move=trajet[best_path[-1]][best_path[-2]][0].pop(1)
        return moveFromLocations(player1_location,move)