# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print "%s / %s / %s / %s / %s" % (successorGameState, newPos, newFood, newGhostStates, newScaredTimes)

        "*** YOUR CODE HERE ***"
        # print "Get score: %s\n" % (successorGameState.getScore())
        # print "Get ghost position: %s\n" % (successorGameState.getGhostPositions())
        newGhostPos = successorGameState.getGhostPositions()
        conDistoGhost = 0
        if util.manhattanDistance(newPos, newGhostPos[0]) <= 1:
            conDistoGhost = -500

        comp = sys.maxint
        for i in range(1, newFood.height - 1):
            for j in range(1, newFood.width - 1):
                if newFood[j][i] and util.manhattanDistance([j, i], newPos) < comp:
                    comp = util.manhattanDistance([j, i], newPos)

        return successorGameState.getScore() - successorGameState.getNumFood() + 10 / comp + conDistoGhost

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # return self.getActionH(gameState, 0)

        if gameState.getNumAgents() == 1:
            TOF = True
        else:
            TOF = False

        bestValue = -float("inf")
        for action in gameState.getLegalActions(0):
            compareto = self.getActionH(gameState.generateSuccessor(0, action),
                                         self.depth * gameState.getNumAgents() - 1, TOF)
            if bestValue < compareto:
                bestValue = compareto
                toReturn = action

        return toReturn

        util.raiseNotDefined()

    def getActionH(self, gameState, depth, isMaximizer):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return float(self.evaluationFunction(gameState))

        tof = False
        if (depth - 1) % gameState.getNumAgents() == 0:
            tof = True
        else:
            tof = False

        agentIndex = (self.depth * gameState.getNumAgents() - depth) % gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)

        if isMaximizer:
            bestValue = -float("inf")
            for action in actions:
                bestValue = max(bestValue, self.getActionH(gameState.generateSuccessor(agentIndex, action),
                                                            depth - 1, tof))
            return float(bestValue)
        else:
            bestValue = float("inf")
            for action in actions:
                bestValue = min(bestValue, self.getActionH(gameState.generateSuccessor(agentIndex, action),
                                                            depth - 1, tof))
            return float(bestValue)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        if gameState.getNumAgents() == 1:
            TOF = True
        else:
            TOF = False

        alpha = -float("inf")
        beta = float("inf")
        bestValue = -float("inf")
        for action in gameState.getLegalActions(0):
            compareto = self.getActionH(gameState.generateSuccessor(0, action),
                                        self.depth * gameState.getNumAgents() - 1, TOF, alpha, beta)
            if bestValue < compareto:
                bestValue = compareto
                toReturn = action
            alpha = max(alpha, bestValue)
            if beta < alpha:
                break

        return toReturn

        util.raiseNotDefined()

    def getActionH(self, gameState, depth, isMaximizer, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return float(self.evaluationFunction(gameState))

        tof = False
        if (depth - 1) % gameState.getNumAgents() == 0:
            tof = True
        else:
            tof = False

        agentIndex = (self.depth * gameState.getNumAgents() - depth) % gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)

        if isMaximizer:
            bestValue = -float("inf")
            for action in actions:
                bestValue = max(bestValue, self.getActionH(gameState.generateSuccessor(agentIndex, action),
                                                           depth - 1, tof, alpha, beta))
                alpha = max(alpha, bestValue)
                if beta < alpha:
                    break
            return float(bestValue)
        else:
            bestValue = float("inf")
            for action in actions:
                bestValue = min(bestValue, self.getActionH(gameState.generateSuccessor(agentIndex, action),
                                                           depth - 1, tof, alpha, beta))
                beta = min(beta, bestValue)
                if beta < alpha:
                    break
            return float(bestValue)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        if gameState.getNumAgents() == 1:
            TOF = True
        else:
            TOF = False

        bestValue = -float("inf")
        for action in gameState.getLegalActions(0):
            compareto = self.getActionH(gameState.generateSuccessor(0, action),
                                        self.depth * gameState.getNumAgents() - 1, TOF)
            if bestValue < compareto:
                bestValue = compareto
                toReturn = action

        return toReturn

        util.raiseNotDefined()

    def getActionH(self, gameState, depth, isMaximizer):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return float(self.evaluationFunction(gameState))

        agentIndex = (self.depth * gameState.getNumAgents() - depth) % gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)

        tof = False
        if (depth - 1) % gameState.getNumAgents() == 0:
            tof = True
        else:
            tof = False

        if isMaximizer:
            bestValue = -float("inf")
            for action in actions:
                bestValue = max(bestValue, self.getActionH(gameState.generateSuccessor(agentIndex, action), depth - 1,
                                                           tof))
            return bestValue
        else:
            bestValue = 0.0
            for action in actions:
                bestValue += self.getActionH(gameState.generateSuccessor(agentIndex, action), depth - 1, tof)

            return float(bestValue) / float(len(actions))


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    newGhostPos =  currentGameState.getGhostPositions()
    conDistoGhost = 0
    if util.manhattanDistance(newPos, newGhostPos[0]) <= 1:
        conDistoGhost = -500

    # comp = sys.maxint
    # for i in range(1, newFood.height - 1):
    #     for j in range(1, newFood.width - 1):
    #         if newFood[j][i] and util.manhattanDistance([j, i], newPos) < comp:
    #             comp = util.manhattanDistance([j, i], newPos)
    # if comp == 1 or comp == 2 or comp == 3:
    #     comp = 0

    value = 0
    for i in range(1, newFood.height - 1):
        for j in range(1, newFood.width - 1):
            if newFood[j][i]:
                value += calculateValue(util.manhattanDistance([j, i], newPos), j, i, newPos)
                # value += 2.0 / float(util.manhattanDistance([j, i], newPos))

    # return currentGameState.getNumFood() + currentGameState.getScore()
    # return currentGameState.getScore() - currentGameState.getNumFood() + conDistoGhost

    capsuleValue = 0
    catchGhost = 0
    if newScaredTimes[0] > 0:
        capsuleValue = 500
        if newScaredTimes[0] < 39:
            catchGhost = 100.0 / float(util.manhattanDistance(newGhostPos[0], newPos))

    return value + currentGameState.getScore() + conDistoGhost + capsuleValue + catchGhost

    util.raiseNotDefined()

def calculateValue(man, j, i, newPos):
    if man <= 2:
        return 3
    elif man <= 3:
        return 2
    elif man <= 5:
        return 1
    else:
        return 1.0 / float(util.manhattanDistance([j, i], newPos))


# Abbreviation
better = betterEvaluationFunction

