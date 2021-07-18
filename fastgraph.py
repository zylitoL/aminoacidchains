import numpy as np

"""
A rewrite of txt2graph.py with local space in mind, and lower level data.

Instead of regular amino acid contact maps, we use a compressed variation. We
assume that a given amino acid is only on contact with immediately adjacent
entries in a lattice. For instance, an amino acid at position (x, y, z) can
only be adjacent to amino acids with (x, y, z), with +/- 1 to precisely one
coordinate. Hence for each axis, there are 2 possible deviations for an
adjacency and thus there are 2 * dimension number of possible adjacencies for
a given amino acid.

Hence instead of a traditional n x n adjacency matrix where n is number of
amino acids, we can instead do a n x 2 * dim adjacency (uh, array) instead,
since we label from 0 to n - 1 anyways.
"""

def arr2adjs(arr: np.array, length: int) -> np.array:
    """Converts an array into an adjacency array.

    For performance reasons, the adjacency array is padded with -1s on the
    right end if there is extra space.

    Args:
        arr (np.array): Lattice representation of amino acid chain.
        length (int): Number of amino acids.

    Returns:
        np.array: Adjacency array.
    """
    adjs = np.full((length, 4), -1)
    maxrow, maxcol = arr.shape
    for i, row in enumerate(arr):
        for j, entry in enumerate(row):
            if entry == -1:
                continue
            adj = []
            # sorting is faster then manually checking and padding
            if i == 0:
                if j == 0:
                    adj.append(arr[i + 1][j])
                    adj.append(arr[i][j + 1])
                    adj.append(-1)
                    adj.append(-1)
                elif j == maxcol - 1:
                    adj.append(arr[i + 1][j])
                    adj.append(arr[i][j - 1])
                    adj.append(-1)
                    adj.append(-1)
                else:
                    adj.append(arr[i + 1][j])
                    adj.append(arr[i][j + 1])
                    adj.append(arr[i][j - 1])
                    adj.append(-1)
            elif i == maxrow - 1:
                if j == 0:
                    adj.append(arr[i - 1][j])
                    adj.append(arr[i][j + 1])
                    adj.append(-1)
                    adj.append(-1)
                elif j == maxcol - 1:
                    adj.append(arr[i - 1][j])
                    adj.append(arr[i][j - 1])
                    adj.append(-1)
                    adj.append(-1)
                else:
                    adj.append(arr[i - 1][j])
                    adj.append(arr[i][j + 1])
                    adj.append(arr[i][j - 1])
                    adj.append(-1)
            else:
                if j == 0:
                    adj.append(arr[i + 1][j])
                    adj.append(arr[i - 1][j])
                    adj.append(arr[i][j + 1])
                    adj.append(-1)
                elif j == maxcol - 1:
                    adj.append(arr[i + 1][j])
                    adj.append(arr[i - 1][j])
                    adj.append(arr[i][j - 1])
                    adj.append(-1)
                else:
                    adj.append(arr[i + 1][j])
                    adj.append(arr[i - 1][j])
                    adj.append(arr[i][j + 1])
                    adj.append(arr[i][j - 1])
            
            adj.sort(reverse=True)
            adjs[entry - 1] = np.array(adj)
    return adjs

def isograph(adjs1: np.array, adjs2: np.array) -> bool:
    """Determines from adjacency arrays if amino acid chains are isomorphic.

    As amino acid chains are fundamentally path graphs, there are only two
    canonical labelings if the amino acids go in sequential order, a "forward"
    and "backward". Hence we check if the arrays are exactly equal, or if equal
    should one go backward.
    
    Args:
        adjs1 (np.array): Adjacency array of amino acid chain.
        adjs2 (np.array): Adjacency array of amino acid chain.

    Returns:
        bool: If the two amino acid chains are isomorphic.
    """
    return np.array_equal(adjs1, adjs2) or np.array_equal(np.fliplr(adjs1), adjs2)
    