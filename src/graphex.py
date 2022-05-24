class Graph():
    def __init__(self, weighted=False, directed=False) -> None:
        '''
        Our graph is a dictionary of tuples, in which each node 'u' points to
        a list of tuples in the form (v, w), where 'v' is a node and 'w' is the
        the wight of the edge (u, v)
        '''
        self._G = dict()

        self._weighted = weighted   # If not weighted, every edge receives weight 1
        self._directed = directed   # If directed, both (u, v) and (v, u) are added to G
    
    def get_nodes(self) -> list:
        return self._G.keys()
    
    def get_edges(self) -> list:
        edges = []

        for u in self.get_nodes():
            for v, w in self.get_adjacency_list(u):
                if self._weighted:
                    edge = (u, v, w)
                else:
                    edge = (u, v)

                edges.append(edge)
        
        # Removing duplicates by turning the list into a set
        return list(set(edges))
    
    def get_adjacency_list(self, node) -> list:
        if node in self.get_nodes():
            return self._G[node]
        else:
            raise KeyError('{node} is not a node of the graph')

    def add_nodes(self, nodes) -> None:
        # If only one node is provided, we turn it into a list
        if not isinstance(nodes, list):
            nodes = [nodes]

        for node in nodes:
            self._G[node] = []
    
    def add_edges(self, edges) -> None:
        # If only one edge is provided, we turn it into a list
        if not isinstance(edges, list):
            edges = [edges]

        for edge in edges:
            if self._weighted:
                u, v, w = edge

            else:
                u, v = edge
                w = 1
            
            if u not in self.get_nodes():
                self.add_nodes(u)
            self._G[u].append((v, w))

            # An undirected graph has both edges (u, v) and (v, u)
            if not self._directed:
                if v not in self.get_nodes():
                    self.add_nodes(v)
                self._G[v].append((u, w))
