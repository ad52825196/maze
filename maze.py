import random

class maze:
    def get_neighbours(self, src):
        """This method returns a list of the cell locations that are adjacent to the source cell passed as a parameter
        """
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        neighbours = []
        for dx,dy in directions:
            x = src[0] + dx
            y = src[1] + dy
            if x in range(self.size) and y in range(self.size):
                neighbours.append((x, y))
        return sorted(neighbours)

    def blank_maze(self):
        """This method creates a blank maze. Each cell in the grid is connected to every adjacent cell. In other words, there are no walls
        """
        self.maze = {}
        for y in range(self.size):
            for x in range(self.size):
                self.maze[(x,y)] = self.get_neighbours((x,y))

    def __init__(self, size):
        """This method does the work of creating the maze. If the size of the maze is less than 1, then it should raise a ValueError with the message:"Maze must be at least size 1".

        *  The size is stored in a state variable called size

        When you have implemented full_maze, the constructor should call that method to generate the maze.
        """
        if size < 1:
            raise ValueError("Maze must be at least size 1")
        else:
            self.size = size
        self.full_maze()

    def get_corridors(self, src):
        """This method should return a list of all the cells (as x,y tuples) that can be reached from the source cell given as a parameter
        """
        return self.maze[src]

    def __repr__(self):
        """This method should return a string representation of the maze. It should simply format the dictionary containing the maze connections with each curly brace on their own line, and each entry of the dictionary on a separate line. The entries are given in sorted order based on the keys.

        For example, a maze with a size of 2 might be represented by the following string:
        {
        (0, 0):[(0, 1)]
        (0, 1):[(0, 0), (1, 1)]
        (1, 0):[(1, 1)]
        (1, 1):[(0, 1), (1, 0)]
        }
        """
        maze_string = "{\n"
        dict_keys = sorted(self.maze.keys())
        for key in dict_keys:
            maze_string += "(" + str(key[0]) + ", " + str(key[1]) + "):["
            for cell in self.maze[key]:
                maze_string += "(" + str(cell[0]) + ", " + str(cell[1]) + ")"
                if cell != self.maze[key][-1]:
                    maze_string += ", "
            maze_string += "]\n"
        maze_string += "}"
        return maze_string

    def pop_random_element(self, the_list):
        """This method picks a random element from a list, removes that element from the list and returns the element.
        """
        random_number = random.randrange(len(the_list))
        return the_list.pop(random_number)

    def add_connection(self, src, dst):
        """This method adds a link in the self.maze dictionary between the src and dst locations. These links will always occur in pairs, since a link from a to b is mirrored in the link from b to a.

        Note:  if the key already exists in the dictionary, then the link must
        be *appended* to the existing list of connections stemming from a, but 
        if the key does not exist, then you will have to create a new entry.
        """
        if src in self.maze:
            self.maze[src].append(dst)
            self.maze[src] = sorted(self.maze[src])
        else:
            self.maze[src] = [dst]
        if dst in self.maze:
            self.maze[dst].append(src)
            self.maze[dst] = sorted(self.maze[dst])
        else:
            self.maze[dst] = [src]

    def append_unique(self, src, dst):
        """This method appends the elements of the src list to the dst list, but only if they are not already in the dst list. In other words, the dst list is increased by adding new elements from the src list.
        """
        for element in src:
            if element not in dst:
                dst += [element]

    def partition_cells(self, locations):
        """This method divides the cells in the location list into two lists - those cells that are already in the maze (i.e. they are present in the dictionary called self.maze) and those cells that are not in the maze.

        The method should return both the inside and outside lists (in that order).
        """
        inside_list = []
        outside_list = []
        for cell in locations:
            if cell in self.maze:
                inside_list += [cell]
            else:
                outside_list += [cell]
        return inside_list, outside_list

    def full_maze(self):
        """This method generates the maze using Prim's algorithm. The algorithm is repeated below for convenience.
        """
        #Create a new empty dictionary to store the maze
        self.maze = {}
        #Add the location (0,0) to the maze with no cells connected to it
        self.maze[(0, 0)] = []
        #Create a frontier list containing the neighbouring cells of (0,0)
        frontier_list = self.get_neighbours((0, 0))

        #while the frontier list is not empty
        while len(frontier_list) != 0:
            #pick a random cell from the frontier list
            #the picked cell will be the next one we add to the maze
            cell_to_add = self.pop_random_element(frontier_list)

            #get the cells adjacent to the cell we picked
            adjacent_cells = self.get_neighbours(cell_to_add)

            #divide the adjacent cells into a list of cells that are already 
            #inside the maze, and cells that are not in the maze (outside)
            inside_list, outside_list = self.partition_cells(adjacent_cells)

            #pick a random cell from the list of cells that are in the maze
            random_cell_within_maze = self.pop_random_element(inside_list)

            #add a connection between the cell that we wanted to add, and 
            #the randomly chosen cell from within the maze
            self.add_connection(cell_to_add, random_cell_within_maze)

            #add the list of cells that was not in the maze (the adjacent cells
            #that are outside the maze) to the frontier list if they are not 
            #already in that list.
            self.append_unique(outside_list, frontier_list)
