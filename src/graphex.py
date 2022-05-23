from collections import defaultdict
from email.policy import default


class Graph():
    def __init__(self, weighted=False) -> None:
        self._G = dict()
        self._weighted = weighted
    
    def get_nodes(self) -> list:
        return self._G.keys()
    
    def get_edges(self) -> list:
        edges = []

        for node in self.get_nodes():
            edges.extend(self._G[node])
        
        # Removing duplicates by turning the list into a set
        return list(set(edges))
