import math

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def build_full_binary_tree(j, alpha=2):
    height = math.ceil(math.log2(j * alpha))

    def add_nodes(node, current_height):
        if current_height < height:
            node.left = TreeNode(None)  # Initialize with None
            add_nodes(node.left, current_height + 1)
            node.right = TreeNode(None)  # Initialize with None
            add_nodes(node.right, current_height + 1)

    if height >= 0:
        root = TreeNode(None)  # Initialize with None
        add_nodes(root, 0)
        return root
    else:
        return None
    
    
def print_tree(root):
    def inorder_traversal(node, depth=0):
        if node:
            inorder_traversal(node.right, depth + 1)
            print("   " * depth + " --> " + str(node.data))
            inorder_traversal(node.left, depth + 1)

    inorder_traversal(root)

def reverse_rightmost_nodes(node, node_remaining):
    if node and node_remaining[0] > 0:
        reverse_rightmost_nodes(node.left, node_remaining)
        reverse_rightmost_nodes(node.right, node_remaining)
        
        if node_remaining[0] > 0 and node.left is None and node.right is None:
            node.right = TreeNode(str(node.data) + "1")
            node.left = TreeNode(str(node.data) + "0")
            node_remaining[0] -= 1

"""
def print_inorder_tree(root):
    def inorder_traversal(node):
        if node:
            inorder_traversal(node.left)
            print(node.data, end=" ")
            inorder_traversal(node.right)

    inorder_traversal(root)
    print()

"""
def label_leaves(node, label):
    if node:
        label = label_leaves(node.left, label)
        if node.left is None and node.right is None:
            node.data = str(label)
            label += 1
        label = label_leaves(node.right, label)
    return label

def build_tree(j_value, alpha_value):
    if j_value == 1:
        tree_root = TreeNode('')
        tree_root.right = TreeNode('1')
        tree_root.left = TreeNode('0')
    else:
        height = math.ceil(math.log2(j_value * alpha_value - 1)) - 1
        x_value = [alpha_value*j_value - 2**(height)]
        tree_root = build_full_binary_tree(j_value, alpha_value)
    #print_tree(tree_root)
        reverse_rightmost_nodes(tree_root, x_value)
    label_leaves(tree_root,0)
    return tree_root
    #print_tree(tree_root)