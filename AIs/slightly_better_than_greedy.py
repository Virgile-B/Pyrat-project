# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 18:16:56 2019

@author: Virgile
"""

TEAM_NAME = "slightly_better_than_greedy"

# =============================================================================
#  When the player is performing a move, it actually sends a character to the main program
#  The four possibilities are defined here
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


#returns a random move
def randomMove():
    moves = [MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP]
    return moves[random.randint(0,3)]

#returns the list of the moves the player can perform
def neighbors(location,maze):
    res=[]
    # for neighbors around the actual rat's location :
    for neighbor in maze[location]:
        #we add the neighbor
        res.append(neighbor)
    return res

#returns what does the player do to move from an initial case to a new one
def moveFromLocations(sourceLocation, targetLocation) :
    #we compute the difference between the couple where we want to got to our location
    difference = tuple(numpy.subtract(targetLocation, sourceLocation))
    #then we compare the difference to the following couples to determine the answer
    if difference == (0, -1) :
        return MOVE_DOWN
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (-1, 0) :
        return MOVE_LEFT
    else :
        #to know the nature of aspecific proclems we put this exception
        raise Exception("Impossible move")

#returns the list of neighbors undiscovered for a specific place in the maze.
def listDiscoveryMoves(location, maze,pieces_of_cheese) : #returns the list of the unvisited places
    #initially we didn't compute anything so there is nothing new
    moves = []
    #for neighbor for our position:
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

# =============================================================================
#  Arguments are:
#  mazeMap : dict(pair(int, int), dict(pair(int, int), int))
#  mazeWidth : int
#  mazeHeight : int
#  playerLocation : pair(int, int)
#  opponentLocation : pair(int,int)
#  piecesOfCheese : list(pair(int, int))
#  timeAllowed : float
# =============================================================================
# =============================================================================
# # This function is not expected to return anything
# 
#     # Example prints that appear in the shell only at the beginning of the game
#     # Remove them when you write your own program
# 
# #get_steps_number = lambda turn: sum(1 for line in open(turn) if 'return' in line)
# =============================================================================
# =============================================================================
#  Turn function
#  The turn function is called each time the game is waiting
#  for the player to make a decision (a move).
# =============================================================================
# =============================================================================
#  Arguments are:
#  mazeMap : dict(pair(int, int), dict(pair(int, int), int))
#  mazeWidth : int
#  mazeHeight : int
#  playerLocation : pair(int, int)
#  opponentLocation : pair(int, int)
#  playerScore : float
#  opponentScore : float
#  piecesOfCheese : list(pair(int, int))
#  timeAllowed : float
# =============================================================================
###############################

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

#this function is used for the dijkstra to build the clothest path from A to B
def add_or_replace(heap,couple):
    exists=False
    #wgile we didn't reach the end of the list heap:
    for i in range(len(heap)):
        #si le ieme terme prit en 0 vaut le couple prit en 0
        if heap[i][0]==couple[0]:
            #we change exists to true
            exists=True
            #if the previous heap at this emplacement is greater than the new one, we replace the old one with the new one
            if heap[i][1]>couple[1]:
                heap[i]=couple
                #else
    if exists==False:
        #on rajoute le couple
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
    l_pos=pieces_of_cheese
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


#Returns the position of the clothest cheese   
def clothest_cheese(maze,pieces_of_cheese,location):
    #we must define mgraph_list as global to use it in turn and update it
    global mgraph_list
    global trajet
    #we initialize the best_weight and mgraph_list once
    best_weight=inf
    best_cheese=None
    if location in trajet:
    #for each vertex in the list:
        for vertex in mgraph_list:
            #to avoir key errors:
            if vertex!=location:
                #we define the weight thanks to the metagraph
                weight=trajet[location][vertex][1]
                #if the tackled cheese is clothest to the player:
                if weight<best_weight:
                    #we update both the result and the weight
                    best_weight=weight
                    best_cheese=vertex
                #we return the result
    #if we don't go into the if loop:
    if best_cheese==None:
        #we avoir going to an empty place:
        return pieces_of_cheese.pop(0)
    #define the result:
    result=mgraph_list.pop(mgraph_list.index(best_cheese))
    return result

#farest cheese is used for density to determine which is the farest cheese from others one.
def farest_cheese(maze,pieces_of_cheese,location):
    global farest_ones
    #we must define mgraph_list as global to use it in turn and update it
    global list_cheeses
    global eviter_boucle_inf
    #we initialize the best_weight and mgraph_list once
    biggest_weight=0
    worst_cheese=None
    if len(farest_ones)==1 and eviter_boucle_inf==True:
        eviter_boucle_inf=False
        return farest_cheese(maze,pieces_of_cheese,farest_ones[0])
    #for each vertex in the list:
    for vertex in list_cheeses:
        #to avoir key errors:
        if vertex!=location:
            #we define the weight thanks to the metagraph
            weight=trajet[location][vertex][1]
            #if the tackled cheese is clothest to the player:
            if weight>biggest_weight:
                #we update both the result and the weight
                biggest_weight=weight
                worst_cheese=vertex
                #we return the result
    if worst_cheese==None:
        return pieces_of_cheese.pop(0)
    result=list_cheeses.pop(list_cheeses.index(worst_cheese))
    return result        
 
#renvoie les 3 fromages les plus loins entre eux pour ensuite faire un calcul de densité dessus                   
def cheeses_far_3(maze,pieces_of_cheese):
    global list_cheeses
    global farest_ones
    global eviter_boucle_inf
    eviter_boucle_inf=True
    #contient les fromages éloignés (vide au début)
    farest_ones=[]
    #on copie mgraph_list pour pas le modifiertant que l'on a pas prit les fromages
    list_cheeses=mgraph_list[:]
    #le 1er élément est random
    res=[list_cheeses.pop(0)]
    #on ajoute 2 fromages au résultat
    for i in range(2):
        far=farest_cheese(maze,pieces_of_cheese,list_cheeses[0])
        res.append(far)
        farest_ones.append(far)
    print('les 3 fromages éloignés',res)
    return res

    #renvoie la densité pour les 3 fromages éloignés définis juste avant    
def density(maze,pieces_of_cheese):
    #là c'est les 3 fromage sque l'on vient de voir
    tackled_list=cheeses_far_3(maze,pieces_of_cheese)
    res={}
    #pour chaque fromage éloigné:
    for cheese in tackled_list:
        res[cheese]={}
        #pour chaque 2ème fromages dans mgraph_list privée des 3 fromages éloignés:
        for cheese_2 in list_cheeses:
            #pour éviter les key orror:
            if cheese_2!=cheese:
               # si le fromage cheese2 est pas trop loins de cheese, on le compte comme dans l'entourage de cheese
                if trajet[cheese][cheese_2][1]<8:
                    #on met n'importe quel nombre on veut just augmeter len(res[cheese][cheese2])
                    res[cheese][cheese_2]=1
    #le fromage autour duquel la densité est le plus forte, et la plus grosse densités valent :
    coolest_cheese,biggest_density=tackled_list[0],len(res[tackled_list[0]])
    for i in range(1,len(tackled_list)):
        #on fait les comparaisons de densité
        cheese_here,density_value=tackled_list[i],len(res[tackled_list[i]])
        #si la densité est plus forte que précédemment, on la garde
        if density_value>biggest_density:
            coolest_cheese,biggest_density=cheese_here,density_value
    return coolest_cheese         
        
    
#preprocessing is called at the beginning of the pyrat game
def preprocessing(maze, width, height, player1_location, player2_location, pieces_of_cheese, turn_time):
    #we will use chemin in turn so it has to be global
 #   global chemin
    # same as chemin
    global trajet
    global destination
    global in_location
    global mgraph_list
    global indice_fin
    global indice_fin2
    #indice to determine whether or not we do something at the end
    indice_fin2=True
    #same principle as indice_fin2 but earlier
    indice_fin=True
    #mgraph_list will be used as the metagraph_list
    mgraph_list=pieces_of_cheese[:]
    #trajet is the actual path that our rat will take to go to the location
    trajet=metagraph(player1_location,maze,pieces_of_cheese)
    #our initial location is obviously player1_location
    in_location=player1_location
    #and our destination is the clothest cheese
    destination=clothest_cheese(maze,pieces_of_cheese,player1_location)


 
 #turn is called for each move of the rat/python   
def turn(maze, width, height, player1_location, player2_location, score1, score2, pieces_of_cheese, turn_time):
#        while we didn't reach the next vertex to be visited:
# =============================================================================
# =============================================================================
    global in_location
    global destination
    global mgraph_list
    global indice_fin
    global destination_snake
    global in_location_snake
    global new_trajet
    global indice_fin2
    global in_location_snake
    global der_des_der
    global trajet
# =============================================================================
    #on supprime les fromages que l'ennemi prend
    destination_snake=None
    for cheese in mgraph_list:
        #si le score est suffisamment grand et que l'ennemi est sur une position où on peut calculer clothest_cheese()
        if score1+score2>20 and player2_location==cheese:
            #on définit la position initiale et la destination de l'ennei comme si c'était un greedy
            in_location_snake=player2_location
            destination_snake=clothest_cheese(maze,pieces_of_cheese,player2_location)
#            print(destination_snake)
            #on suprime les fromages que l'ennemi prend:
        if player2_location==cheese:
            mgraph_list.pop(mgraph_list.index(cheese))

# =============================================================================
    #si le score est suffisamment grand et que nous somme à un endroit où on peut calculer clothest_cheese ou farest_cheese:
    #avec indice_fin qui sert à ne pas refaire le calcul à chaque fois que l'on récupère un fromage pour éviter les allers retours
    #pour de trop grandes distances.
    if player1_location==destination and score1+score2>27 and len(pieces_of_cheese)>3 and indice_fin==True:
        in_location=player1_location
        #on fait le calcul de densité et on définit notre destination en conséquence
        destination=density(maze,pieces_of_cheese)
        print(destination)
        indice_fin=False
    if player1_location==destination and score1+score2>34 and indice_fin2==True:
        #si on est sûr que le serpent arrivera à notre fromage le plus proche avant nous:
        if destination==destination_snake and trajet[in_location][destination][1]>=trajet[in_location_snake][destination_snake][1]:
            #on renouvelle notre destination
            destination=clothest_cheese(maze,pieces_of_cheese,player1_location)
            indice_fin2=False
            

      #prog principal auquel je touche pas :      
# =============================================================================
    if player1_location!=destination:
        move=trajet[in_location][destination][0].pop(1)
        return moveFromLocations(player1_location,move)
    else:
        #if we reached our destination:
        #we deleete the just-visited vertex of best_path
        #and we do the same thing as before
        destination=clothest_cheese(maze,pieces_of_cheese,destination)
        in_location=player1_location
        move=trajet[player1_location][destination][0].pop(1)
        return moveFromLocations(player1_location,move)
# =============================================================================
