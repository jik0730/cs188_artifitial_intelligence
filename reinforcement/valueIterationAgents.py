# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        temp = util.Counter()
        for i in range(0, self.iterations):
            for state in self.mdp.getStates()[1:]:
                temp[state] = self.getQValue(state, self.getPolicy(state))
            for s in temp.sortedKeys():
                self.values[s] = temp[s]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        Q_Value = 0.0
        for successor in self.mdp.getTransitionStatesAndProbs(state, action):
            s, t = successor
            r = self.mdp.getReward(state, action, s)
            v = self.getValue(s)
            Q_Value += t * (r + self.discount * v)

        return Q_Value

        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        dic = util.Counter()
        for action in self.mdp.getPossibleActions(state):
            dic[action] = self.getQValue(state, action)
        return dic.argMax()

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        total = len(self.mdp.getStates())
        for i in range(0, self.iterations):
            if i % total != 0:
                state = self.mdp.getStates()[i % total]
                temp = self.getQValue(state, self.getPolicy(state))
                self.values[state] = temp


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = util.Counter()
        for s in self.mdp.getStates():
            #predecessors[s] = self.findPredecessors(s)
            set2 = set()
            self.findPredecessors2(s, set2)
            set2.add(s)
            predecessors[s] = set2

        priorityQ = util.PriorityQueue()
        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                diff = abs(self.values[s] - self.getQValue(s, self.getPolicy(s)))
                priorityQ.update(s, -diff)

        for i in range(0, self.iterations):
            if priorityQ.isEmpty():
                return
            s = priorityQ.pop()
            self.values[s] = self.getQValue(s, self.getPolicy(s))
            for p in predecessors[s]:
                diff = abs(self.values[p] - self.getQValue(p, self.getPolicy(p)))
                if diff > self.theta:
                    priorityQ.update(p, -diff)

    def findPredecessors(self, state):
        set1 = set()
        for s in self.mdp.getStates():
            if s != state and not self.mdp.isTerminal(s):
                for a in self.mdp.getPossibleActions(s):
                    for successor in self.mdp.getTransitionStatesAndProbs(s, a):
                        s_p, t = successor
                        if t > 0.0 and s_p == state and s != state:
                            set1.add(s)
        return set1

    def findPredecessors2(self, state, set2):
        for s in self.mdp.getStates():
            if s != state and not self.mdp.isTerminal(s):
                for a in self.mdp.getPossibleActions(s):
                    for successor in self.mdp.getTransitionStatesAndProbs(s, a):
                        s_p, t = successor
                        if t > 0.0 and s_p == state:
                            set2.add(s)
                            if s not in set2:
                                self.findPredecessors2(s, set2)

    def findPredecessors3(self, state, set3):
        for a in self.mdp.getPossibleActions(state):
            for successor in self.mdp.getTransitionStatesAndProbs(state, a):
                s_p, t = successor
                if t > 0.0 and s_p != state and not self.mdp.isTerminal(s_p):
                    set3.add(s_p)
