import unittest

from .uniform import Node, Uniform


class TestNode(unittest.TestCase):
    def setUp(self):
        self.node_A = Node('A', 5)
        self.node_B = Node('B')

        self.another_node_A = Node('A', 10)

    def test_node_should_equal_when_label_is_the_same_even_different_cost(self):
        self.assertEqual(self.node_A, self.another_node_A)

    def test_node_should_not_equal_when_label_is_different(self):
        self.assertNotEqual(self.node_A, self.node_B)


class TestUniform(unittest.TestCase):
    def setUp(self):
        self.uniform = Uniform('./src/routes.csv', 'A', 'B')

    ####
    # load_graph
    ####
    def test_load_graph_should_return_data_structure_like_expected(self):
        expected = {
            'A': [{'label': 'B', 'cost': 5}, {'label': 'D', 'cost': 15}],
            'B': [{'label': 'A', 'cost': 5}, {'label': 'C', 'cost': 5}],
            'C': [{'label': 'B', 'cost': 5}, {'label': 'D', 'cost': 7}],
            'D': [{'label': 'C', 'cost': 7}, {'label': 'A', 'cost': 15}],
            'E': [{'label': 'F', 'cost': 5}],
            'F': [{'label': 'E', 'cost': 5}, {'label': 'G', 'cost': 5}],
            'G': [{'label': 'F', 'cost': 5}, {'label': 'H', 'cost': 10}, {'label': 'J', 'cost': 20}],
            'H': [{'label': 'G', 'cost': 10}, {'label': 'I', 'cost': 10}],
            'I': [{'label': 'H', 'cost': 10}, {'label': 'J', 'cost': 5}],
            'J': [{'label': 'I', 'cost': 5}, {'label': 'G', 'cost': 20}]}
        self.assertDictEqual(self.uniform.graph, expected)

    ####
    # valid_to_expand
    ####
    def test_valid_to_expand_should_return_true_when_node_not_in_expanded_list(self):
        node_A = Node('A')
        node_B = Node('B')
        self.uniform.expanded_list.append(node_B)

        self.assertTrue(self.uniform.valid_to_expand(node_A))

    def test_valid_to_expand_should_return_false_when_node_in_expanded_list(self):
        node_B = Node('B')
        self.uniform.expanded_list.append(node_B)

        self.assertFalse(self.uniform.valid_to_expand(node_B))

    ####
    # find_path
    ####
    def test_find_path_should_find_back_with_there_parent(self):
        node_A = Node('A')
        node_B = Node('B', parent=node_A)
        node_C = Node('C', parent=node_B)

        actual = self.uniform.find_path(node_C)
        expected = [node_A, node_B, node_C]
        self.assertEqual(actual, expected)

    def test_run_have_path_between_node_should_return_path_and_last_node_should_have_correct_cost(self):
        # A -> B
        actual = self.uniform.run()
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].label, 'A')
        self.assertEqual(actual[0].cost, 0)
        self.assertEqual(actual[1].label, 'B')
        self.assertEqual(actual[1].cost, 5)

        # A -> C
        actual = Uniform('./src/routes.csv', 'A', 'C').run()
        self.assertEqual(len(actual), 3)
        self.assertEqual(actual[0].label, 'A')
        self.assertEqual(actual[0].cost, 0)
        self.assertEqual(actual[1].label, 'B')
        self.assertEqual(actual[1].cost, 5)
        self.assertEqual(actual[2].label, 'C')
        self.assertEqual(actual[2].cost, 10)

        # E -> J
        actual = Uniform('./src/routes.csv', 'E', 'J').run()
        self.assertEqual(len(actual), 4)
        self.assertEqual(actual[0].label, 'E')
        self.assertEqual(actual[0].cost, 0)
        self.assertEqual(actual[1].label, 'F')
        self.assertEqual(actual[1].cost, 5)
        self.assertEqual(actual[2].label, 'G')
        self.assertEqual(actual[2].cost, 10)
        self.assertEqual(actual[3].label, 'J')
        self.assertEqual(actual[3].cost, 30)

        # A -> D
        actual = Uniform('./src/routes.csv', 'A', 'D').run()
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].label, 'A')
        self.assertEqual(actual[0].cost, 0)
        self.assertEqual(actual[1].label, 'D')
        self.assertEqual(actual[1].cost, 15)

    def test_run_have_no_path_should_return_none(self):
        # A -> C
        actual = Uniform('./src/routes.csv', 'A', 'J').run()
        self.assertEqual(actual, None)


if __name__ == '__main__':
    unittest.main()
