import numpy as np
import txt2graph
import itertools
from tqdm import tqdm

def gendirs(length, dim: int=2):
    return (itertools.product(list(range(2 ** dim)), repeat=length))

def genseq(length, dirs, dim: int=2):
    lattice = np.zeros([2 * length - 1] * dim, dtype=int)
    counter = 1
    coords = [length - 1] * dim
    mins = [length - 1] * dim
    maxs = [length - 1] * dim
    lattice[tuple(coords)] = 1

    mid = 2 ** (dim - 1)
    for dr in dirs:
        counter += 1
        if dr < mid:
            coords[dr] += 1
            maxs[dr] = max(maxs[dr], coords[dr])
        else:
            dr -= mid
            coords[dr] -= 1
            mins[dr] = min(mins[dr], coords[dr])
        if lattice[tuple(coords)] != 0:
            return None
        lattice[tuple(coords)] = counter
    return lattice[tuple([slice(x, y + 1) for x, y in zip(mins, maxs)])]

def genseqs(length, dim: int=2):
    return (genseq(length, dr, dim) for dr in gendirs(length - 1, dim))

def isograph(m1, m2):
    adjl1 = txt2graph.arr2adjl(m1)
    adjl2 = txt2graph.arr2adjl(m2)

    max1 = max(adjl1.keys())
    max2 = max(adjl2.keys())

    if max1 != max2:
        return False
    
    for vertex, adjset in adjl1.items():
        if adjset != adjl2[vertex]:
            return False
    else:
        return True
    for vertex, adjset in adjl1.items():
        if adjset != adjl2[max1 + 1 - vertex]:
            return False
    return True

def genseqswrapper(length:int, dim: int=2, dirname: str="chains") -> None:
    res = []
    for seq in tqdm(genseqs(length, dim), total=(2 ** dim) ** (length - 1)):
        if seq is not None:
            for oldseq in res:
                if isograph(oldseq, seq):
                    break
            else:
                res.append(seq)
    
    with open("{}/{}".format(dirname, str(length)), "w") as f:
        for chain in res:
            f.write(str(chain))