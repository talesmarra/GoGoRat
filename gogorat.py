#IA created to be integrated as a player in the PyRat Game.
#Winner of the competition between AI's in the first semester of 2019.
#This AI combines a Supervised Approach with a CGT approach in order to obtain maximum performance,
#not only against the greedy algorithm but also against other types of AI.
# The supervised learning model was trained using games of the greedy algorithm against itself,
#but also against a reinforcement learning algorithm trained against the greedy, in order to increase robustness.
#Please cite as you use this code.



import numpy as np
import random as rd
import pickle
import time
import joblib


MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
MIN_CHEESE_GT = 12

global model

# new location after a move
def move(location, move):
    if move == MOVE_UP:
        return (location[0], location[1] + 1)
    if move == MOVE_DOWN:
        return (location[0], location[1] - 1)
    if move == MOVE_LEFT:
        return (location[0] - 1, location[1])
    if move == MOVE_RIGHT:
        return (location[0] + 1, location[1])

#opponnent stategy
def distance(la, lb):
    ax,ay = la
    bx,by = lb
    return abs(bx - ax) + abs(by - ay)

#simulates opponent
def turn_of_opponent(opponentLocation, piecesOfCheese):    
    closest_poc = (-1,-1)
    best_distance = -1
    for poc in piecesOfCheese:
        if distance(poc, opponentLocation) < best_distance or best_distance == -1:
            best_distance = distance(poc, opponentLocation)
            closest_poc = poc
    ax, ay = opponentLocation
    bx, by = closest_poc
    if bx > ax:
        return MOVE_RIGHT
    if bx < ax:
        return MOVE_LEFT
    if by > ay:
        return MOVE_UP
    if by < ay:
        return MOVE_DOWN
    pass

# With this template, we integrate two ML approaches to acquire robustness against the greedy algorithm 
#but also against other AI's

TEAM_NAME = "GoGoRat"


# We do not need preprocessing, so we let this function empty
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global model
    ### Here we load the previously trained model
    model = joblib.load('trained_classifier_go.pkl')

# We use a recursive function that goes through the trees of possible plays
# It takes as arguments a given situation, and return a best target piece of cheese for the player, such that aiming to grab this piece of cheese will eventually lead to a maximum score. It also returns the corresponding score
def best_target(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese):

    # First we should check how many pieces of cheese each player has to see if the play is over. It is the case if no pieces of cheese are left, or if playerScore or opponentScore is more than half the total number playerScore + opponentScore + piecesOfCheese
    totalPieces = len(piecesOfCheese) + playerScore + opponentScore
    if playerScore > totalPieces / 2 or opponentScore > totalPieces / 2 or len(piecesOfCheese) == 0:
        return (-1,-1), playerScore

    # If the play is not over, then the player can aim for any of the remaining pieces of cheese
    # So we will simulate the game to each of the pieces, which will then by recurrence test all
    # the possible trees.

    best_score_so_far = -1
    best_target_so_far = (-1,-1)
    for target in piecesOfCheese:
        end_state = simulate_game_until_target(
            target,playerLocation,opponentLocation,
            playerScore,opponentScore,piecesOfCheese.copy())
        _, score = best_target(*end_state)
        if score > best_score_so_far:
            best_score_so_far = score
            best_target_so_far = target

    return best_target_so_far, best_score_so_far


# Move the agent on the labyrinth using function move from aux and the different directions
# It suffices to move in the direction of the target. 
# You should only run function move once and you can't move diagonally.
## Without loss of generality, we can suppose it gets there moving vertically first then horizontally

def updatePlayerLocation(target,playerLocation):
    if playerLocation[1] != target[1]:
        if target[1] < playerLocation[1]:
            playerLocation = move(playerLocation, MOVE_DOWN)
        else:
            playerLocation = move(playerLocation, MOVE_UP)
    elif target[0] < playerLocation[0]:
        playerLocation = move(playerLocation, MOVE_LEFT)
    else:
        playerLocation = move(playerLocation, MOVE_RIGHT)
    return playerLocation

#CHECK IF EITHER/BOTH PLAYERS ARE ON THE SAME SQUARE OF A CHEESE. 
#If that is the case you have to remove the cheese from the piecesOfCheese list and 
#add points to the score. The players get 1 point if they are alone on the square with a cheese.
#If both players are in the same square and there is a cheese on the square each player gets 0.5 points.
def checkEatCheese(playerLocation,opponentLocation,playerScore,opponentScore,piecesOfCheese):
    if playerLocation in piecesOfCheese and playerLocation == opponentLocation:
        playerScore = playerScore + 0.5
        opponentScore = opponentScore + 0.5
        piecesOfCheese.remove(playerLocation)
    else:
        if playerLocation in piecesOfCheese:
            playerScore = playerScore + 1
            piecesOfCheese.remove(playerLocation)
        if opponentLocation in piecesOfCheese:
            opponentScore = opponentScore + 1
            piecesOfCheese.remove(opponentLocation)
    return playerScore,opponentScore


#In this function we simulate what will happen until we reach the target
#You should use the two functions defined before
def simulate_game_until_target(target,playerLocation,opponentLocation,playerScore,opponentScore,piecesOfCheese):
    
    #While the target cheese has not yet been eaten by either player
    #We simulate how the game will evolve until that happens    
    while target in piecesOfCheese:
        #Update playerLocation (position of your player) using updatePlayerLocation
        playerLocation = updatePlayerLocation(target,playerLocation)
        #Every time that we move the opponent also moves. update the position of the opponent using turn_of_opponent and move
        opponentLocation = move(opponentLocation, turn_of_opponent(opponentLocation, piecesOfCheese))
        #Finally use the function checkEatCheese to see if any of the players is in the same square of a cheese.
        playerScore, opponentScore = checkEatCheese(
            playerLocation,opponentLocation,playerScore,opponentScore,piecesOfCheese)
    return playerLocation,opponentLocation,playerScore,opponentScore,piecesOfCheese
    

# During our turn we continue going to the next target, unless the piece of cheese it originally contained has been taken
# In such case, we compute the new best target to go to
current_target = (-1,-1)
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global current_target
    if(len(piecesOfCheese)<MIN_CHEESE_GT):
        if current_target not in piecesOfCheese:
            current_target, score = best_target(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese)
            
        if current_target[1] > playerLocation[1]:
            return MOVE_UP
        if current_target[1] < playerLocation[1]:
            return MOVE_DOWN
        if current_target[0] > playerLocation[0]:
            return MOVE_RIGHT
        return MOVE_LEFT
    else:
        return turn_supervised(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed)
        

def convert_input_2(player, maze, opponent, mazeHeight, mazeWidth, piecesOfCheese):
	# We will consider twice the size of the maze to simplify the creation of the canvas 
	# The canvas is initialized as a numpy tensor with 3 modes (meaning it is indexed using three integers), the third one corresponding to "layers" of the canvas. 
	# Here, we just use one layer, but you can defined other ones to put more information on the play (e.g. the location of the opponent could be put in a second layer)

    im_size = (2*mazeHeight-1,2*mazeWidth-1,1)

    # We initialize a canvas with only zeros
    canvas = np.zeros(im_size)


    (x,y) = player

    # fill in the first layer of the canvas with the value 1 at the location of the cheeses, relative to the position of the player (i.e. the canvas is centered on the player location)
    center_x, center_y = mazeWidth-1, mazeHeight-1
    for (x_cheese,y_cheese) in piecesOfCheese:
        canvas[y_cheese+center_y-y,x_cheese+center_x-x,0] = 1
    return canvas

def turn_supervised(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):    
    global model,input_tm1, action, score

    # Transform the input into the canvas using convert_input 

    input_t = convert_input_2(playerLocation, mazeMap, opponentLocation, mazeHeight, mazeWidth, piecesOfCheese)    
    

    # Predict the next action using the trained model	
    output = model.predict(input_t.reshape(1,-1))
    action = output[0]
    # Return the action to perform
    return [MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN][action]

def postprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    pass    

