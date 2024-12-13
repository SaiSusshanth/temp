
class List_node:

    def __init__(self, key, value):
        self.prev = None 
        self.next = None 
        self.val = value
        self.key = key

class Doubly_linked_list:

    def __init__(self, SIZE):
        self.front = None
        self.end = None 
        self.length = 0
        self.SIZE = SIZE 

    def insert(self, Node):

        if self.front == None:
            self.front = Node 
            self.end = Node 
            self.length += 1

        else:

            Node.prev = self.front 
            self.front.next = Node 
            self.front = Node 
            self.length += 1 
        

    def delete(self):
        deleted_Node = self.end
        self.end = self.end.next
        self.length -= 1
        return deleted_Node.key


    def update_linked_list(self, Node):
        next_node = Node.next
        prev_node = Node.prev

        if next_node == None:
            return 
        
        elif prev_node == None:
            self.delete()
            self.insert(Node)

        else:

            prev_node.next = next_node
            next_node.prev = prev_node
            self.length -= 1

            self.insert(Node)
        

# returns (1, val) if key found
# returns (0) if key not found
class Linked_List_cache:
    
    def __init__(self, SIZE):
        self.cache = Doubly_linked_list(SIZE)
        self.SIZE = SIZE 
        self.key_value_map = {}

    def query(self, key):
        return_value = None

        if key in self.key_value_map:
            return_value = [1, self.key_value_map[key].val]

        else: 
            return_value = [0]

        return return_value 

    def insert(self, key, value):

        if self.cache.length == self.cache.SIZE:
            deleted_key = self.cache.delete()
            del self.key_value_map[deleted_key]

        Node = List_node(key, value)

        self.cache.insert(Node)
        self.key_value_map[key] = Node 
        
