import txt2graph
import numpy as np

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
        self.has = txt2graph.copy(has)
        self.nts = txt2graph.copy(nts)
        self.mats = txt2graph.copy(mats)
        self.left = None
        self.right = None

def id3wrapper(mats):
    ans = txt2graph.copy(mats)
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
        if len(node.mats) == 1:
            nonlocal ans
            for i, mat in enumerate(ans):
                if np.array_equal(mat, node.mats[0]):
                    ans[i] = (node.has, node.nts)
                    break
            return None
        if len(node.mats) == 0:
            return None

        # Creates a list of edges and the graphs that contain it
        edges = []
        for i in range(nodes):
            for j in range(i + 1, nodes):
                if (i, j) in node.has or (i, j) in node.nts: # no repeats
                    continue
                grphs = txt2graph.validate([(i, j)], node.mats)
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
    id3(Node([], [], mats))
    return ans

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
    print(id3wrapper(txt2graph.mats("compact.txt")))

    

