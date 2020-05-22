# import modules here
import math
################# Question 0 #################


def add(a, b):  # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x):  # do not change the heading of the function
    if x < 0:
        return -1
    elif x < 2:
        return x
    else:
        left = 0
        right = x
        while right != 1 + left:
            mid = (left + right) / 2.0
            flag = mid * mid
            if flag > x:
                right = math.ceil(mid)
            elif flag < x:
                left = math.floor(mid)
            else:
                return int(mid)
        return left


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them


def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    x_new = x_0
    for i in range(MAX_ITER):
        x = x_new
        x_new = x - f(x) / fprime(x)
        if abs(x - x_new) < EPSILON:
            break
    return x_new


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)


def make_tree(tokens):  # do not change the heading of the function
    tree = Tree(tokens[0])
    child = tree
    parent = Tree(tokens[0])
    root = []
    for i in range(1, len(tokens)):
        if tokens[i] == '[':
            root.append(parent)
            parent = child
            i += 1
        elif tokens[i] == ']':
            i += 1
            parent = root.pop()
            continue
        else:
            child = Tree(tokens[i])
            parent.add_child(child)
    return tree


def max_depth(root):  # do not change the heading of the function
    if root == None:
        return 0
    elif root.children == None:
        return 1
    else:
        branch_depth = set()
        branch_depth.add(1)
        for i in root.children:
            branch_depth.add(max_depth(i) + 1)
        overall_depth = max(branch_depth)
        return overall_depth
