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
        temp = util.Counter()
        self.list = []
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #iterate over the grid
        while(iterations >= 0):
            #Count the amount of iterations
            iterations -= 1
            #Update for every state
            for state in mdp.getStates():
                highest = None
                #Update for every action
                for action in mdp.getPossibleActions(state):
                    #Get the highest value out of the 4 Q-values
                    if highest == None or self.values[str(state)+action] > highest:
                        highest = self.values[str(state)+action]
                #to make sure the TERMINAL STATE also has a value instead it being None
                self.values["TERMINAL_STATE"] = 0
                #Update the optimal value for state
                self.values[state] = highest
            #Update for every state
            for state in mdp.getStates():
                #update for every action
                for action in mdp.getPossibleActions(state):
                    newval = 0
                    for a,b in self.mdp.getTransitionStatesAndProbs(state, action):
                        #calculte the new value
                        newval += b*(self.mdp.getReward(state, action, a)+discount*self.values[a])
                    #save new value in a temporary dictionary
                    temp[str(state)+action] = newval
            #Update the dictionary with new values after an iteration is done
            for x in temp:
                self.values[x] = temp[x]

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        #return optimal value for state
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #Get the Q value for state and action
        return self.values[str(state)+action]

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
        #if state is terminal then return none
        if self.mdp.isTerminal(state):
            return None
        else:
            #return the optimal action
            highest = None
            act = 'north'
            for action in self.mdp.getPossibleActions(state):
                if self.values[str(state)+action] > highest or highest is None:
                    highest = self.values[str(state)+action]
                    act = action
            return act
            
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
