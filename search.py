# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from copy import copy


class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  """

  problem.getSuccessors(problem.getStartState())
  return recursiveDLS([],problem,300)

def recursiveDLS(path,problem,limit):
    """
    Recursive Depth Limited Search
    :param path:
    :param problem:
    :param limit:
    :return path:
    """

    if problem.isGoalState(problem._visitedlist[-1]):
        return path
    elif problem._expanded == limit:
        return []
    else:
        result = []
        cutoff_occurred = False
        actions = copy(problem)
        actions = actions.getSuccessors(problem._visitedlist[-1])
        for action in actions:
            move = action[0]
            direction = action[1]
            if move in problem._visitedlist:
                if len(actions) == 1:
                    cutoff_occurred = True
                continue
            child = copy(problem)
            child.getSuccessors(move)
            result = recursiveDLS(path + [direction],child,limit)
            if not result:
                cutoff_occurred = True
            else:
                return result
        if cutoff_occurred:
            return []
        else:
            return result

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """

  path = util.Queue()
  frontier = util.Queue()
  frontier.push([(problem.getStartState(), 0)])
  explored = []

  # While frontier has items left, loop
  while not frontier.isEmpty():
      # Remove most shallow frontier item and add it to path and explored
      path = frontier.pop()
      parentMove = path[len(path) - 1]
      parentMove = parentMove[0]
      explored.append(parentMove)

      # Check to see if goal is met
      if problem.isGoalState(explored[-1]):
          return [direction[1] for direction in path][1:]

      # Iterate through possible moves
      actions = problem.getSuccessors(parentMove)
      for action in actions:
          move = action[0]
          if action in frontier.list or move in explored:
              continue

          # push path to frontier
          parentPath = path[:]
          parentPath.append(action)
          frontier.push(parentPath)



def uniformCostSearch(problem):
  "Search the node of least total cost first. "

  def nameYourPrice(dollars):
      return problem.costFn(dollars[-1][0])

  # frontier = util.PriorityQueueWithFunction(problem.costFn)
  frontier = util.PriorityQueueWithFunction(nameYourPrice)

  frontier.push([(problem.getStartState(),0, 0)])
  explored = []

  #[((33, 16), 'West', 1.1641532182693481e-10)]

  # While frontier has items left, loop
  while not frontier.isEmpty():
      # Remove most shallow frontier item and add it to path and explored
      path = frontier.pop()

      parentMove = path[len(path) - 1]
      parentMove = parentMove[0]
      explored.append(parentMove)

      # Check to see if goal is met
      if problem.isGoalState(explored[-1]):
          return [direction[1] for direction in path][1:]

      # Iterate through possible moves
      actions = problem.getSuccessors(parentMove)
      for action in actions:
          move = action[0]
          if action in frontier.heap or move in explored:
              continue

          # push path to frontier
          parentPath = path[:]
          parentPath.append(action)
          frontier.push(parentPath)


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."

  def nameYourPrice(dollars):
      return heuristic([10, 10], problem)

  frontier = util.PriorityQueueWithFunction(nameYourPrice)
  frontier.push([(problem.getStartState(),0, 0)])
  explored = []

  # While frontier has items left, loop
  while not frontier.isEmpty():
      # Remove most shallow frontier item and add it to path and explored
      path = frontier.pop()

      parentMove = path[len(path) - 1]
      parentMove = parentMove[0]
      explored.append(parentMove)

      # Check to see if goal is met
      if problem.isGoalState(explored[-1]):
          return [direction[1] for direction in path][1:]

      # Iterate through possible moves
      actions = problem.getSuccessors(parentMove)
      for action in actions:
          move = action[0]
          if action in frontier.heap or move in explored:
              continue

          # push path to frontier
          parentPath = path[:]
          parentPath.append(action)
          frontier.push(parentPath)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


