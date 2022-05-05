#!/usr/bin/env python3
"""
Author: JD Hamelink 
Initial Commit: 04-05-22
Search reachable positions in a 2D np.array representing a grid
"""

import numpy as np
import time

def main():

	height, width = 20, 20		# grid dimensions
	wall_density = .4			# how many walls will be in the grid
	render_pause = .2			# extra variable for visual_<search>() methods

	grid = initialize_grid(height, width, wall_density)

	# starting position in grid: (y, x) or (row, col)
	start: tuple[int, int] = (np.random.randint(1, height-1), np.random.randint(1, width-1))
	# set value to 0 to circumvent spawning in walls
	grid[start] = 0
	
	visualize: bool = True if input('Press any key and ENTER to visualize, press ENTER directly to skip this\n>') \
						   else False
	if visualize:
		for visual_method in [visual_DSearch, visual_BFSearch, visual_DFSearch]:
			print(f'now running: \033[1m{visual_method.__name__}\033[0m' + '\n' * height)
			time.sleep(1)
			visual_method(grid, start, render_pause)
	
	for method in [DSearch, BFSearch, DFSearch]:
		res, duration = timer(method, grid, start)
		print_stats(method, grid, res, wall_density, start, duration, printgrids=False)

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

def DSearch(grid: np.array, start: tuple[int, int] = (1, 1)) -> np.array:
	"""
	Direct Search
	---
	so far the quickest algorithm, that is in essence a BFS algorithm, but operates directly on the grid
	rather than creating a graph (represented by a dictionary) first
	"""

	res = grid.copy()
	res[start] = 2		# color starting point

	frontier = set()	# positions to be expanded
	frontier.add(start)

	while frontier:
		new_frontier = set()	# will become next frontier
		for pos in frontier:
			for move in [(0,-1), (0,1), (-1,0), (1,0)]:
				neighbour = (pos[0]+move[0], pos[1]+move[1])
				if res[neighbour] == 0:
					new_frontier.add(neighbour)
					res[neighbour] = 3 	# color reachable position
		frontier = new_frontier

	return res

def visual_DSearch(grid: np.array, start: tuple[int, int] = (1, 1), render_pause: float = .2) -> np.array:
	"""
	same DS algorithm, but with step by step visualization (returns the same result)
	"""

	res = grid.copy()
	res[start] = 2		# color starting point

	frontier = set()	# positions to be expanded
	frontier.add(start)

	while frontier:
		new_frontier = set()	# will become next frontier
		for pos in frontier:
			for move in [(0,-1), (0,1), (-1,0), (1,0)]:
				neighbour = (pos[0]+move[0], pos[1]+move[1])
				if res[neighbour] == 0:
					new_frontier.add(neighbour)
					res[neighbour] = 4 	# temporarily color new frontier differently
		
		print_array(res)
		time.sleep(render_pause)
		
		frontier.clear()
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
				reachable_from.update({(row, col): {nb for move in [(0,-1), (0,1), (-1,0), (1,0)] \
											if grid[nb:=(row+move[0], col+move[1])] == 0}})
	
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

def visual_BFSearch(grid: np.array, start: tuple[int, int] = (1, 1), render_pause: float = .2) -> np.array:
	"""
	same Breadth First Search implementation, but with step by step visualization (returns the same result)
	
	this visualization is slightly different from the last one, because this implementation of BFS doesn't
	iteratively keep a separate set of what the new frontier is
	"""

	def update_grid(grid: np.array, frontier: set[tuple]) -> np.array:
		"""for annoying coloring purposes"""
		for pos in frontier:
			grid[pos] = 4 if grid[pos] != 2 else 2
		return grid

	reachable_from = dict()
	for row in range(1, grid.shape[0]-1):
		for col in range(1, grid.shape[1]-1):
			if grid[row,col] == 0:
				reachable_from.update({(row, col): {nb for move in [(0,-1), (0,1), (-1,0), (1,0)] \
											if grid[nb:=(row+move[0], col+move[1])] == 0}})
	
	res = grid.copy()
	visited = set() 	# keep track of visited positions
	frontier = set()	# positions to be checked

	visited.add(start)
	frontier.add(start)
	res[start] = 2

	render_pause /= 5	# BFS prints way more iterations when compared to DS

	while frontier:
		pos = frontier.pop()
		res[pos] = 3 if res[pos] != 2 else 2
		for neighbour in reachable_from[pos]:
			if neighbour not in visited:
				visited.add(neighbour)
				frontier.add(neighbour)
				res[neighbour] = 4 # if grid[pos] != 2 else 2
		print_array(res)
		time.sleep(render_pause)
		res = update_grid(res, frontier)

	return res


def DFSearch(grid: np.array, start: tuple[int, int] = (1, 1)) -> np.array:
	"""
	Depth First Search implementation
	"""

	def dfs(res: np.array, visited: set, reachable_from: dict[tuple: set[tuple]], pos: tuple[int, int]):
		"""recursive dfs algorithm, updates "global" res array"""
		if pos not in visited:
			visited.add(pos)
			res[pos] = 3
			for neighbour in reachable_from[pos]:
				dfs(res, visited, reachable_from, neighbour)

	reachable_from = dict()
	for row in range(1, grid.shape[0]-1):
		for col in range(1, grid.shape[1]-1):
			if grid[row,col] == 0:
				reachable_from.update({(row, col): {nb for move in [(0,-1), (0,1), (-1,0), (1,0)] \
											if grid[nb:=(row+move[0], col+move[1])] == 0}})
	
	res = grid.copy()
	visited = set()
	
	dfs(res, visited, reachable_from, start)
	res[start] = 2

	return res

def visual_DFSearch(grid: np.array, start: tuple[int, int] = (1, 1), render_pause: float = .2) -> np.array:
	"""
	same Depth First Search implementation, but with step by step visualization (returns the same result)
	
	this visualization is again slightly different from the last one, because DFS recursive properties
	only allow for rendering every single step
	"""

	def dfs(res: np.array, visited: set, reachable_from: dict[tuple: set[tuple]], pos: tuple[int, int],
			render_pause: float, prev_idx: int = 0, frontier: set = set()):
		"""
		recursive dfs algorithm, does not update "global" res array
		----
		it's a lot more complicated than the one in the regular DFSearch algorithm, but luckily
		I am the only one that has to understand what it does (I don't really)
		"""
		if pos not in visited:
			visited.add(pos)
			frontier.add(pos)
			res[pos] = 4 if len(visited) != 1 else 2
			print_array(res)
			time.sleep(render_pause)
			for idx, neighbour in enumerate(reachable_from[pos]):
				if idx == len(reachable_from[pos])-1:
					res = update_grid(res, frontier)
				prev_idx = idx
				dfs(res, visited, reachable_from, neighbour, render_pause, prev_idx, frontier)
		return res
	
	def update_grid(grid: np.array, frontier: set[tuple]) -> np.array:
		for pos in frontier:
			grid[pos] = 3 if grid[pos] != 2 else 2
		return grid

	reachable_from = dict()
	for row in range(1, grid.shape[0]-1):
		for col in range(1, grid.shape[1]-1):
			if grid[row,col] == 0:
				reachable_from.update({(row, col): {nb for move in [(0,-1), (0,1), (-1,0), (1,0)] \
											if grid[nb:=(row+move[0], col+move[1])] == 0}})
	
	res = grid.copy()
	visited = set()
	
	render_pause /= 2	# DFS also prints some more iterations when compared to DS

	res = dfs(res, visited, reachable_from, start, render_pause)
	print_array(res)

	return res


# --------------------------------- #
# 			HELPER FUNCTIONS		#
# --------------------------------- #

def timer(f, *args) -> tuple[any, float]:
	"""
	computes the time it takes to perform a given function and returns its result, and this duration
	"""
	tic: float = time.perf_counter()	# timer start
	res = f(*args)
	toc: float = time.perf_counter()	# timer end
	return res, toc-tic

def print_array(grid: np.array) -> None:
	"""
	prints a colored representation of the grid
	"""

	# 0 | white | empty space 
	# 1 | black | wall
	# 2 | red   | starting point
	# 3 | cyan  | reachable position
	# 4 | green | frontier
	d = {0: '\033[47m  ', 1: '\033[40m  ', 2: '\033[41m  ', 3: '\033[46m  ', 4: '\033[42m  '}
	
	print()	# spacing

	for x in range(grid.shape[0]):
		for y in range(grid.shape[1]):
			print(d[grid[x,y]], end='')
		print('\033[0m')

	print()	# spacing

def print_stats(f, grid: np.array, res: np.array, wall_density: float, start: tuple[int, int],
				duration: float, printgrids: bool = True) -> None:
	"""
	prints some numbers about the search
	"""
	print(f'method: \033[1m{f.__name__}\033[0m')
	print(f'dimensions: {grid.shape[0]}x{grid.shape[1]} (HxW)')
	print(f'wall density: {wall_density}')
	_ = print_array(grid) if printgrids else None
	_ = print(f'starting point: {start}') if printgrids else None
	_ = print_array(res) if printgrids else None
	print(f'of all {np.count_nonzero(grid == 0)} empty spaces, {np.count_nonzero(res == 3) + 1} are reachable')
	print(f'search took {(duration)*1000:.3f} ms\n')



if __name__ == '__main__':
	main()
