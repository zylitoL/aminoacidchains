import numpy as np

# reads delimited strings into a list of ints
def readints(s: str) -> list:
    return [int(i) for i in s.split()]

# reads in filename, returns array of matrix entries
def read(fname: str) -> np.array:
    chains = []
    with open(fname) as f:
        chain = []
        for line in f:
            line = line.strip()
            if not line:
                chains.append(np.array(chain))
                chain = []
            else:
                chain.append(np.array(readints(line)))
        chains.append(np.array(chain))
    return chains

# converts encoded array into adjacency list
# to avoid if statement labyrinths, we map the array onto an n + 2 by n + 2
# one for padding, then do the adjacency operations
def arr2adjl(arr: np.array) -> dict:
    dic = {}
    new = np.zeros((len(arr) + 2, len(arr[0]) + 2), dtype=int)
    for i, row in enumerate(arr):
        for j, entry in enumerate(row):
            new[i + 1][j + 1] = arr[i][j]
    
    for i, row in enumerate(new):
        for j, entry in enumerate(row):
            if entry == 0:
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
    mat = np.zeros((len(d), len(d)), dtype=int)
    for key, vals in d.items():
        mat[key - 1][key - 1] = 1
        for val in vals:
            if val == 0:
                continue
            mat[key - 1][val - 1] = mat[val - 1][key - 1] = 1
    return mat

def mats(fname):
    return [adjl2mat(arr2adjl(arr)) for arr in read(fname)]

def validate(edges: list, mats) -> bool:
    ret = []
    for i, mat in enumerate(mats):
        valid = True
        for edge in edges:
            if mat[edge[0], edge[1]] == 0:
                valid = False
        if valid:
            ret.append(mat)
    return ret

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