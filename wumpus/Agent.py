import numpy as np
import math
from Tile import *
from Environment import *
from Player import *

class Agent:
    debug = True

    dangers = [[0 for x in range(10)] for x in range(10)]
    visited = [[False for x in range(10)] for x in range(10)]
    shoot = [[0 for x in range(10)] for x in range(10)]

    nextActions = []
    nextMoves = []
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def setDebug(self,value):
        self.debug = value

    def beforeMove(self,player):
        # if(self.debug):
        #     print(player.render())
        #     print(player.debug())
        pass
    def afterAction(self,player):
        if(self.debug):
            print(player.getLastAction())
            if(player.isDead()):
                print("Game Over!!!")

    
    def getAction(self,player):
        x = player.getX()
        y = player.getY()

        self.visited[x][y] = True
        if(len(self.nextActions)>0):
            print(len(self.nextActions))
            return [self.nextActions.pop(0),self.nextMoves.pop(0)]
        if(player.hasGlitter() == True):
            return [Environment.Action.GRAB,[player.x,player.y]]
        neighbors = self.get_adjacent_caves(x,y)

        if((player.hasStench() == True) and (player.hasArrow() == True)):
            for cave in neighbors:
                if((self.visited[cave[0]][cave[1]] == False) and (self.shoot[cave[0]][cave[1]] == False)):
                    self.shoot[cave[0]][cave[1]] = True
                    actions = self.getActionsToShoot(player,cave)
                    self.nextActions.append(actions)
                    self.nextMoves.append([player.x,player.y])
                    return [self.nextActions.pop(0),self.nextMoves.pop(0)]

        if(player.hasBreeze() == True):
            knownPitPosition = False
            for cave in neighbors:
                if(self.dangers[cave[0]][cave[1]] == 1):
                    knownPitPosition = True
                    break

            if(knownPitPosition == False):
                for cave in neighbors:
                    if(self.visited[cave[0]][cave[1]] == False):
                        if(self.dangers[cave[0]][cave[1]] < 1):
                            self.dangers[cave[0]][cave[1]] += 0.5
                        if(self.dangers[cave[0]][cave[1]] == 1):
                            knownPitPosition = True

                if(knownPitPosition == True):
                    for cave in neighbors:
                        if(self.dangers[cave[0]][cave[1]] < 1):
                            self.dangers[cave[0]][cave[1]] = 0.0
        else:
            for cave in neighbors:
                if(self.dangers[cave[0]][cave[1]] < 1):
                    self.dangers[cave[0]][cave[1]] = 0.0

        currentCost = 100
        next = [-1,-1]
        for cave in neighbors:
            cost = self.getCost(player,cave)
            if(cost < currentCost and self.visited[cave[0]][cave[1]] == False):
                currentCost = cost
                next = cave
        if(self.debug):
            print("Go to {} {}".format(next[0],next[1]))
        actions = self.getActionsTo(player,next)
        self.nextActions.append(actions)
        self.nextMoves.append([next[0],next[1]])

        return [self.nextActions.pop(0),self.nextMoves.pop(0)]

    def get_adjacent_caves(self,i,j):
        adjacent_caves = []

        if((i-1)>=0):
                adjacent_caves.append([i-1,j])
        if((i+1)<=9):
                adjacent_caves.append([i+1,j])
        if((j-1)>=0):
                adjacent_caves.append([i,j-1])
        if((j+1)<=9):
                adjacent_caves.append([i,j+1])

        return adjacent_caves

    
    
    def getTurns(self,player, toDest):
        fromDest = [1,0]
        direction = player.getDirection()

        turns = 0

        if(direction == Player.Direction.N):
            fromDest[0] = 0
            fromDest[1] = 1
        elif(direction == Player.Direction.S):
            fromDest[0] = 0
            fromDest[1] = -1
        elif(direction == Player.Direction.W):
            fromDest[0] = -1
            fromDest[1] = 0

        if(toDest[0] == fromDest[0]):
            if(toDest[1] != fromDest[1]):
                turns += 2

        if(toDest[1] == fromDest[1]):
            if(toDest[0] != fromDest[0]):
                turns += 2
        vector_a = np.array([fromDest[0],fromDest[1]])
        vector_b = np.array([toDest[0],toDest[1]])

        if(toDest[0]!=fromDest[0] and toDest[1]!=fromDest[1]):
            theta = math.acos(np.dot(vector_a, vector_b) / (np.dot(vector_a,vector_a)*np.dot(vector_b,vector_b)))
            return (theta/(math.pi/2))
        
        return turns

    def getCost(self,player, cave):
        sum = 1
        if(self.visited[cave[0]][cave[1]]):
            if(player.hasGlitter()):
                sum -= 5
            else:
                sum += 5
        else:
            if(player.hasBreeze()):
                if(self.dangers[cave[0]][cave[1]] < 1):
                    sum+=10
                elif(self.dangers[cave[0]][cave[1]] == 1):
                    sum+=100
        turns = self.getTurns(player,cave)
        sum += abs(turns)

        return sum

    def getActionsTo(self,player, cave):
        turns = self.getTurns(player,cave)
        actions = []
        for i in range(0,int(abs(turns))):
            if(turns < 0):
                actions.append(Environment.Action.TURN_RIGHT)
            if(turns > 0):
                actions.append(Environment.Action.TURN_LEFT)
        actions.append(Environment.Action.GO_FORWARD)
        return actions

    def getActionsToShoot(self,player, cave):
        turns = self.getTurns(player,cave)
        actions = []
        for i in range(0,int(abs(turns))):
            if(turns < 0):
                actions.append(Environment.Action.TURN_RIGHT)
            if(turns > 0):
                actions.append(Environment.Action.TURN_LEFT)
        actions.append(Environment.Action.SHOOT_ARROW)
        return actions
