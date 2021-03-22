import txt2graph

def _minhitset(edgeset: set, matset: set, edges: list=None):
    if not edges:
        edges = []

    while edgeset and matset:
        dqlst = (None, matset)
        # finds the edge that has the fewest graphs in common
        for edge in edgeset:
            dqlst = min(
                dqlst,
                (edge, [mat for mat in matset if mat[edge[0]][edge[1]] == 1]),
                key=lambda x: len(x[1])
            )
        # records best edge
        edges.append(dqlst[0])
        # removes edge
        edgeset.remove(dqlst[0])
        # consider only the remaining graphs
        matset = dqlst[1]
    return edges if edgeset else None
   


def minhitset(mats):
    res = []
    for i, mat1 in enumerate(mats):
        edges = txt2graph.edgeset(mat1)

        copy = [mat for mat in mats if not (mat==mat1).all()]
        res.append(_minhitset(edges, copy, []))
    return res

if __name__ == "__main__":
    print(minhitset(txt2graph.mats("compact.txt")))
