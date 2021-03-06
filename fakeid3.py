import txt2graph

class Node:
    # do the actual subsetting in initalization
    def __init__(self, has, nts, mats):
        self.has = copy(has)
        self.nts = copy(nts)
        self.mats = copy(mats)
        self.left = None
        self.right = None

# shallow, lol
def copy(l: list) -> list:
    return [e for e in l]


def id3(node):
    if len(node.mats) == 1 or len(node.mats) == 0:
        return None # freedom

    edges = []
    for i in range(16):
        for j in range(16):
            if (i, j) in node.has or (i, j) in node.nts: # no repeats
                continue
            grphs = txt2graph.validate([(i, j)], node.mats)
            if grphs:
                edges.append((i, j, grphs))
    edge = min(edges, key=lambda x: int(abs((len(node.mats) / 2) - len(x[2]))))

    nots = [mat for mat in node.mats if mat[edge[0]][edge[1]] == 0]
    
    node.left = Node(node.has, node.nts, nots)
    node.left.nts.append((edge[0], edge[1]))
    node.left = id3(node.left)

    node.has.append((edge[0], edge[1]))
    node.right = Node(node.has, node.nts, edge[2])
    node.right = id3(node.right)

    node.edge = (edge[0], edge[1])

    return node

def traverse(node, edges):
    def dfs(node):
        nonlocal edges
        edges.add(node.edge)
        if node.left:
            dfs(node.left)
        if node.right:
            dfs(node.right)
    dfs(node)
    return edges
    
if __name__ == "__main__":
    root = Node([], [], txt2graph.mats("compact.txt"))
    id3(root)
    print(traverse(root, set()))
    print(len(traverse(root, set())))

    

