from Node import Node
from collections import deque

class Tree:
    
    # n_ary is the maximum number of children a node can have
    # m_ary is the maximum depth of the tree
    def __init__(self, n_ary: int, m_ary: int):
        self.n_ary = n_ary
        self.m_ary = m_ary
        self.root = None
    
    
    # returns True if the node was added successfully, False otherwise
    def add_node(self, value, parent_value = None, allow_duplicates=False):
        # empty tree
        if self.root == None:
            if parent_value and value:
                self.root = Node(parent_value)
                self.root.add_next(Node(value))
                return True
            self.root = Node(value)
            return True
        
        # add to root if parent_value is None
        # do not allow duplicate values
        if not allow_duplicates:
            found, _ = self.find_node(value)
            if found is not None:
                return False

        # add as child of root when parent_value is None
        if parent_value is None:
            # check root children limit
            if len(self.root) >= self.n_ary:
                return False
            self.root.add_next(Node(value))
            return True

        # find parent
        parent_node, depth = self.find_node(parent_value)
        if parent_node is None:
            return False

        # depth is 1-based; disallow adding if would exceed max depth
        if depth >= self.m_ary:
            return False

        # check parent children limit (n_ary)
        if len(parent_node) >= self.n_ary:
            return False

        parent_node.add_next(Node(value))
        return True
    
    # returns the node with the given value and its depth, or (None, None) if not found
    # approach: depth-first search
    def find_node(self, value):
        def search_node(value, node=self.root, depth=1):
            if node.value == value:
                return node, depth
            for next_node in node.next:
                found_node, found_depth = search_node(value, next_node, depth + 1)
                if found_node == None and found_depth == None:
                    continue
                return found_node, found_depth
            return None, None
        return search_node(value)
    
    
    def __len__(self):
        def count_nodes(node):
            count = 1
            for next_node in node.next:
                count += count_nodes(next_node)
            return count
        if self.root == None:
            return 0
        return count_nodes(self.root)
    
    def balance(self):
        # TODO: implement tree balancing algorithm (e.g., AVL or Red-Black Tree)
        pass
        
        
    
    # displays the tree in a readable format
    def display(self):
        def display_node(node, prefix="", is_last=True):
            connector = "└── " if is_last else "├── "
            print(prefix + connector + str(node.value))
            prefix += "    " if is_last else "│   "
            for i, child in enumerate(node.next):
                display_node(child, prefix, i == len(node.next) - 1)

        if not self.root:
            return

        # print root and its children (do not duplicate child nodes at top-level)
        print(str(self.root.value))
        for i, child in enumerate(self.root.next):
            display_node(child, "", i == len(self.root.next) - 1)
    
    # checks if two trees are similar, check for the same structure regardless of node values
    def similar_tree(self, other):
        if not isinstance(other, Tree):
            return False
        
        def compare_nodes(node1, node2):
            if len(node1.next) != len(node2.next):
                return False
            node1.next.sort(key=lambda x: len(x))
            node2.next.sort(key=lambda x: len(x))
            for child1, child2 in zip(node1.next, node2.next):
                if not compare_nodes(child1, child2):
                    return False
            return True

        return compare_nodes(self.root, other.root)      
    
    def __str__(self):
        def display_node(node):
            return_string = str(node.value)
            for i, child in enumerate(node.next):
                return_string += display_node(child)
            return return_string
        string = str(self.root.value)
        for i, child in enumerate(self.root.next):
            string += display_node(child)
        return string
    
    def __eq__(self, other):
        if not isinstance(other, Tree):
            return False
        
        def compare_nodes(node1, node2):
            if len(node1.next) != len(node2.next):
                return False
            if node1.value != node2.value:
                return False
            
            node1.next.sort(key=lambda x: len(x))
            node2.next.sort(key=lambda x: len(x))
            for child1, child2 in zip(node1.next, node2.next):
                if not compare_nodes(child1, child2):
                    return False
            return True
        
        return compare_nodes(self.root, other.root)
        
if __name__ == "__main__":
    t = Tree(3, 3)
    t.add_node(10, 2)
    t.add_node(3, 2)
    t.add_node(8, 10)

    t4 = Tree(4, 4)
    t4.add_node(10, 2)
    t4.add_node(3, 2)
    t4.add_node(8, 10)
    t4.add_node(9, 8)


    print(t == t4)

    t.display()
    t4.display()

    print(t)


