#!/usr/bin/env python3
"""
Author: JD Hamelink 
Initial Commit: 04-05-22
Search reachable positions in a 2D np.array representing a grid
"""

import numpy as np
import time

def main():

	height, width = 10, 10		# grid dimensions
	wall_density = .4			# how many walls will be in the grid
	render_pause = .2			# extra variable for visual_search()

	grid = initialize_grid(height, width, wall_density)
	print_array(grid)

	# starting position in grid: (y, x) or (row, col), set value to 0 to circumvent spawning in walls
	start: tuple[int, int] = (np.random.randint(1, height-1), np.random.randint(1, width-1))
	grid[start] = 0
	
	# print(f'starting point: {start}')

	tic = time.perf_counter()	# timer start

	# res = search(grid, start)
	res = BFSearch(grid, start)
	# res = visual_search(grid, start, render_pause)
	
	tac = time.perf_counter()	# timer end

	print_array(res)

	print(f'search took {(tac-tic)*1000:.3f} ms')	
	print_stats(grid, res)

	quit()


# --------------------------------- #
#		GRID INITIALIZATION			#
# --------------------------------- #

def initialize_grid(height: int = 10, width: int = 10, wall_density: float = .33) -> np.array:
	"""
	creates two-dimensional NumPy array with specified height, width, and wall density
	"""
	
	grid = np.zeros((height, width))

	grid[:,width-1] = 1
	grid[:,0] = 1
	grid[height-1,:] = 1
	grid[0,:] = 1

	for y in range(1, height-1):
		for x in range(1, width-1):
			if np.random.rand() < wall_density:
				grid[y,x] = 1

	return grid


# --------------------------------- #
# 			  ALGORITHMS			#
# --------------------------------- #

def search(grid: np.array, start: tuple[int, int] = (1, 1)) -> np.array:
	"""
	suboptimal algorithm
	"""

	res = grid.copy()
	res[start] = 2		# color starting point

	frontier = set()	# positions to be expanded
	frontier.add(start)
	expanded = True

	while expanded:
		expanded = False		# will remain False if no new positions are found
		new_frontier = set()	# will become next frontier
		for pos in frontier:
			for move in [(0,-1), (0,1), (-1,0), (1,0)]:
				neighbour = (pos[0]+move[0], pos[1]+move[1])
				if res[neighbour] == 0:
					new_frontier.add(neighbour)
					expanded = True
					res[neighbour] = 3 	# color reachable position
		frontier = new_frontier

	return res

def visual_search(grid: np.array, start: tuple[int, int] = (1, 1), render_pause: float = .2) -> np.array:
	"""
	same suboptimal algorithm, but with step by step visualization (returns the same result)
	"""

	res = grid.copy()
	res[start] = 2		# color starting point

	frontier = set()	# positions to be expanded
	frontier.add(start)
	expanded = True

	while expanded:
		expanded = False		# will remain False if no new positions are found
		new_frontier = set()	# will become next frontier
		for pos in frontier:
			for move in [(0,-1), (0,1), (-1,0), (1,0)]:
				neighbour = (pos[0]+move[0], pos[1]+move[1])
				if res[neighbour] == 0:
					new_frontier.add(neighbour)
					expanded = True
					res[neighbour] = 4 	# temporarily color new frontier differently
		
		print_array(res)
		time.sleep(render_pause)
		
		for new_pos in new_frontier:
			frontier.add(new_pos)
			res[new_pos] = 3			# color reachable position
		new_frontier.clear()

	return res

def BFSearch(grid: np.array, start: tuple[int, int] = (1, 1)) -> np.array:
	"""
	Breadth First Search implementation
	"""

	reachable_from = dict()
	for row in range(1, grid.shape[0]-1):
		for col in range(1, grid.shape[1]-1):
			if grid[row,col] == 0:
				reachable_from.update({(row, col): {nb for move in [(0,-1), (0,1), (-1,0), (1,0)] if grid[nb := (row+move[0], col+move[1])] == 0}})
	
	res = grid.copy()
	visited = set() 	# keep track of visited positions
	frontier = set()	# positions to be checked

	visited.add(start)
	frontier.add(start)
	res[start] = 2

	while frontier:
		pos = frontier.pop() 
		for neighbour in reachable_from[pos]:
			if neighbour not in visited:
				visited.add(neighbour)
				frontier.add(neighbour)
				res[neighbour] = 3
	
	return res


# --------------------------------- #
# 			HELPER FUNCTIONS		#
# --------------------------------- #

def print_array(grid: np.array) -> None:
	"""
	prints a colored representation of the grid
	"""

	# empty space: white
	# wall: black
	# starting point: red
	# reachable position: cyan
	# frontier: green
	d = {0: '\033[47m ', 1: '\033[40m ', 2: '\033[41m ', 3: '\033[46m ', 4: '\033[42m '}
	
	print()	# spacing

	for x in range(grid.shape[0]):
		for y in range(grid.shape[1]):
			print(d[grid[x,y]], end='')
		print('\033[0m')

	print()	# spacing

def print_stats(grid: np.array, res: np.array) -> None:
	"""
	prints some numbers about the search space
	"""
	empty: int = np.count_nonzero(grid == 0)
	reachable: int = np.count_nonzero(res == 3) + 1
	print(f'off all {empty} empty spaces, {reachable} are reachable')



if __name__ == '__main__':
	main()
