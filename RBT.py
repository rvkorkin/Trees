import numpy as np

class Node():
    def __init__(self, _data):
        self.data = _data
        self.parent = None
        self.left = None
        self.right = None
        self.color = 'red'

class BRT():
    def __init__(self):
        self.nil = Node(None)
        self.nil.color = 'black'
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

    def insert(self, _data):
        if self.search(_data):
            return
        z = Node(_data)
        z.parent = None
        z.data = _data
        z.left = self.nil
        z.right = self.nil
        z.color = 'red'

        y = None
        x = self.root
        
        while x != self.nil:
            y = x
            if z.data < x.data:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == None:
            self.root = z
        elif z.data < y.data:
            y.left = z
        else:
            y.right = z
        
        if z.parent == None:
            z.color = 'black'
            return
        
        if z.parent.parent == None:
            #z.parent.parent.color = 'black'
            return

        self.insert_balance(z)
    
    def insert_balance(self, z):
        while z.parent.color == 'red':
            if z.parent == z.parent.parent.right:
                u = z.parent.parent.left
                if u.color == 'red':
                    u.color = 'black'
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
            else:
                u = z.parent.parent.right
                if u.color == 'red':
                    u.color = 'black'
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            if z == self.root:
                break
        self.root.color = 'black'
        
    def right_balance(self, z):
        while z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                elif z == z.parent.right:
                    z = z.parent
                    self.left_rotate(z)
                z.parent.color = 'black'
                z.parent.parent.color = 'red'
                self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                elif z == z.parent.left:
                    z = z.parent
                    self.right_rotate(z)
                z.parent.color = 'black'
                z.parent.parent.color = 'red'
                self.left_rotate(z.parent.parent)
        self.root.color = 'black'

    def left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        
    def trans(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def search(self, value):
        return self.search_node(self.root, value)
        
    def search_node(self, node, value):
        if node == self.nil:
            return False
        if value == node.data:
            return True
        if value < node.data:
            return self.search_node(node.left, value)
        return self.search_node(node.right, value)
        
    def remove(self, value):
        if not self.search(value):
            return
        self.delete_node(self.root, value)
        
    def delete_node(self, node, value):
        z = self.nil
        while node != self.nil:
            if node.data == value:
                z = node
            if node.data < value:
                node = node.right
            else:
                node = node.left
        if z == self.nil:
            return
        y = z
        last_color = y.color
        if z.left == self.nil:
            x = z.right
            self.trans(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.trans(z, z.left)
        else:
            y = self.tree_min(z.right)
            last_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.trans(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.trans(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if last_color == 'black':
            self.delete_balance(x)

    def delete_balance(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'

    def print_tree(self):
        self.__print_helper(self.root)
        
    def __print_helper(self, node):
        if node != self.nil:
            print(node.data)
            self.__print_helper(node.left)
            self.__print_helper(node.right)


    def tree_min(self, z):
        while z.left != self.nil:
            z = z.left
        return z       
    
if __name__ == "__main__":
    import numpy as np
    brt = BRT()
    for i in range(1, 10):
        brt.insert(i)
    
    for _ in range(5):
        el = np.random.randint(1, 10, 1)[0]
        brt.remove(el)