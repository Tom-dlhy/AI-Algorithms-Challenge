from typing import Callable
import problem2
import heapq
import numpy as np

class InformedSearch:
    def __init__(self):
        pass
    
    def heuristic_rentabilite(self,state:problem2.State):

        if(state.current_pos==0):
            return 0
        return state.value/state.current_pos

    def Astar(self,problem: problem2.BiscuitOptimization, heuristic: Callable):
        """
        Implementation of the A* search algorithm using a priority queue to expand nodes 
        based on the sum of the path cost (g(n)) (backward cost) and heuristic estimate (h(n)) (froward cost).

        :param problem: An instance of the Eightclass problem.
        :param heuristic: A callable function representing the heuristic to be used.
        :return: 
            - path: A list of actions that solve the puzzle.
            - len(path): The number of moves required to solve the puzzle.
            - expanded_nodes: A list of expanded nodes (states) during the search.
        """
        node = (heuristic(problem.initial_state), 0, problem.initial_state.to_tuple(), [])

        frontier = [node] 
        reached = {}
        expanded_nodes = []  
        while frontier:
            hcost, gcost, statetuple, path = heapq.heappop(frontier) 
            state = problem2.State(current_pos=statetuple[0], path=list(statetuple[1]), value=statetuple[2])
            if problem.goal_state(state):  
                return path, len(path), expanded_nodes  
            expanded_nodes.append(state)
            if statetuple in reached and reached[statetuple] <= gcost:
                continue  
            reached[statetuple] = gcost  
            for action in problem.actions(state):
                newstate = problem.result(state, action)
                newstatetuple = newstate.to_tuple()
                newpath = path + [action]
                newgcost = gcost + 1  
                newfcost = newgcost + heuristic(newstate, problem.goal)  #f(n) = g(n) + h(n)
                if newstatetuple not in reached or newgcost < reached[newstatetuple]: #If the new state has not been reached or if a better path is found, add it to the priority queue
                    heapq.heappush(frontier, (newfcost, newgcost, newstatetuple, newpath))
        
        return None 