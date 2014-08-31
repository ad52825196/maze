"""
This module is designed to show a graphical representation of a maze.

This module requires the maze class to have the following methods and variables:

maze.size #the size of the maze
maze.get_corridors(src) #a list of cells that can be reached from the src cell
maze.get_neighbours(src) #a list of cells that are adjacent to the src cell
"""

from maze import *

def get_coords(src, dst, top_left, cell_size):
    #calculates the coordinates of the wall
    #between the src and dst cells
    horizontal = dst[0] - src[0]
    vertical = dst[1] - src[1]
    sx = sy = dx = dy = 0 #offsets for walls
    
    #calculate offsets
    if (horizontal, vertical) == (0, -1): #north
        sx = sy = dy = 0
        dx = 1
    elif (horizontal, vertical) == (0, 1): #south
        sx = 0
        dx = sy = dy = 1
    elif (horizontal, vertical) == (-1, 0): #west
        sx = dx = sy = 0
        dy = 1
    elif (horizontal, vertical) == (1, 0): #east
        sx = dx = dy = 1
        sy = 0
    #use offsets to calculate the start and end locations
    #of a wall
    x1 = top_left[0] + (src[0] + sx) * cell_size
    y1 = top_left[1] + (src[1] + sy) * cell_size
    x2 = top_left[0] + (src[0] + dx) * cell_size
    y2 = top_left[1] + (src[1] + dy) * cell_size
    return (x1, y1, x2, y2)
    
def draw(maze):
    #define the available drawing region
    canvas_width = 650
    canvas_height = 450
    max_size = min(canvas_width - 10, canvas_height - 10)
    
    #create the canvas to draw the maze
    import tkinter
    canvas = tkinter.Canvas(tkinter.Tk(), width=canvas_width, height=canvas_height)
    canvas.pack() 
    
    #calculate the size and positions to draw
    #centre the maze in the window
    cell_size = max_size // maze.size
    offset_x = (canvas_width - cell_size * maze.size) // 2
    offset_y = (canvas_height - cell_size * maze.size) // 2
    top_left = (offset_x, offset_y)
            
    #draw the outline of the maze
    canvas.create_rectangle(offset_x, 
                            offset_y, 
                            offset_x + cell_size* maze.size, 
                            offset_y + cell_size*maze.size, 
                            outline="black", fill="white")
    
    #for each cell in the maze
    for mx in range(maze.size):
        for my in range(maze.size):
            #get a list of adjacent cells, and the 
            #cells that have no walls between them
            location = (mx, my)
            corridors = maze.get_corridors(location)
            neighbours = maze.get_neighbours(location)
            for adjacent in neighbours:
                if adjacent not in corridors:
                    #if the cell is adjacent and it is a wall, then draw the line
                    x1, y1, x2, y2 = get_coords(location, adjacent, top_left, cell_size)
                    canvas.create_line(x1, y1, x2, y2, fill="black") 
    #pause until the user closes the window
    tkinter.mainloop() 

#create a maze of a specific size and draw it.
#anything over around 100 starts to get slow
m = maze(20)   
draw(m)