from enum import Enum
from enum import auto
from Environment import *

class Player:
    class Direction(Enum):
        N = auto()
        E = auto()
        S = auto()
        W = auto()
    perceptions = []
    actions = []
    direction = Direction.E
    alive = True
    gold = False
    arrows = 3

    def __init__(self, world, cave):
        self.world = world
        self.x = cave[0]
        self.y = cave[1]

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def reset(self):
        self.arrows = 3
        self.gold = False
        self.direction = Player.Direction.E
        self.actions.clear()

    def getTile(self):
        return [self.x,self.y]

    def setTile(self,cave):
        self.x = cave[0]
        self.y = cave[1]
        #Check if player is still alive

        # self.alive = not (self.tile.contains(Environment.Element.WUMPUS) or self.tile.contains(Environment.Element.PIT))

    def getDirection(self):
        return self.direction

    def getNeighbors(self,i,j):
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

    def shootArrow(self):
        if(self.arrows > 0):
            self.arrows -= 1
            neighbors = self.getNeighbors(self.x, self.y)
            neighbor= None
            if(self.direction == Player.Direction.N):
                neighbor = neighbors[0]
            elif(self.direction == Player.Direction.E):
                neighbor = neighbors[1]
            elif (self.direction == Player.Direction.S):
                neighbor = neighbors[2]
            elif (self.direction == Player.Direction.W):
                neighbor = neighbors[3]
            if ((neighbor is not None) and (Environment.Element.WUMPUS in neighbor)):
                neighbor.remove(Environment.Element.WUMPUS)
                return Environment.Perception.SCREAM
            return None
        else:
            return Environment.Perception.NO_ARROWS

    def setAction(self,action,move):
        self.actions.append(action)
        self.x = move[0]
        self.y = move[1]
        if(action == Environment.Action.GO_FORWARD):
            neighbors = self.getNeighbors(self.x, self.y)
            if (self.direction == Player.Direction.N):
                if (neighbors[0] is not None):
                    self.setTile(neighbors[0])
            elif (self.direction == Player.Direction.E):
                if (neighbors[1] is not None):
                    self.setTile(neighbors[1])
            elif (self.direction == Player.Direction.S):
                if (neighbors[2] is not None):
                    self.setTile(neighbors[2])
            elif (self.direction == Player.Direction.W):
                if (neighbors[3] is not None):
                    self.setTile(neighbors[3])

        elif (action == Environment.Action.TURN_LEFT):
            if (self.direction == Player.Direction.N):
                self.direction = Player.Direction.W
            elif (self.direction == Player.Direction.E):
                self.direction = Player.Direction.N
            elif (self.direction == Player.Direction.S):
                self.direction = Player.Direction.E
            elif (self.direction == Player.Direction.W):
                self.direction = Player.Direction.S

        elif (action == Environment.Action.TURN_RIGHT):
            if (self.direction == Player.Direction.N):
                self.direction = Player.Direction.E
            elif (self.direction == Player.Direction.E):
                self.direction = Player.Direction.S
            elif (self.direction == Player.Direction.S):
                self.direction = Player.Direction.W
            elif (self.direction == Player.Direction.W):
                self.direction = Player.Direction.N

        elif(action == Environment.Action.GRAB):
            if (self.world[self.x][self.y].glitter == True):
                self.world[self.x][self.y].glitter = False
                self.gold = True
        elif (action == Environment.Action.SHOOT_ARROW):
            perception = self.shootArrow()
            if (perception != None) :
                self.setPerceptionsNew(perception)
            return

        self.setPerceptions()

    def getActions(self):
        return self.actions

    def getLastAction(self):
        if (len(self.actions) == 0):
            return None
        return self.actions[(len(self.actions) - 1)]

    def getScore(self):
        return Environment.getScore(self)

    def getPerceptions(self):
        return self.perceptions

    def setPerceptions(self):
        self.perceptions.clear()
        if (self.world[self.x][self.y].glitter == True):
            self.perceptions.append(Environment.Perception.GLITTER)
        neighbors = self.getNeighbors(self.x,self.y)
        for neighbor in neighbors:
            if(neighbor == -1):
                if((self.direction == Player.Direction.N) or (self.direction == Player.Direction.E) or (self.direction == Player.Direction.S) or (self.direction == Player.Direction.W)):
                    self.perceptions.append(Environment.Perception.BUMP)
            else:
                if (self.world[self.x][self.y].pit == True):
                    self.perceptions.append(Environment.Perception.BREEZE)
                if (self.world[self.x][self.y].stench == True):
                    self.perceptions.append(Environment.Perception.STENCH)

    def setPerceptionsNew(self,value):
        self.setPerceptions()
        self.perceptions.append(value)

    def isAlive(self):
        return self.alive

    def isDead(self):
        return not self.alive

    def hasArrow(self):
        return (self.arrows > 0)

    def hasGlitter(self):
        return self.gold

    def hasStench(self):
        return Environment.Perception.STENCH in self.perceptions
    
    def hasScream(self):
        return Environment.Perception.SCREAM in self.perceptions

    def hasBreeze(self):
        return Environment.Perception.BREEZE in self.perceptions
    
