import txt2graph
from typing import Mapping, Iterable
import numpy as np

def orthog(position: tuple[int, int]) -> list[tuple[int, int]]:
    """Returns a list of orthogonally adjacent positions to a given position on
    a 2-D lattice.

    Args:
        position: An iterable of 2 ints representing coordinates in a 2-D
            lattice.
    
    Returns:
        List: List of tuples representing orthogonally adjacent positions in a
        2-D lattice.
    """
    return [
        (position[0], position[1] + 1),
        (position[0], position[1] - 1),
        (position[0] + 1, position[1]),
        (position[0] - 1, position[1])
    ]

def croparray(lattice: np.array, placeholder=0) -> np.array:
    """Removes all placeholder elements from a 2-D array by returning the
    smallest contigious view that contains non-placeholder elements.

    Args:
        lattice: numpy array.
        placeholder: element to which to not consider in cropping the array.
            Defaults to 0.
    
    Returns:
        np.array: a view of the cropped numpy array
    """
    minx, miny = float("inf"), float("inf")
    maxx, maxy = float("-inf"), float("-inf")

    for x, row in enumerate(lattice):
        for y, entry in enumerate(row):
            if entry != placeholder:
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
    
    return lattice[minx:maxx + 1, miny:maxy + 1]

def pprint(lattice: np.array, frn: Iterable[tuple[int, int]]=None) -> None:
    """Prints the current lattice with fringe elements denoted.

    Args:
        lattice: The lattice with currently known placed vertices.
        frn: Fringe positions, consisting of a list of tuple representing
            coordinates in a 2-D lattice. Defaults to none.
    """
    lat = np.array(lattice, dtype="str")
    minx, miny = float("inf"), float("inf")
    maxx, maxy = float("-inf"), float("-inf")

    for x, row in enumerate(lattice):
        for y, entry in enumerate(row):
            if entry != 0:
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
                lat[x, y] = "{:2d}".format(entry)
            else:
                lat[x, y] = "  "
    if frn:
        for f in frn:
            x, y = f
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
            lat[f] = "??"
    print(lat[minx:maxx + 1, miny:maxy + 1])

def reconstruct(adjl: Mapping[int, Iterable[int]]) -> np.array:
    """Given an adjacency-DS representation of a graph, yields a (potentially)
    isomorphic array representing valid positions on a lattice of the vertices.

    Args:
        adjl: An adjacency-DS representation of a graph, mapping vertices to
            some iterable of their adjacent vertices.
    
    Returns:
        np.array: A view of the reconstructed array
    """
    # map from discovered degree to iterable of vertices
    vtx = [set(adjl.keys()), set(), set(), set(), set()]
    # map from vertex to discovered adjacencies
    discovered = {k: set() for k in adjl}

    lattice = np.zeros([2 * len(adjl) - 1] * 2, dtype=int)
    pos = {} # mapping vertices to their positions
    frn = set() # fringe coordinates
    placed = set() # placed vertices

    def updatefrn(position: tuple[int, int]) -> None:
        """Helper subroutine to update potential fringe locations around a given
        vertex.

        Args:
            position: A tuple representing the position to update in 2-D.
        """
        nonlocal lattice
        nonlocal frn
        vertex = lattice[position]
        # do not update around a non-placed position
        if vertex == 0:
            return
        # compute the current discovered degree of the vertex
        degree = 0
        for dev in orthog(position):
            if lattice[dev] != 0:
                degree += 1
        # if the vertex still has adjacencies, add neighboors to fringe
        # otherwise explicitly remove neighboors from fringe.
        for dev in orthog(position):
            if lattice[dev] == 0:
                frn.add(dev) if degree != len(adjl[vertex]) else frn.discard(dev)
    
    def updatearound(position: tuple[int, int]) -> None:
        """Helper subroutine to update data structures when a given vertex is
        placed in a given position.

        Updates pos: vertex->position, the placed set, vtx, the degree->list of
        vertices degree map, and the fringe of positions.

        Args:
            position: A tuple representing the position to update around.
        """
        nonlocal discovered
        nonlocal vtx
        nonlocal lattice
        nonlocal pos
        nonlocal frn
        nonlocal placed

        # update positions and fringe
        if position in frn:
            frn.remove(position)
        vertex = lattice[position]
        pos[vertex] = position

        placed.add(vertex)

        # remove vertex from degree map
        olddegree = len(discovered[vertex])
        vtx[olddegree].remove(vertex)
        
        # update non-placed adjacencies
        for neighboor in adjl[vertex]:
            if neighboor not in placed:
                discovered[neighboor].add(vertex)
                vtx[len(discovered[neighboor]) - 1].remove(neighboor)
                vtx[len(discovered[neighboor])].add(neighboor)
        
        # update fringes
        updatefrn(position)
        for neighboor in orthog(position):
            updatefrn(neighboor)
    
    def place1(vertex: int) -> None:
        """Helper subroutine to place vertices. For a given unplaced vertex that
        is adjacent to two other vertices, iterates over the neighbors of its
        adjacent vertices to identify the unique position of the vertex and
        places it in the lattice. 

        Args:
            vertex: A given vertex with multiple discovered adjacencies
        """
        nonlocal adjl
        nonlocal lattice
        nonlocal placed
        nonlocal discovered
        # for its neighbors, find their common neighneighboor
        candidates = set()
        for vtx in discovered[vertex]:
            if vtx in placed:
                options = {p for p in orthog(pos[vtx]) if lattice[p] == 0}
                if not candidates:
                    candidates = options
                else:
                    candidates = candidates.intersection(options)
        (victor,) = candidates
        lattice[victor] = vertex
        updatearound(victor)
    
    def place2() -> None:
        """Helper subroutine to place vertices. Performs a depth-limited depth-
        first search. Iterates over the fringe to find two orthogonally
        adjacent fringe positions. Identifies the vertices that are adjacent to
        the fringe positions, and then iterates over the adjacencies to find
        which two belong in the positions.
        """
        nonlocal adjl
        nonlocal frn
        nonlocal lattice
        # find two neighboring fringe points
        for f in frn:
            for neighboor in orthog(f):
                if neighboor in frn:
                    f1, f2 = f, neighboor
                    break
            else:
                continue
            break
        else:
            return
        
        # find the vertices the fringe points are adjacent to
        for neighboor in orthog(f1):
            vertex = lattice[neighboor]
            if vertex != 0:
                f1v = vertex
        for neighboor in orthog(f2):
            vertex = lattice[neighboor]
            if vertex != 0:
                f2v = vertex
        
        # brute force configurations
        for v1 in adjl[f1v]:
            if v1 in placed:
                continue
            for v2 in adjl[f2v]:
                if v2 in placed:
                    continue
                if v2 in adjl[v1]:
                    lattice[f1], lattice[f2] = v1, v2
                    updatearound(f1)
                    updatearound(f2)

 
    # first two must be hand placed
    lattice[len(adjl) - 1][len(adjl) - 1] = 1
    lattice[len(adjl) - 1][len(adjl)] = 2

    updatearound((len(adjl) - 1, len(adjl) - 1))
    updatearound((len(adjl) - 1, len(adjl)))

    # iterate until all vertices are found
    while len(placed) < len(adjl):
        # deductive
        for d in [2, 3, 4]:
            while vtx[d]:
                for v in vtx[d]:
                    place1(v)
                    break
        # depth limited dfs
        place2()
    
    return croparray(lattice)

def main():
    large_width = 400
    np.set_printoptions(linewidth=large_width)
    pprint(reconstruct(txt2graph.mat2adjs(txt2graph.mats("compact.txt")[1])))


if __name__ == "__main__":
    main()