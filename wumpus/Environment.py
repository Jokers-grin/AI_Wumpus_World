from enum import Enum
from enum import auto

class Environment:

    class Element(Enum):
        WUMPUS = auto()
        PIT = auto()
        HUNTER = auto()
        GOLD = auto()

    class Perception(Enum):
        SCREAM = auto()
        STENCH = auto()
        BREEZE = auto()
        GLITTER = auto()
        BUMP = auto()
        NO_ARROWS = auto()

    class Action(Enum):
        GO_FORWARD = auto()
        TURN_LEFT = auto()
        TURN_RIGHT = auto()
        GRAB = auto()
        SHOOT_ARROW = auto()

    class Result(Enum):
        WIN = auto()
        LOSS = auto()

    def getScore(self,player):
        sum = 0
        if(player.isDead() == True):
            sum += -1000
        if(player.hasGold() == True):
            sum += 1000
        for action in player.getActions():
            if(action == Environment.Action.TURN_LEFT or action == Environment.Action.TURN_RIGHT or action == Environment.Action.GO_FORWARD or action == Environment.Action.GRAB):
                sum += -1
            if(action == Environment.Action.SHOOT_ARROW):
                sum += -10

        return sum

    def getIconElement(self,element):
        if(element == Environment.Element.WUMPUS):
            return "W"
        elif(element == Environment.Element.HUNTER):
            return "H"
        elif(element == Environment.Element.PIT):
            return "P"
        elif(element == Environment.Element.GOLD):
            return "G$"
        return "  "

    def getIconPerception(self,perception):
        if(perception == Environment.Perception.GLITTER):
            return "*"
        elif(perception == Environment.Perception.STENCH):
            return "="
        return " "
