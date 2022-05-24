import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import src.graphex as gx


class TestGraphex(unittest.TestCase):
    def setUp(self):
        self.G = gx.Graph()

    def test_graph_initialized_with_no_nodes(self):
        nodes = self.G.get_nodes()
        self.assertEqual(len(nodes), 0)

    def test_graph_initialized_with_no_edges(self):
        edges = self.G.get_edges()
        self.assertEqual(len(edges), 0)
    
    def test_adding_one_node(self):
        self.G.add_nodes(10)
        nodes = self.G.get_nodes()

        self.assertEqual(len(nodes), 1)
        self.assertIn(10, nodes)
    
    def test_adding_multiple_nodes(self):
        self.G.add_nodes([10, 'a', 3.14])
        nodes = self.G.get_nodes()

        self.assertEqual(len(nodes), 3)
        self.assertIn('a', nodes)
    
    def test_new_node_has_no_neighbors(self):
        self.G.add_nodes(10)
        adj_list = self.G.get_adjacency_list(10)

        self.assertEqual(len(adj_list), 0)
    
    def test_get_adjacency_list_from_inexistent_node(self):
        with self.assertRaises(KeyError) as context:
            _ = self.G.get_adjacency_list(10)

        self.assertTrue('not a node' in str(context.exception))
    
    def test_adding_one_edge_to_undirected_graph(self):
        self.G.add_edges((10, 20))
        edges = self.G.get_edges()

        self.assertIn((10, 20), edges)
        self.assertIn((20, 10), edges)
    
    def test_adding_one_edge_to_directed_graph(self):
        G = gx.Graph(directed=True)
        G.add_edges((10, 20))
        edges = G.get_edges()

        self.assertIn((10, 20), edges)
        self.assertNotIn((20, 10), edges)

    def test_adding_multiple_edges(self):
        self.G.add_edges([(10, 20), (20, 30)])
        edges = self.G.get_edges()

        self.assertIn((10, 20), edges)
        self.assertIn((20, 30), edges)
    
    def test_adding_an_edge_creates_nodes(self):
        self.G.add_edges((10, 20))
        nodes = self.G.get_nodes()

        self.assertIn(10, nodes)
        self.assertIn(20, nodes)
    
    def test_edge_has_weight_one_if_unweighted_graph(self):
        pass


if __name__ == '__main__':
    unittest.main()
