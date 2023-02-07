TEAM_NAME = "BFS"

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
a=0 #increases every time turn is executed in order to select the next move to do in the path
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
def preprocessing(maze, width, height, player1_location, player2_location, pieces_of_cheese, turn_time):
    #we will use chemin in turn so it has to be global
    global chemin
    # same as chemin
    global trajet
    #chemin is the complete DFS with the path and the routing table
    chemin=BFS(player1_location,maze)
    #trajet is the actual path that our rat will take to go to the location
    trajet=list(reversed(path(pieces_of_cheese[0],player1_location)))
 
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

def BFS(start_vertex,maze):
    neighborsAndParents=[]
    #no parents for the first vertex, we fill lifo with the initial location.
    neighborsAndParents.append((start_vertex,None))
    explored_vertices=[]
    routing_table={}

    while len(neighborsAndParents)>0:
        (current_vertex,parent)=neighborsAndParents.pop(0)
        if current_vertex not in explored_vertices:
            explored_vertices.append(current_vertex)
            routing_table[current_vertex]=parent
            for neighbor in neighbors(current_vertex,maze):
                if neighbor not in explored_vertices:
                    neighborsAndParents.append((neighbor,current_vertex))
                    
    return  explored_vertices,routing_table

#path returns the path to go from A to B using BFS/DFS
def path(end,begin):
    #we initialize the path list with the end
    path=[end]
    #we initialize the immaginary location we are on
    location=end
    #while we didn't reach the end:
    while location!=begin:
        #we add the child of the actual vertex to path
        path.append(chemin[1][location])
        #we change location so it stops
        location=chemin[1][location]
    return path

def turn(maze, width, height, player1_location, player2_location, score1, score2, pieces_of_cheese, turn_time):
    #global visitedCells
    #a has to be global so the value will not reinitialize to 0 every turn
    global a
    #we add our actual position to visited cells
    if player1_location not in visitedCells :
        visitedCells.append(player1_location)

    # v-- new code (we get the moves leading to a new cell and apply one of them at random if possible)
    moves = listDiscoveryMoves(player1_location,maze,pieces_of_cheese)
    #si moves n'est pas vide:
    if moves:
        #a increases...
        a+=1
        #so the rat takes the next location to go to in trajet
        return moveFromLocations(player1_location,trajet.pop(0))
        #return moveFromLocations(player1_location,moves[random.randint(0,len(moves)-1)])
    else :
#        alternative=chemin[1][player1_location]
#        return moveFromLocations(player1_location,alternative)
        return MOVE_UP