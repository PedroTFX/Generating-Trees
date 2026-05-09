class Node:
    def __init__(self, value):
        self.value = value
        self.next = []
        
    def add_next(self, node:int):
        self.next.append(node)
    
    def sort(self):
        self.next.sort(key=lambda n: n.value)
        
    def __str__(self):
        string = f"{self.value}"
        if self.next:
            for n in self.next:
                string += str(n)
        return string
    
    def __len__(self):
        return len(self.next)
        



# n = Node(2)
# n.add_next(1)
# n.add_next(1)
# print(n)
    

    