from itertools import chain, combinations
import txt2graph

def powerset(i):
    s = list(i)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def complement_edgeset(edges):
    complement = {(i, j) for i in range(16) for j in range(16)}
    for edge in edges:
        complement.remove(edge)
    return complement

def bruteforce(matrices):
    for i, mat in enumerate(matrices):
        print("considering graph {}".format(i))
        for pset in powerset(txt2graph.edgeset(mat)):
            found = False
            for mat2 in matrices:
                valid = True
                for edge in pset:
                    if mat2[edge[0]][edge[1]] == 0:
                        valid = False
                if valid:
                    break
            else:
                found = True
                print("match found")
                print(pset)
                break
        else:
            print("no match found")

if __name__ == "__main__":
    bruteforce(txt2graph.mats("compact.txt"))
                