class BinaryTree:
    def __init__(self, data, parent):
        if self == None:
            return
        self.data = data
        self.left = None
        self.right = None
        self.parent = parent
        self.root = None
        self.height = 0

    def insertLeft(self, data):
        if self.left == None:
            self.left = BinaryTree(data, self)
        else:
            new_node = BinaryTree(data, self.parent)
            new_node.left = self.left
            self.left = new_node

    def insertRight(self, data):
        if self.right == None:
            self.right = BinaryTree(data, self)
        else:
            new_node = BinaryTree(data, self.parent)
            new_node.right = self.right
            self.right = new_node

    def getBalance(node):
        if node.right:
            h_r = node.right.height
        else:
            h_r = 0
        if node.left:
            h_l = node.left.height
        else:
            h_l = 0
        node.height = max(h_r, h_l) + 1
        return h_r - h_l

    def rebalance(self, node):
        if node.getBalance() > 1:
            if node.right.getBalance() == -1:
                self.small_right(node.right)
                self.small_left(node)
            else:
                self.small_left(node) 
        elif node.getBalance() < -1:
            if node.left.getBalance() == 1:
                self.small_left(node.left)
                self.small_right(node)
            else:
                self.small_right(node)

    def check(self, key):
        node = self.root
        while True:
            if key > node.data:
                if node.right != None:
                    node = node.right
                else:
                    return False
            elif key < node.data:
                if node.left != None:
                    node = node.left
                else:
                    return False
            else:
                return True
        return False

    def insert(self, key):
        if self.root == None:
            self.data = key
            self.root = self
            self.height = 1
            return
        node = self.root
        while True:
            if key > node.data:
                if node.right == None:
                    node.insertRight(key)
                    node.right.height = 1
                    break 
                else:
                    node = node.right
            elif key < node.data:
                if node.left == None:
                    node.insertLeft(key)
                    node.left.height = 1
                    break
                else:
                    node = node.left
        if node != None:
            my_node = node
        else:
            self = self.root
            return
        while my_node != None:
            self.rebalance(my_node)
            my_node = my_node.parent
        self = self.root

    def remove(self, key):
        node = self.root
        if node.data == None:
            return
        if node.check(key) == False:
            return
        while node != None:
            if key > node.data:
                node = node.right
            elif key < node.data:
                node = node.left
            else:
                if node.left == None and node.right == None:
                    if node.parent == None:
                        node.data = None
                        node = None
                        return
                    else:
                        if node.parent.left == node:
                            my_node = node.parent
                            node.parent.left = None
                        elif node.parent.right == node:
                            my_node = node.parent
                            node.parent.right = None
                    node = None
                    break
                elif node.left == None:
                    node.data = node.right.data
                    my_node = node
                    node.right = None
                    node.height = 1
                    break
                else:
                    node_repl = node.replacement(node)
                    if node_repl != None:
                        node.data = node_repl.data
                        node.left.remove_node(node_repl)
                        node_repl = None
                        my_node = node
                    break
        while my_node != None:
            self.rebalance(my_node)
            my_node = my_node.parent
        return

    def remove_node(self, key_node):
        node = key_node
        if node.left == None and node.right == None:
            if node.parent != None and node.parent.left == node:
                node.parent.left = None
            elif node.parent != None and node.parent.right == node:
                node.parent.right = None
            node.parent.height = 1
            node = None
            return
        elif node.left == None:
            node.data = node.right.data
            node.right = None
            node.height = 1
            return
        else:
            node_repl = node.replacement(node)
            if node_repl != None:
                node.data = node_repl.data
                node.left.remove_node(node_repl)
            return
    
    def replacement(self, node):
        node = node.left
        if node != None:
            while node.right != None:
                node = node.right
        return node

    def tree2set(self):
        q = []
        node = self
        q.append(node)
        height = 0
        shift = 0
        while len(q) > shift:
            height += 1
            for nodeCount in reversed(range(len(q)-shift)):
                node = q[shift]
                shift += 1
                if node.left != None: 
                    q.append(node.left)
                if node.right != None: 
                    q.append(node.right)
        return set([el.data for el in q])
    
    def small_left(self, node):
        child = node.right
        node.right = child.left
        if child.left != None:
            h_child = child.left.height
            child.left.parent = node
        else:
            h_child = 0
        if node.left:
            n_height = node.left.height
        else:
            n_height = 0
        node.height = max(h_child, n_height) + 1
        child.parent = node.parent
        if node.parent == None:
            node.parent, node.parent.root = child, child
            node.root = node.parent.root
        else:
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child
        child.left = node
        node.parent = child
        if child.parent == None:
            self.root = child

    def small_right(self, node): 
        child = node.left
        node.left = child.right
        if child.right != None:
            h_child = child.right.height
            child.right.parent = node
        else:
            h_child = 0
        if node.right:
            n_height = node.right.height
        else:
            n_height = 0
        node.height = max(h_child, n_height) + 1
        child.parent = node.parent
        if node.parent == None:
            node.parent, node.parent.root = child, child
            node.root = node.parent.root
        else:
            if node.parent.right == node:
                node.parent.right = child
            else:
                node.parent.left = child
        child.right = node
        node.parent = child
        if child.parent == None:
            self.root = child

if __name__ == "__main__":
    import numpy as np
    AVL = BinaryTree(None, None)
    for i in range(1, 10):
        AVL.insert(i)
    AVL = AVL.root
    
    for _ in range(100):
        el = np.random.randint(1, 10, 1)[0]
        print(el)
        AVL.remove(el)
