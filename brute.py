from itertools import chain, combinations
import numpy as np
import txt2graph

def powerset(i):
    """Creates the powerset of an iterable.
    From https://docs.python.org/3/library/itertools.html#itertools-recipes

    Args:
        i (iterable): Iterable to create the powerset of

    Returns:
        generator: Powerset of the iterable
    """
    s = list(i)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def complement_edgeset(edges: set, nodes:int):
    """Method to find the complement of edges from an edge set of a graph

    Args:
        edges (set): Set of edges
        nodes (int): Number of nodes in the graph

    Returns:
        set: Complementary set
    """
    complement = {(i, j) for i in range(nodes) for j in range(nodes)}
    for edge in edges:
        complement.remove(edge)
    return complement

def bruteforce(matrices: list) -> list:
    """For each matrix, identifies the minimal edge set that uniquely identifies
    the matrix.

    Args:
        matrices (list): List of adjacency matrices

    Returns:
        set: Set of edges that uniquely identifies each matrix.
    """
    res = []
    for i, mat in enumerate(matrices):
        # print("considering graph {}".format(i))
        for j, pset in enumerate(powerset(txt2graph.edgeset(mat))):
            # print("considering powerset {}".format(j))
            found = False
            for mat2 in matrices:
                # ignore the same matrix
                if np.array_equal(mat, mat2):
                    continue
                # check to see if the edges can identify the given matrix
                valid = True
                for edge in pset:
                    if mat2[edge[0]][edge[1]] == 0:
                        valid = False
                # if so, invalid edge set
                if valid:
                    break
            # if no breaks, match was found, do not have to consider more sets
            else:
                found = True
                # print("match found")
                # print(pset)
                res.append(pset)
                break
        # if no breaks, no match was found
        else:
            # print("no match found")
            res.append(None)
    return res

if __name__ == "__main__":
    funedges = bruteforce(txt2graph.mats("compact.txt"))
    with open("funedgescompact.txt", "w") as f:
        for edge in funedges:
            f.write(str(edge))
            f.write("\n")
                