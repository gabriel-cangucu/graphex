import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import src.graphex as gx

class TestGraphex(unittest.TestCase):
    def setUp(self):
        self.G = gx.Graph()

    def test_graph_initialized_with_no_nodes(self):
        self.assertEqual(len(self.G.get_nodes()), 0)

    def test_graph_initialized_with_no_edges(self):
        self.assertEqual(len(self.G.get_edges()), 0)

if __name__ == '__main__':
    unittest.main()
