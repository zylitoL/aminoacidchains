import txt2graph

def validate(edges: list, mats: list) -> list:
    """Calculates the number of graphs in a list of adjacency matrix containing
    edges.

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

class Node:
    """Internal node class for pseudo-ID3 implementation. Describes a list of
    graphs.

    Fields:
        has: Non-exhaustive list of edges all graphs that the node describes
        necessarily have.
        nts: Non-exhaustive list of edges all graphs that the node describes
        do not have
        mats: List of adjacency matrices of graphs the node describes.
        edge: Potential edge
        left: Left node, all graphs from the node that do not have the potential
        edge.
        right: Right node, all graphs from the node that do have the potential
        edge.
    """
    def __init__(self, has, nts, mats):
        """Initailizer for a node. Consider class docstring for more detail.

        Args:
            has (list): List of edges
            nts (list): List of edges
            mats (list): List of adjacency matrices
        """
        self.has = copy(has)
        self.nts = copy(nts)
        self.mats = copy(mats)
        self.left = None
        self.right = None

def copy(l: list) -> list:
    """Shallow copies a list.

    Args:
        l (list): A list

    Returns:
        list: Copy of the list.
    """
    return [e for e in l]


def id3(node: Node, nodes: int=None) -> Node:
    """Implements a pseudo ID3 algorithm for graphs. For each node, considers
    all edges in the list of graphs it describes, and identifies the edge that
    most equally splits the list into graphs that do and do not have the edge.
    Creates the left and right children of the node, with the left child graphs
    not containing the edge and the right child graphs not containing the edge,
    and recursively applies the algorithm until only a single graph is uniquely
    described. Once a potential edge is found, it is added as a field to the
    node object. This creates a binary tree.

    Args:
        node (Node): Node
        nodes (int, optional): Number of vertices in the graphs.
        Defaults to None.

    Returns:
        Node: Node that has been id3'd.
    """
    if not nodes:
        # determines number of nodes by the dimension of the adjacency matrix
        nodes = len(node.mats[0])
    
    # If a graph is uniquely described, we are done.
    if len(node.mats) == 1 or len(node.mats) == 0:
        return None

    # Creates a list of edges and the graphs that contain it
    edges = []
    for i in range(nodes):
        for j in range(i + 1, nodes):
            if (i, j) in node.has or (i, j) in node.nts: # no repeats
                continue
            grphs = validate([(i, j)], node.mats)
            if grphs:
                edges.append((i, j, grphs))
    # Finds the edge that most closely splits the list in half
    edge = min(edges, key=lambda x: int(abs((len(node.mats) / 2) - len(x[2]))))

    # List of all matrices that do not contain the edge
    nots = [mat for mat in node.mats if mat[edge[0]][edge[1]] == 0]
    
    # Recurse on left
    node.left = Node(node.has, node.nts, nots)
    node.left.nts.append((edge[0], edge[1]))
    node.left = id3(node.left, nodes)
    
    # Recurse of right
    node.has.append((edge[0], edge[1]))
    node.right = Node(node.has, node.nts, edge[2])
    node.right = id3(node.right, nodes)

    # Denote the edge for the node
    node.edge = (edge[0], edge[1])

    return node

def traverse(node, edges=None) -> set:
    """DFS based traversal algorithm to determine the number of unique edges
    necessary in the ID3 algorithm.

    Args:
        node (Node): Root node of the ID3 tree
        edges (list): List of edges to return. Defaults to none.
    
    Returns:
        set of unique edges used in the ID3 algorithm.
    """
    if not edges:
        edges = set()

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

    

