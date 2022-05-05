GridSearch
==========
Some algorithms to visualize the process of finding all reachable spaces in a 2D grid

For now, there are three search algorithms:
- BFS (Breadth First Search)
- DFS (Depth First Search)
- DS ("Direct" Search)

Breadth First Search
--------------------
Picks a random position on the frontier that has not been explored yet, and colors all of its direct neighbours.

Depth First Search
------------------
Picks a random position on the frontier and immediately expands its first neighbour, then that neighbour expands its first neighbour, and on and on until a position is found that has no new neighbours to discover.
In that case, the algorithm moves up recursively to expand other neighbours.

<fig>
  <img src="https://github.com/Josef-Hlink/GridSearch/blob/main/assets/DFS.gif" width="256" height="256" alt="DFS demo"/>
  <figcaption>Depth First Search on a 20x20 grid with ±40% walls</figcaption>
</fig>

"Direct" Search
---------------
In essence just BFS, but implemented more efficiently as the process of the creation of a graph representation is left out.
