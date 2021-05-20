# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import util
from util import Stack
from util import Queue
from util import PriorityQueue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    fringe = Stack() #fringe#
    closed = set() #explored set#
    suc = [] #successors list#
    next = problem.getStartState()
    fringe.push((next,[],0)) #push starting state in list#

    while 1:
        (next,direction,cost) = fringe.pop() #pop next node from fringe#
        if problem.isGoalState(next): #if node is goal stop the search#
            break
        closed.add(next) #add the node to the explored set#
        suc.extend(problem.getSuccessors(next)) #get nodes successors#
        for x in range(len(suc)): #push successors in fringe if they are not already explored#
            if not (suc[x][0] in closed):
                fringe.push((suc[x][0],direction+[suc[x][1]],cost+suc[x][2]))
                closed.add(next) #add the child to the explored set#
        suc.clear() #clear successors list#
    return direction

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    fringe = Queue()
    closed = [] #explored nodes list#
    suc = [] #successors list#
    next = problem.getStartState()
    fringe.push((next, [], 0))
    vis=0 #variable for cornerproblem#
    c=0 #nodes in fringe counter#
    while 1:
        (next, dir, cost) = fringe.pop()
        c=c-1
        if problem.isGoalState(next):
            break
        closed.append(next) #node is explored, dont go over it again#
        suc.extend(problem.getSuccessors(next))
        for x in range(len(suc)):
            if not (suc[x][0] in closed): #if successor is not in explored list#
                if len(problem._visitedlist)>vis and len(problem.corners)==4: #for cornerproblem only#
                    vis+=1
                    while c>-1: #remove all paths from fringe, use the one that goes throuth the corner#
                        fringe.pop()
                        c=c-1
                fringe.push((suc[x][0], dir + [suc[x][1]], cost + suc[x][2]))
                closed.append(suc[x][0])
                c=c+1
        suc.clear()
        if fringe.isEmpty(): #in order to go to next corner you might have to navigate through already expored nodes#
            closed.clear() #clear the already explored list so that you may go through these nodes to the next corner#
            suc.extend(problem.getSuccessors(next))
            for x in range(len(suc)):
                if not (suc[x][0] in closed):
                    fringe.push((suc[x][0], dir + [suc[x][1]], cost + suc[x][2]))
                    closed.append(suc[x][0])
                    c = c + 1
            suc.clear()
    return dir
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    fringe = PriorityQueue()
    closed = set()
    suc = []
    next = problem.getStartState()
    fringe.push((next, [], 0),0)
    while 1:
        (next, dir, cost) = fringe.pop()
        if problem.isGoalState(next):
            break
        closed.add(next)
        suc.extend(problem.getSuccessors(next))
        for x in range(len(suc)):
            if not (suc[x][0] in closed):
                fringe.push((suc[x][0], dir + [suc[x][1]], cost + suc[x][2]),cost + suc[x][2])
                closed.append(suc[x][0])
        suc.clear()
    return dir
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    fringe = PriorityQueue()
    closed = []  # explored nodes list
    suc = []
    next = problem.getStartState()
    fringe.push((next, [], 0),heuristic(next,problem))
    c = 0 #counter of nodes in fringe#
    vis = 0 #visited corners#
    food = 0
    if next[1].count(True)>4: #a way to to distinguish between cornerproblem and foodsearchproblem, corner grid has count(true)=4#
        food=1
    while 1:
        (next, dir, cost) = fringe.pop()
        c=c-1
        if problem.isGoalState(next):
            break
        closed.append(next)
        suc.extend(problem.getSuccessors(next)) #get node's successors#
        for x in range(len(suc)):
            if not (suc[x][0] in closed): #if successor[x] not in closed, push to fringe#
                if food==1:
                    fringe.push((suc[x][0], dir + [suc[x][1]], cost + suc[x][2]), cost + suc[x][2] + heuristic(suc[x][0], problem))
                    continue
                if len(problem._visitedlist) > vis: #for corners problem, if one of successors is a corner #
                    vis += 1
                    while c > -1: #clear the fringe and leave only the corner#
                        fringe.pop()
                        c = c - 1
                fringe.push((suc[x][0], dir + [suc[x][1]], cost + suc[x][2]), cost + suc[x][2] + heuristic(suc[x][0], problem))
                closed.append(suc[x][0])
                c=c+1
        suc.clear()
        if food==0 and fringe.isEmpty():    #if no nodes in fringe because all successors are in explored set#
            closed.clear()  #clear explored set if you need to go back to already explored nodes in order to reach next corner#
            suc.extend(problem.getSuccessors(next))
            for x in range(len(suc)):
                if not (suc[x][0] in closed):
                    fringe.push((suc[x][0], dir + [suc[x][1]], cost + suc[x][2]),cost + suc[x][2] + heuristic(suc[x][0], problem))
                    closed.append(suc[x][0])
                    c = c + 1
            suc.clear()
    return dir
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
