import unittest
from Node import Node
from Tree import Tree


# Node tests
class TestNode(unittest.TestCase):
    def test_Node_creation(self):
        node = Node(5)
        self.assertEqual(node.value, 5)
        self.assertEqual(len(node.next), 0)

    def test_Node_add_next(self):
        node = Node(5)
        next_node = Node(10)
        node.add_next(next_node)
        self.assertIn(next_node, node.next)

        nodes_to_append = [Node(i) for i in range(3, 8)]
        for i in range(3, 8):
            node.add_next(nodes_to_append[i - 3])
        for i in range(3, 8):
            self.assertIn(nodes_to_append[i - 3], node.next)
        
    def test_Node_length(self):
        node = Node(5)
        self.assertEqual(len(node), 0)
        node.add_next(Node(10))
        self.assertEqual(len(node), 1)

    def test_Node_sort(self):
        node = Node(5)
        
        nodes = [Node(10), Node(3), Node(8)]
        for n in nodes:
            node.add_next(n)
        node.sort()
        self.assertEqual([n.value for n in node.next], [3, 8, 10])


class TestTree(unittest.TestCase):
    def test_Tree_creation(self):
        tree = Tree(3, 2)
        self.assertEqual(tree.n_ary, 3)
        self.assertEqual(tree.m_ary, 2)
        self.assertEqual(tree.root, None)

    def test_Tree_add_node(self):
        tree = Tree(3, 2)
        self.assertTrue(tree.add_node(10, 5))
    
    def test_Tree_find_node(self):
        tree = Tree(3, 3)
        tree.add_node(10, 2)
        tree.add_node(3, 5)
        tree.add_node(8, 10)
        node, depth = tree.find_node(8)
        
        # print(node, depth)
        self.assertEqual(node.value, 8)
        self.assertEqual(depth, 3)
        
    def test_Tree_add_node_constraints(self):
        tree = Tree(2, 2)
        tree.add_node(10, 5)  # root
        tree.add_node(3, 5)   # child of root
        tree.add_node(8, 5)   # child of root
        self.assertFalse(tree.add_node(15, 5))  # exceeds n_ary
        self.assertFalse(tree.add_node(20, 3))  # exceeds m_ary

    def test_Tree_display(self):
        tree = Tree(3, 2)
        tree.add_node(10, 5)
        tree.add_node(3, 5)
        tree.add_node(8, 10)
        # This test just ensures the display method doesn't raise an error
        tree.display()
        
    def test_duplicate_values(self):
        tree = Tree(2, 2)
        tree.add_node(10, 5)  # root
        self.assertFalse(tree.add_node(10, 5))  # duplicate value

    def test_Tree_equality(self):
        t = Tree(3, 3)
        t.add_node(10, 2)
        t.add_node(3, 2)
        t.add_node(8, 10)

        t2 = Tree(3, 3)
        t2.add_node(10, 2)
        t2.add_node(3, 2)
        t2.add_node(8, 10)
        
        t3 = Tree(3, 3)
        t3.add_node(2, 1)
        t3.add_node(10, 1)
        t3.add_node(3, 2)
        
        t4 = Tree(4, 4)
        t4.add_node(10, 2)
        t4.add_node(3, 2)
        t4.add_node(8, 10)
        t4.add_node(9, 8)
        
        self.assertEqual(t, t2)
        self.assertEqual(t, t3)
        self.assertNotEqual(t, t4)

if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass