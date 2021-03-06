class Graph():

    def __init__(self, weighted=False, directed=False) -> None:
        '''
        Our graph is a dictionary of tuples, in which each node 'u' points to
        a list of tuples in the form (v, w), where 'v' is a node and 'w' is the
        the weight of the edge (u, v)
        '''
        self._G = dict()

        self._weighted = weighted   # If not weighted, every edge receives weight 1
        self._directed = directed   # If directed, both (u, v) and (v, u) are added to G


    def get_nodes(self) -> list:
        return list(self._G.keys())
    

    def get_edges(self) -> list:
        edges = []

        for u in self.get_nodes():
            for v, _ in self.get_adjacency_list(u):
                edges.append((u, v))
        
        return edges
    

    def get_adjacency_list(self, node) -> list:
        if node in self.get_nodes():
            return self._G[node]
        else:
            raise KeyError('{} is not a node of the graph'.format(node))
    

    def get_weight(self, edge: tuple):
        u, v = edge

        for node, weight in self.get_adjacency_list(u):
            if node == v:
                return weight
        
        raise KeyError('Edge {} is not in the graph'.format((u, v)))


    def add_nodes(self, nodes) -> None:
        # If only one node is provided, we turn it into a list
        if not isinstance(nodes, list):
            nodes = [nodes]

        for node in nodes:
            if node not in self.get_nodes():
                self._G[node] = []
    

    def add_edges(self, edges) -> None:
        # If only one edge is provided, we turn it into a list
        if not isinstance(edges, list):
            edges = [edges]

        for edge in edges:
            if self._weighted:
                if len(edge) != 3:
                    raise TypeError('Edges in a weighted graph must be in the form (u, v, w)')
                
                u, v, w = edge
            else:
                if len(edge) != 2:
                    raise TypeError('Edges in an unweighted graph must be in the form (u, v)')

                u, v = edge
                w = 1
            
            # If (u, v) is already in the graph, we override its weight
            if (u, v) in self.get_edges():
                if self._weighted:
                    self.update_weight((u, v), w)        
                break
            
            # Node 'u' is added do the graph if not existent
            if u not in self.get_nodes():
                self.add_nodes(u)
            self._G[u].append((v, w))

            # An undirected graph has both edges (u, v) and (v, u)
            if not self._directed:
                if v not in self.get_nodes():
                    self.add_nodes(v)
                self._G[v].append((u, w))
    

    def update_weight(self, edge: tuple, weight) -> None:
        u, v = edge

        for i, (node, _) in enumerate(self.get_adjacency_list(u)):
            if node == v:
                self._G[u][i] = (node, weight)
        
        # Updating the weight for both (u, v) and (v, u) if not directed
        if not self._directed:
            for i, (node, _) in enumerate(self.get_adjacency_list(v)):
                if node == u:
                    self._G[v][i] = (node, weight)


    def remove_nodes(self, nodes):
        # If only one node is provided, we turn it into a list
        if not isinstance(nodes, list):
            nodes = [nodes]
        
        for node in nodes:
            if node not in self.get_nodes():
                raise KeyError('{} is not a node of the graph'.format(node))
            else:
                del self._G[node]
                for edge in self.get_edges():
                    if(node in edge):
                        self.remove_edges(edge)

    
    
    def remove_edges(self, edges):
        # If only one edge is provided, we turn it into a list
        if not isinstance(edges, list):
            edges = [edges]
        
        for edge in edges:
            u, v = edge

            if edge not in self.get_edges():
                raise KeyError('Edge {} is not in the graph'.format((u, v)))
            
            for node, weight in self.get_adjacency_list(u):
                if node == v:
                    self._G[u].remove((node, weight))
            
            # Removing both (u, v) and (v, u) if not directed
            if not self._directed:
                for node, weight in self.get_adjacency_list(v):
                    if node == u:
                        self._G[v].remove((node, weight))

    def breadth_first_search(self, goal, start=None, get_path=True):
        if len(self.get_nodes()) == 0:
            raise KeyError('Graph has no nodes')

        if len(self.get_edges()) == 0:
            raise KeyError('Graph has no edges')

        if start == None:
            start=self.get_nodes()[0][0]

        visited = []
        queue = []

        queue.append(start)

        while len(queue) > 0:
            node = queue.pop(0)

            visited.append(node)

            if node == goal:
                if get_path:
                    return (True, visited)
                return True

            for neighbor in self.get_adjacency_list(node):
                if neighbor[0] not in visited and neighbor[0] not in queue:
                    queue.append(neighbor[0])

        if get_path:
            return (False, [])
        return False

    def depth_first_search(self, goal, start=None, get_path=True):
        if len(self.get_nodes()) == 0:
            raise KeyError('Graph has no nodes')

        if len(self.get_edges()) == 0:
            raise KeyError('Graph has no edges')

        if start == None:
            start=self.get_nodes()[0][0]

        stack = []
        stack.append(start)
        visited = []

        while len(stack) > 0:
            node = stack.pop()

            visited.append(node)

            if node == goal:
                if get_path:
                    return (True, visited)
                return True

            for neighbor in self.get_adjacency_list(node):
                if neighbor[0] not in visited and neighbor[0] not in stack:
                    stack.append(neighbor[0])

        if get_path:
            return (False, [])
        return False

    def uniform_cost_search(self, goal, start=None):
        if len(self.get_nodes()) == 0:
            raise KeyError('Graph has no nodes')

        if len(self.get_edges()) == 0:
            raise KeyError('Graph has no edges')

        if start == None:
            start=self.get_nodes()[0][0]

        queue = []
        visited = {}
        queue.append([0, start])

        while (len(queue) > 0):

            queue = sorted(queue)
            node = queue[0]
            del queue[0]
            if (node[1] == goal):
                answer = node[0]
                return (True, answer)
            if (node[1] not in visited):
                for new_node in self.get_adjacency_list(node[1]):
                    queue.append([(node[0] + int(new_node[1])), new_node[0]])
            visited[node[1]] = 1

        return (False, [])
