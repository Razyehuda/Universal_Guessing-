import math
class TreeNode:
    def __init__(self, path, label):
        self.path = path  # Path from root to node (e.g., "001")
        self.label = label  # I (index), None if not a leaf
        self.left = None
        self.right = None

def build_full_binary_tree(j, alpha=2):
    height = math.ceil(math.log2(j * alpha - 1)) - 1

    def add_nodes(node, current_height, current_path):
        if current_height < height:
            node.left = TreeNode(current_path + "0", None)  # Initialize label with None
            add_nodes(node.left, current_height + 1, node.left.path)
            node.right = TreeNode(current_path + "1", None)  # Initialize label with None
            add_nodes(node.right, current_height + 1, node.right.path)

    if height >= 0:
        root = TreeNode("", None)  # Initialize with empty path and None label
        add_nodes(root, 0, root.path)
        return root
    else:
        return None

def print_tree(root):
    def inorder_traversal(node, depth=0):
        if node:
            inorder_traversal(node.right, depth + 1)
            if node.label is None:
                print("   " * depth + f" --> {node.path}")
            else:
                print("   " * depth + f" --> {node.path}, {node.label}")
            inorder_traversal(node.left, depth + 1)

    inorder_traversal(root)

def reverse_rightmost_nodes(node, node_remaining):
    if node and node_remaining[0] > 0:
        reverse_rightmost_nodes(node.left, node_remaining)
        reverse_rightmost_nodes(node.right, node_remaining)
        
        if node_remaining[0] > 0 and node.left is None and node.right is None:
            node.right = TreeNode(node.path + "1", str(node.label) + "1")
            node.left = TreeNode(node.path + "0", str(node.label) + "0")
            node_remaining[0] -= 1

def find_path(root, target_index):

    if root:
        if root.label == target_index:
            return root.path
        left_result = find_path(root.left, target_index)
        right_result = find_path(root.right, target_index)

        if left_result is not None:
            return left_result
        elif right_result is not None:
            return right_result        



def label_leaves(node, label):
    if node:
        label = label_leaves(node.left, label)
        if node.left is None and node.right is None:
            node.label = str(label)
            label += 1
        label = label_leaves(node.right, label)
    return label

def build_tree(j_value, alpha_value = 2):
    if j_value == 1:
        tree_root = TreeNode('', '0')
        tree_root.right = TreeNode('1','1')
        tree_root.left = TreeNode('0','0')
    else:
        height = math.ceil(math.log2(j_value * alpha_value - 1)) - 1
        x_value = [alpha_value*j_value - 2**(height)]
        tree_root = build_full_binary_tree(j_value, alpha_value)
        reverse_rightmost_nodes(tree_root, x_value)
    label_leaves(tree_root,0)
    # print_tree(tree_root)
    # print("\n")
    return tree_root
