from Node import Node
import Tree
import test_gen

class Tree_Generator:
    # n_ary is the number of children each node can have, 
    # m_ary is the depth of the tree
    def __init__(self, n_ary: int, m_ary: int):
        self.n_ary = n_ary
        self.m_ary = m_ary
        self.tree_database = set()
    
    
    
    def generate_tree(self, size = None):
        size = size if size is not None else self.n_ary ** self.m_ary        
        # find combinations of values that add up to size
        
        possible_trees,_ = test_gen.redistribution_based(size)
        return possible_trees

        # make branches from said combinations
    
    def generate_all_trees(self, size = None):
        if size is None:
            print("Size not provided, using default max size based on n_ary and m_ary")
            return
        all_unique_trees_code = test_gen.redistribution_based(size)
        
        all_trees = []
        for tree_code in all_unique_trees_code:
            tree = self.build_tree_from_code(tree_code)
            all_trees.append(tree)
        return all_trees
    
    
    def build_tree_from_code(self, tree_code):
        tree = Tree(self.n_ary, self.m_ary)
        
        # for value in tree_code:
        #     temp = Node(value)
        #     for i in range(value - 1):
        #         temp.add_node(i)
        
    
generator = Tree_Generator(5, 5)
# for n in (5, 7):
    # print(f"Unique canonical partitions for N={n}:", generator.generate_tree(n))
arr = generator.generate_tree(5)
arr.sort(reverse=True)
for a in arr:
    print(a)

    