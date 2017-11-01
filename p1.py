#Avery Tan(altan:1392212), Canopus Tong(canopus:1412275)



def read(grid):
    """
    Read the grid from stdin.
    Return the a two dimensional array,
    which contains two lists, empty_cell_coors  occupied_coors,
    in which it contains tuples (x,y).
       eg. [empty_cell_coors, occupied_coors] = [[(1,2),(2,3)], [(5,4),(4,3)]]
           
    """
    occupied_coors = set()
    empty_cell_coors = set()
    grid_coors = [empty_cell_coors, occupied_coors]
    N = len(grid)
    
    for y in range(N):
	    for x in range (N):
	        if grid[y][x] == '*':
		        occupied_coors.add((x,y))
	        else:
		        empty_cell_coors.add((x,y))
		
    return grid_coors



def write(N, grid_coors):
    """
    Print the grid to stdout using the two dimensional array generated from read().
    """
    grid = [['.']*N for i in range(N)]
        
    for coor in grid_coors[1]:
	    x = coor[0]
	    y = coor[1]
	    print(x,y)
	    grid[y][x] = '*'
    
    for line in grid:
	    for point in line:
	        print(point, end="")
	    print()
    
    
def main():
    N = int(input()) # Get the size of a NxN grid from stdin.
    grid = list()
    for i in range(1, N + 1): # Get the grid from stdin and put them in a list.
        grid.append(list(input()))
    
    grid_coors = read(grid) # Calls read() to get create data.
    write(N, grid_coors) # Calls write() to print to stdout.
    
	
if __name__ == "__main__":
	x=main()
