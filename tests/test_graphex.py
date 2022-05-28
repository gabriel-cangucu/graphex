import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import src.graphex as gx


class TestGraphex(unittest.TestCase):

    def setUp(self):
        self.G = gx.Graph()
        self.weighted_G = gx.Graph(weighted=True)
        self.directed_G = gx.Graph(directed=True)


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
    

    def test_adding_existent_node(self):
        self.G.add_nodes(10)
        self.G.add_nodes(10)
        nodes = self.G.get_nodes()

        self.assertEqual(len(nodes), 1)


    def test_get_adjacency_list_from_inexistent_node(self):
        with self.assertRaises(KeyError) as context:
            _ = self.G.get_adjacency_list(10)

        self.assertTrue('10 is not a node of the graph' in str(context.exception))
    

    def test_adding_one_edge_to_undirected_graph(self):
        self.G.add_edges((10, 20))
        edges = self.G.get_edges()

        self.assertIn((10, 20), edges)
        self.assertIn((20, 10), edges)
    

    def test_adding_one_edge_to_directed_graph(self):
        self.directed_G.add_edges((10, 20))
        edges = self.directed_G.get_edges()

        self.assertIn((10, 20), edges)
        self.assertNotIn((20, 10), edges)
    

    def test_adding_one_weighted_edge(self):
        self.weighted_G.add_edges(('a', 'b', 3))
        edges = self.weighted_G.get_edges()

        self.assertIn(('a', 'b'), edges)


    def test_adding_multiple_edges(self):
        self.G.add_edges([(10, 20), (20, 30)])
        edges = self.G.get_edges()

        self.assertIn((10, 20), edges)
        self.assertIn((20, 30), edges)
    

    def test_edge_must_be_a_tuple_or_list(self):
        with self.assertRaises(TypeError) as context:
            self.G.add_edges('not a tuple')
        
        self.assertTrue('Edges in an unweighted graph must be in the form (u, v)' in str(context.exception))
    

    def test_adding_an_edge_creates_nodes(self):
        self.G.add_edges((10, 20))
        nodes = self.G.get_nodes()

        self.assertIn(10, nodes)
        self.assertIn(20, nodes)
    

    def test_adding_weighted_edges_to_unweighted_graph(self):
        with self.assertRaises(TypeError) as context:
            self.G.add_edges(('a', 'b', 3))
        
        self.assertTrue('Edges in an unweighted graph must be in the form (u, v)' in str(context.exception))
    

    def test_adding_unweighted_edges_to_weighted_graph(self):
        with self.assertRaises(TypeError) as context:
            self.weighted_G.add_edges((10, 20))
        
        self.assertTrue('Edges in a weighted graph must be in the form (u, v, w)' in str(context.exception))
    

    def test_getting_edge_weight(self):
        self.weighted_G.add_edges(('a', 'b', 2.73))
        weight = self.weighted_G.get_weight(('a', 'b'))

        self.assertEqual(weight, 2.73)
    

    def test_edge_has_weight_one_if_unweighted_graph(self):
        self.G.add_edges((10, 20))
        weight = self.G.get_weight((10, 20))

        self.assertEqual(weight, 1)
    

    def test_getting_weight_from_inexistent_edge(self):
        self.weighted_G.add_nodes([10, 20])

        with self.assertRaises(KeyError) as context:
            _ = self.weighted_G.get_weight((10, 20))
        
        self.assertTrue('Edge (10, 20) is not in the graph' in str(context.exception))
    

    def test_adding_existent_edge(self):
        self.directed_G.add_edges((10, 20))
        self.directed_G.add_edges((10, 20))
        edges = self.directed_G.get_edges()

        self.assertEqual(len(edges), 1)


    def test_adding_existent_edge_overrides_previous_weight(self):
        self.weighted_G.add_edges(('a', 'b', 3))
        self.weighted_G.add_edges(('a', 'b', 5))
        weight = self.weighted_G.get_weight(('a', 'b'))

        self.assertEqual(weight, 5)
    

    def test_both_edges_get_updated_if_they_exist_and_undirected(self):
        self.weighted_G.add_edges(('a', 'b', 3))
        self.weighted_G.add_edges(('a', 'b', 5))

        weight_1 = self.weighted_G.get_weight(('a', 'b'))
        weight_2 = self.weighted_G.get_weight(('b', 'a'))

        self.assertEqual(weight_1, 5)
        self.assertEqual(weight_2, 5)
    

    def test_removing_one_node(self):
        self.G.add_nodes(10)
        self.G.remove_nodes(10)
        nodes = self.G.get_nodes()

        self.assertNotIn(10, nodes)


    def test_removing_multiple_nodes(self):
        self.G.add_nodes([10, 20])
        self.G.remove_nodes([10, 20])
        nodes = self.G.get_nodes()

        self.assertNotIn(10, nodes)
        self.assertNotIn(20, nodes)
    

    def test_removing_inexistent_node(self):
        with self.assertRaises(KeyError) as context:
            _ = self.G.remove_nodes(10)
        
        self.assertTrue('10 is not a node of the graph' in str(context.exception))


    def test_removing_one_edge_in_undirected_graph(self):
        self.G.add_edges((10, 20))
        self.G.remove_edges((10, 20))
        edges = self.G.get_edges()

        self.assertNotIn((10, 20), edges)
        self.assertNotIn((20, 10), edges)
    

    def test_removing_one_edge_in_directed_graph(self):
        self.directed_G.add_edges((10, 20))
        self.directed_G.remove_edges((10, 20))
        edges = self.directed_G.get_edges()

        self.assertNotIn((10, 20), edges)

    
    def test_removing_multiple_edges(self):
        self.directed_G.add_edges([(10, 20), (20, 30), (30, 10)])
        self.directed_G.remove_edges([(10, 20), (20, 30)])
        edges = self.directed_G.get_edges()

        self.assertNotIn((10, 20), edges)
        self.assertNotIn((20, 30), edges)


    def test_removing_inexistent_edge(self):
        self.G.add_nodes([10, 20])

        with self.assertRaises(KeyError) as context:
            _ = self.G.remove_edges((10, 20))
        
        self.assertTrue('Edge (10, 20) is not in the graph' in str(context.exception))


    def test_turning_undirected_graph_into_directed(self):
        pass


    def test_turning_directed_graph_into_undirected(self):
        pass

    ## Algoritms tests 
    # BFS

    def test_BFS_with_no_nodes(self):
        with self.assertRaises(KeyError) as context:
            _ = self.G.breadth_first_search(goal="A")
        
        self.assertTrue('Graph has no nodes' in str(context.exception))

    def test_BFS_with_no_edges(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        
        with self.assertRaises(KeyError) as context:
            _ = self.G.breadth_first_search(goal="A")
        
        self.assertTrue('Graph has no edges' in str(context.exception))


    def test_BFS_with_result_in_first_node(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.breadth_first_search(goal="A", get_path=False)

        self.assertTrue(found)

    def test_BFS_with_path(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found, path  = self.G.breadth_first_search(start="D", goal="B")

        self.assertTrue(found)
        self.assertTrue(path == ['D', 'M', 'C', 'L', 'R', 'P', 'T', 'S', 'B'])

    def test_BFS_with_no_path(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.breadth_first_search(start="D", goal="B", get_path=False)

        self.assertTrue(found)

    def test_BFS_with_no_start(self):
        self.G.add_nodes(["D", "A", "T", "L", "M", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.breadth_first_search(goal="B", get_path=False)

        self.assertTrue(found)

    def test_BFS_with_path_and_no_start(self):
        self.G.add_nodes(["D", "A", "T", "L", "M", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found, path  = self.G.breadth_first_search(goal="B")

        self.assertTrue(found)
        self.assertTrue(path == ['D', 'M', 'C', 'L', 'R', 'P', 'T', 'S', 'B'])

    def test_BFS_no_result(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.breadth_first_search(start="D", goal="H", get_path=False)

        self.assertFalse(found)

    def test_BFS_no_result_with_path(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found, path = self.G.breadth_first_search(start="D", goal="H")

        self.assertFalse(found)
        self.assertTrue(path == [])

    # DFS

    def test_DFS_with_no_nodes(self):
        with self.assertRaises(KeyError) as context:
            _ = self.G.depth_first_search(goal="A")
        
        self.assertTrue('Graph has no nodes' in str(context.exception))

    def test_DFS_with_no_edges(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        
        with self.assertRaises(KeyError) as context:
            _ = self.G.depth_first_search(goal="A")
        
        self.assertTrue('Graph has no edges' in str(context.exception))

    def test_DFS_with_result_in_first_node(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.breadth_first_search(goal="A", get_path=False)

        self.assertTrue(found)

    def test_DFS_with_path(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found, path  = self.G.depth_first_search(start="D", goal="B")

        self.assertTrue(found)
        self.assertTrue(path == ['D', 'C', 'P', 'B'])

    def test_DFS_with_no_path(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.depth_first_search(start="D", goal="B", get_path=False)

        self.assertTrue(found)

    def test_DFS_with_no_start(self):
        self.G.add_nodes(["D", "A", "T", "L", "M", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.depth_first_search(goal="B", get_path=False)

        self.assertTrue(found)

    def test_DFS_with_path_and_no_start(self):
        self.G.add_nodes(["D", "A", "T", "L", "M", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found, path  = self.G.depth_first_search(goal="B")

        self.assertTrue(found)
        self.assertTrue(path == ['D', 'C', 'P', 'B'])


    def test_DFS_no_result(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.depth_first_search(start="D", goal="H", get_path=False)

        self.assertFalse(found)

    def test_DFS_no_result_with_path(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found, path = self.G.depth_first_search(start="D", goal="H")

        self.assertFalse(found)
        self.assertTrue(path == [])

     # UCS

    def test_UCS_with_no_nodes(self):
        with self.assertRaises(KeyError) as context:
            _ = self.G.uniform_cost_search(goal="A")
        
        self.assertTrue('Graph has no nodes' in str(context.exception))
     
    def test_UCS_no_edges(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        
        with self.assertRaises(KeyError) as context:
            _ = self.G.uniform_cost_search(goal="A")
        
        self.assertTrue('Graph has no edges' in str(context.exception))
    
    def test_UCS_with_result_in_first_node(self):
        self.G.add_nodes(["A", "T", "L", "M", "D", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.uniform_cost_search(goal="A")

        self.assertTrue(found)
    
    def test_UCS_with_no_start(self):
        self.G.add_nodes(["D", "A", "T", "L", "M", "C", "S", "R", "F", "P", "B", "G"])
        self.G.add_edges([("A", "T"), ("T", "L"), ("M", "L"), ("M", "D"), ("D", "C"), ("C", "R"), ("C", "P"),
                          ("R", "S"), ("A", "S"), ("S", "F"), ("R", "P"), ("P", "B"), ("B", "G"), ("F", "B")])

        found = self.G.uniform_cost_search(goal="B")

        self.assertTrue(found)
        self.assertEqual(found[1], 3)

    def test_UCS_with_weighted_edges(self):
        self.weighted_G.add_nodes(["D", "A", "T", "L", "M", "C", "S", "R", "F", "P", "B", "G"])
        self.weighted_G.add_edges([("A", "T", "118"), ("T", "L", "111"), ("M", "L", "70"), ("M", "D", "75"), ("D", "C", "120"), ("C", "R", "146"), ("C", "P", "138"),
                          ("R", "S", "80"), ("A", "S", "140"), ("S", "F", "99"), ("R", "P", "97"), ("P", "B", "101"), ("B", "G", "90"), ("F", "B", "211")])

        found = self.weighted_G.uniform_cost_search(goal="B")
        self.assertEqual(found[1], (120+138+101))
if __name__ == '__main__':
    unittest.main()
