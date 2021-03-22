import numpy as np

def readints(s: str) -> list:
    """Helper function that reads in a line of integers in the form of a space
    delimited string, and returns a list of integers. Defaults to returning
    -1 if the "integer" entry in the string is an X, as a placeholder. Integers
    should be non-negative.

    Args:
        s (str): String of spaced integers or "X"s.
            Example: "1 2 3 X 7 12 X X"

    Returns:
        list: List of integers, with Xs replaced with -1s.
    """
    ints = []
    for i in s.split():
        if i == "X":
            ints.append(-1)
        else:
            ints.append(int(i))
    return ints

def read(fname: str) -> np.array:
    """Reads a file of integer matrices and returns list of numpy arrays. Uses
    readints to read each line, so accepts X and interprets to be empty using
    -1 as a placeholder. File should not have a trailing newline.

    Args:
        fname (str): Filename

    Returns:
        list: List of arrays
    """
    chains = []
    with open(fname) as f:
        chain = []
        for line in f:
            line = line.strip()
            # empty line implies end of array
            if not line:
                chains.append(np.array(chain))
                chain = []
            else:
                chain.append(np.array(readints(line)))
        # include last line
        chains.append(np.array(chain))
    return chains

def arr2adjl(arr: np.array) -> dict:
    """Interprets numpy array of integer entries as a lattice graph, and returns
    an adjacency list representation using a dictionary mapping integer entries
    to a list of adjacent integers.

    Args:
        arr (np.array): Array of integers

    Returns:
        dict: Adjacency list
    """
    dic = {}
    # To avoid numerous if statements, we map the numpy array into one of size
    # (n + 2) x (n + 2), and pad the border with zeros. Then for each element
    # we can simply look at its 4 neighbors, and treat the zeros later.
    new = np.zeros((len(arr) + 2, len(arr[0]) + 2), dtype=int)
    for i, row in enumerate(arr):
        for j, entry in enumerate(row):
            new[i + 1][j + 1] = arr[i][j]
    
    for i, row in enumerate(new):
        for j, entry in enumerate(row):
            # ignore placeholders
            if entry == 0 or entry == -1:
                continue
            if entry not in dic:
                dic[entry] = []
            dic[entry].append(new[i - 1][j])
            dic[entry].append(new[i][j - 1])
            dic[entry].append(new[i + 1][j])
            dic[entry].append(new[i][j + 1])
    
    return dic

# converts adjacency lists to arrays, ignoring 0s
def adjl2mat(d: dict) -> np.array:
    """Converts the dictionary of an adjacency list representation of a graph
    into an adjacency matrix. Ignores 0 entries. Entries are decremented by 1,
    so if the vertices are enumerated 1 to n, the adjacency list is returned in
    form 0 to n - 1.

    Args:
        d (dict): Adjacency list

    Returns:
        np.array: Adjacency matrix
    """
    mat = np.zeros((len(d), len(d)), dtype=int)
    for key, vals in d.items():
        mat[key - 1][key - 1] = 1
        for val in vals:
            if val == 0 or val == -1:
                continue
            mat[key - 1][val - 1] = mat[val - 1][key - 1] = 1
    return mat

def mats(fname: str) -> list:
    """Returns a list of adjacency matrices from a file containing entries of
    matrices.

    Args:
        fname (str): Filename

    Returns:
        list: List of adjacency matrices
    """
    return [adjl2mat(arr2adjl(arr)) for arr in read(fname)]

def edgeset(mat):
    """Returns the set of edges for a given adjacency matrix

    Args:
        mat ([type]): Adjacency matrix

    Returns:
        [type]: Edge set
    """
    edges = set()
    for i, row in enumerate(mat):
        for j, entry in enumerate(row):
            if i < j - 1:
                continue
            if entry == 1:
                edges.add((i, j))
    return edges

def dfsmax(ds, maxelem=float("-inf")) -> int:
    """DFS based algorithm to determine the maximum element in a nested
    iterable data structure/

    Args:
        ds (iterable): A data structure
        maxelem (int, optional): Current maximal element.
        Defaults to float("-inf").

    Returns:
        int: Maximal element.
    """
    # If we have recursed to a single element, len will not work.
    try:
        if len(ds):
            for elem in ds:
                # Recursively consider the maximum of all children
                maxelem = max(maxelem, dfsmax(elem))
            return maxelem
    except TypeError:
        # Single element
        return max(maxelem, ds)

def validate(edges: list, mats: list) -> list:
    """Calculates the graphs in a list of adjacency matrix containing the edges.

    Args:
        edges (list): List of edges
        mats (list): List of adjacency matrices

    Returns:
        list: graphs containing edges
    """
    ret = []
    for i, mat in enumerate(mats):
        valid = True
        for edge in edges:
            if mat[edge[0], edge[1]] == 0:
                valid = False
        if valid:
            ret.append(mat)
    return ret

def copy(l: list) -> list:
    """Shallow copies a list.

    Args:
        l (list): A list

    Returns:
        list: Copy of the list.
    """
    return [e for e in l]

def main():
    with open("mats.txt", "w") as f:
        for mat in mats("compact.txt"):
            for row in mat:
                f.write(str(row[0]))
                for entry in row[1:]:
                    f.write(" {}".format(entry))
                f.write("\n")
            f.write("\n")

if __name__ == "__main__":
    main()