#Avery Tan(altan:1392212), Canopus Tong(canopus:1412275)
#
#
#
#Requires queue python library
#
#
#



import p1
from queue import PriorityQueue



class Node(object):
    """
    class we use to make implement priority queue
    """

    def __init__(self,coor):
        self.coor = coor
        self.g=0
        self.h=0
        self.f=0
        self.parent = None


    def __lt__(self,other):
        if self.f<other.f:
            return True



def find_valid_moves(curr_coor, grid_coors):
    """
    returns all valid next states.
    inputs: curr_coor = tuple representing x and y coor of the curr position
            grid_coors = list containing 2 lists; the list containing tuples 
                        of all empty cells and the list containing tuples of 
                        all cells containing obstacles
    returns a list containing tuples representing possible next state transitions
    """
    x = curr_coor[0]
    y = curr_coor[1]
    empty_cell_coors = grid_coors[0]
    valid_moves = [] # udlr
    
    # up
    if (x, y-1) in empty_cell_coors:
        valid_moves.append((x, y-1))
    
    # down
    if (x, y+1) in empty_cell_coors:
        valid_moves.append((x, y+1))

    # left
    if (x-1, y) in empty_cell_coors:
        valid_moves.append((x-1, y))
    
    # right
    if (x+1, y) in empty_cell_coors:
        valid_moves.append((x+1, y))

    return valid_moves


def a_star(start, goal, grid, Htype):
    """
    A* algorithm
    inputs: start = tuple representing starting coordinates
            goal = tuple representing goal coordinates
            grid = list containing tuples of obstacles and free cells
            Htype =  string representing h=0 or h=M
    returns a string with the formatted result as specified in the assg spec
    """
    Open = PriorityQueue()
    Closed = dict()
    maxOpen = 1 #we already have one element in Open, the start state
    maxClosed = 0


    def get_sol(cn):
        '''
        this function takes as input a tuple representing (x,y) of the curr node 
        in which the curr node has stumbled upon the goal state

        returns a string representing the list of moves taken from the start state
        that takes the agent all the way to the goal state
        '''
        list_of_moves = ''

        #this dict stores move vectors and their names
        moves = {(0,1):'D', (0,-1):'U', (1,0):'R', (-1,0):'L'}
        

        while cn.coor != start: 
            parent_node = cn.parent
            x = cn.coor[0]-parent_node.coor[0]
            y = cn.coor[1]-parent_node.coor[1]
            ultimate_action = moves[(x,y)]
            list_of_moves = ultimate_action + list_of_moves
            cn = parent_node

        cost = len(list_of_moves)
        result_string = 'h='+Htype+' '+str(cost)+' '+str(maxOpen)+' '+str(maxClosed)+' '+\
                        str(start[0])+' '+str(start[1])+' '+str(goal[0])+' '+str(goal[1])+' '+list_of_moves
        return result_string

    s = Node(start) #create a Node object and place it into the priority Q
    Open.put(s)
    while not Open.empty(): 
        curr_node = Open.get()
        if curr_node.coor in Closed:
            continue
        else:
            Closed[curr_node.coor]=curr_node 
            if len(Closed)>maxClosed: #update the max size of Closed
                maxClosed = len(Closed)

        #are we at goal state?
        if curr_node.coor[0] == goal[0] and curr_node.coor[1]== goal[1]:
            solution = get_sol(curr_node)
            return solution

        #expand the search.
        curr_node_children= find_valid_moves(curr_node.coor,grid)
        for i in curr_node_children: #curr_node_children is now a list of tuples representing reachable next states
            successor=Node(i)
            successor.parent= curr_node
            successor.g = curr_node.g+1
            if Htype == 'M':
                successor.h = abs(successor.coor[0]-goal[0])+abs(successor.coor[1]-goal[1])
            else:
                successor.h = 0
            successor.f = successor.h+successor.g 
            if successor.coor not in Closed:
                Open.put(successor)
            if Open.qsize()>maxOpen: #keep track of max size of Open
                maxOpen = Open.qsize()

    #FAILURE
    result_string = 'h='+Htype+' '+'-1'+' '+str(maxOpen)+' '+str(maxClosed)+' '+\
                        str(start[0])+' '+str(start[1])+' '+str(goal[0])+' '+str(goal[1])
    return result_string


def main():
    N = int(input()) # Get the size of a NxN grid from stdin.
    grid = list() #where we will store each row of the grid as a list of strings
    sg = [] #where we will store start and goal states as a list of tuples (s,g)
    for i in range(1, N + 1): # Get the grid from stdin and put them into a list.
	    grid.append(list(input()))
    for i in range(N + 1, N + 2):
	    P = int(input())
    for i in range(N + 2, N + 2 + P): # Read the problems
	    input_sg = input().split()
	    s = (int(input_sg[0]), int(input_sg[1]))
	    g = (int(input_sg[2]), int(input_sg[3]))
	    input_sg = (s,g)
	    sg.append(input_sg)

    grid_coors = p1.read(grid) # Calls read() and create data.

    #go through each (start,goal) pair and run A*
    for i in range(len(sg)):
        ans=a_star(sg[i][0],sg[i][1],grid_coors, '0') #no heuristics
        print(ans)
        ans=a_star(sg[i][0],sg[i][1],grid_coors, 'M') # manhattan distance heuristics
        print(ans)
    

	
if __name__ == "__main__":
	x=main()