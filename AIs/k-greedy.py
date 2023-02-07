# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 08:46:24 2019

@author: Virgile
"""
TEAM_NAME = "k-greedy"


###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
# =============================================================================
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
# =============================================================================

# =============================================================================
import random
import numpy
import heapq
# =============================================================================

# =============================================================================
visitedCells=[] #list of visited vertex
inf=10000 #infinity
# =============================================================================

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


# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.

# =============================================================================
# # Arguments are:
# # mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# # mazeWidth : int
# # mazeHeight : int
# # playerLocation : pair(int, int)
# # opponentLocation : pair(int,int)
# # piecesOfCheese : list(pair(int, int))
# # timeAllowed : float
# =============================================================================

# This function is not expected to return anything

    # Example prints that appear in the shell only at the beginning of the game
    # Remove them when you write your own program

#get_steps_number = lambda turn: sum(1 for line in open(turn) if 'return' in line)
###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).

# =============================================================================
# # Arguments are:
# # mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# # mazeWidth : int
# # mazeHeight : int
# # playerLocation : pair(int, int)
# # opponentLocation : pair(int, int)
# # playerScore : float
# # opponentScore : float
# # piecesOfCheese : list(pair(int, int))
# # timeAllowed : float
# =============================================================================

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
                mgraph[vertex][vertex2]=actual_path,length(vertex2,maze)
    return mgraph

def length(location,maze):
    return actual_dijkstra[1][location]


# =============================================================================
# # The bruteforce function is called once during the preprocessing
# # ------------------------------------------------------------
# # remaining : defined at the beginning as pieces_of_cheese, then changed as bruteforce() is executed
# # path : initially defined as empty, fill-up as bruteforce() is called
# # weight : initially equal to 0, increases when bruteforce() is called
#     #trajet : our actual metagraph
# # pieces_of_cheese : list(pair(int, int))
# # player1_location: location of the player, we we only consider the initial one
# =============================================================================
#the bruteforce algorithm
#we define best as inf and best_path as None for now
best=inf
best_path=[]
#it returns nothing but best and best_path are global
def bruteforce(remaining, vertex, path, weight,player1_location):
    global best
    global best_path
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
                bruteforce(remaining_withoutv, v, path+[v], weight+ trajet[vertex][v][1],player1_location)


def clothest_cheese(maze,pieces_of_cheese,location):
    global mgraph_list
    best_weight=inf
    best_cheese=None
    print('mg av',mgraph_list)
#    if len(mgraph_list)<3:
#        if mgraph_list[0]==location:
#            return mgraph_list[1]
#        else:
#            return mgraph_list[0]
    for vertex in mgraph_list:
        if vertex!=location:
            weight=trajet[location][vertex][1]
            if weight<best_weight:
                best_weight=weight
                best_cheese=vertex
    result=mgraph_list.pop(mgraph_list.index(best_cheese))
    print('mg ap',mgraph_list)
    return result

#def clothest_cheese_during_game(maze,location,player1_location,player2_location):
#    best_weight=inf
#    for vertex in mgraph_list:
#        if vertex!=location:
#            if location==player1_location:
#                weight=new_dijkstra_rat[location][vertex][1]
#            elif location==player2_location:
#                weight=new_dijkstra_pyth[location][vertex][1]
#            if weight<best_weight:
#                best_weight=weight
#                best_cheese=vertex
#    result=mgraph_list.pop(mgraph_list.index(best_cheese))
#    return result  


def next_2_cheeses(maze,pieces_of_cheese,location):
    next_cheeses=[]
    for i in range(2):
        next_cheeses.append(clothest_cheese(maze,pieces_of_cheese,location))
    return next_cheeses

def next_3_cheeses(maze,pieces_of_cheese,location):
    next_cheeses=[]
    for i in range(3):
        next_cheeses.append(clothest_cheese(maze,pieces_of_cheese,location))
    return next_cheeses
    

##############################################################
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
# ------------------------------------------------------------
# maze_map : dict(pair(int, int), dict(pair(int, int), int))
# maze_width : int
# maze_height : int
# player_location : pair(int, int)
# opponent_location : pair(int,int)
# pieces_of_cheese : list(pair(int, int))
# time_allowed : float
##############################################################
def preprocessing(maze, width, height, player1_location, player2_location, pieces_of_cheese, turn_time):
    #we will use chemin in turn so it has to be global
 #   global chemin
    # same as chemin
    global trajet
#    global destination
    global really_best_path
    global mgraph_list
    mgraph_list=pieces_of_cheese[:]
    #chemin is the complete DFS with the path and the routing table
    #trajet is the actual path that our rat will take to go to the location
    trajet=metagraph(player1_location,maze,pieces_of_cheese)
 #   we execute bruteforce() in order to get best_path
   # bruteforce(pieces_of_cheese,player1_location,[],0,player1_location)
    bruteforce(next_2_cheeses(maze,pieces_of_cheese,player1_location),player1_location,[],0,player1_location)
    really_best_path=list(reversed(best_path))
    really_best_path.append(player1_location)



    

##############################################################
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
# ------------------------------------------------------------
# maze_map : dict(pair(int, int), dict(pair(int, int), int))
# maze_width : int
# maze_height : int
# player_location : pair(int, int)
# opponent_location : pair(int,int)
# player_score : float
# opponent_score : float
# pieces_of_cheese : list(pair(int, int))
# time_allowed : float
##############################################################   
def turn(maze, width, height, player1_location, player2_location, score1, score2, pieces_of_cheese, turn_time):
    global really_best_path
    global best
    global mgraph_list
    for i in pieces_of_cheese:
        if player2_location==i:
            if mgraph_list.count(i)>0:
                mgraph_list.pop(mgraph_list.index(i))
#    for k in really_best_path:
#        if player2_location==k:
#            really_best_path.pop(really_best_path.index(k))
#            really_best_path.append(clothest_cheese(maze,pieces_of_cheese,really_best_path[0]))
  #  global the_next_cheeses
# to reduces computing for a single turn :
#    if len(really_best_path)==3 and len(mgraph_list)>1:
#        the_next_cheeses=next_2_cheeses(maze,pieces_of_cheese,really_best_path[0])
#    if len(really_best_path)==2:
#        bruteforce(the_next_cheeses,player1_location,[],0,player1_location)
#    #        while we didn't reach the next vertex to be visited:
    if len(trajet[really_best_path[-1]][really_best_path[-2]][0])>1:
        #our move is defined as the m else :
        move=trajet[really_best_path[-1]][really_best_path[-2]][0].pop(1)
        return moveFromLocations(player1_location,move)
   
    if player1_location==really_best_path[0]:
        the_next_cheeses=next_3_cheeses(maze,pieces_of_cheese,really_best_path[0])
        best=inf
        bruteforce(the_next_cheeses,player1_location,[],0,player1_location)
        print('next cheeses=',the_next_cheeses)
        really_best_path=list(reversed(best_path))
        really_best_path.append(player1_location)
        print('rbp=',really_best_path)
        move=trajet[really_best_path[-1]][really_best_path[-2]][0].pop(1)
        return moveFromLocations(player1_location,move)
    else :
        #if we reached our destination:
        #we deleete the just-visited vertex of best_path
        really_best_path.pop()
        #and we do the same thing as before
        print('trajet=',trajet[really_best_path[-1]][really_best_path[-2]][0])
        move=trajet[really_best_path[-1]][really_best_path[-2]][0].pop(1)
        return moveFromLocations(player1_location,move)

    