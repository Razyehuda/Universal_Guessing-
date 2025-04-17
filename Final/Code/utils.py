import numpy as np
from tree import *

def list_to_str(y):
    y_str = ""
    for i in y:
       y_str += str(i)

    return y_str

def check_if_iid(x):
    check = 0
    for i in x:
        check += int(i)
    check = check/100

def binary_to_float(binary_fraction):
    decimal_fraction = 0.0
    power = -1
    binary_fraction = binary_fraction[2:]
    for bit in binary_fraction:
        decimal_fraction += int(bit) * 2 ** power
        power -= 1

    return decimal_fraction


def float_to_binary(num):
    if num == 0:
        return '0'

    integer_part = int(num)
    fractional_part = num - integer_part

    # Convert the integer part to binary
    binary_integer = bin(integer_part)[2:]

    # Convert the fractional part to binary
    binary_fractional = ''
    while fractional_part > 0:
        fractional_part *= 2
        bit = int(fractional_part)
        binary_fractional += str(bit)
        fractional_part -= bit

    binary_result = binary_integer + ('.' + binary_fractional if binary_fractional else '')
    return binary_result


def bitwise_xor(str1,str2):

    result = ''.join(str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(str1, str2))

    return result

def generate_iid_sequence(length, p = 1/2):
    return list_to_str(np.random.choice([0, 1], size = length, p = [ 1- p,p]).tolist())

def generate_markov1(length, transitionMatrix, stat_p = 0.5):
    # Define the state names
    states = [0, 1]
    
    # Choose the starting two states
    x_n_minus_1 = np.random.choice(states, p = [stat_p, 1 - stat_p])
    seq = [x_n_minus_1]
    
    for _ in range(length - 1):  # -1 because we already have 1 state
        state_index = x_n_minus_1  
        x_n = np.random.choice(states, p=transitionMatrix[state_index])
        
        seq.append(x_n)
        
        # Update states
        x_n_minus_1 = x_n
    
    return list_to_str(seq)

def generate_markov2(length, transitionMatrix, stat_p = 0.5):
    # Define the state names
    states = [0, 1]
    
    # Choose the starting two states
    x_n_minus_2 = np.random.choice(states, p = [stat_p, 1 - stat_p])
    x_n_minus_1 = np.random.choice(states, p = [stat_p, 1 - stat_p])
    seq = [x_n_minus_2, x_n_minus_1]
    # For checking
    seq = [1,0] ###
    for _ in range(length - 2):  # -2 because we already have 2 states
        state_index = x_n_minus_2 * 2 + x_n_minus_1  # Convert binary state to index (00->0, 01->1, 10->2, 11->3)
        x_n = np.random.choice(states, p=transitionMatrix[state_index])
        
        seq.append(x_n)
        
        # Update states
        x_n_minus_2, x_n_minus_1 = x_n_minus_1, x_n
    
    return list_to_str(seq)

def list_to_str(seq):
    return ''.join(map(str, seq))

def find_current_I(j, I_bits, previous_I, alpha_value = 2):
    treeRoot = build_tree(j, alpha_value)
    currentNode = treeRoot
    index = 0
    while currentNode.left != None and currentNode.right != None:
        try:
            if I_bits[index] == "0":
                currentNode = currentNode.left
            if I_bits[index] == "1":
                currentNode = currentNode.right
            index +=1
        except:
            return (None, None)
        
    I = int(currentNode.label)
    new_I_bits = I_bits[index:]
    if previous_I:
        if I in previous_I:
            return (None, new_I_bits)
        
    return(I,new_I_bits)

def find_current_I2(j, I_bits, previous_I, alpha_value = 2):
    treeRoot = build_tree(j, alpha_value)
    currentNode = treeRoot
    index = 0
    while currentNode.left != None and currentNode.right != None:
        try:
            if I_bits[index] == "0":
                currentNode = currentNode.left
            if I_bits[index] == "1":
                currentNode = currentNode.right
            index +=1
        except:
            return (None, None)
        
    I = int(currentNode.label)
    new_I_bits = I_bits[index:]
        
    return(I,new_I_bits)

def generate_log_range(start, end, num_dots):
    
    log_start = np.log10(start)
    log_end = np.log10(end)

    log_space = np.linspace(log_start, log_end, num_dots)
    n_values = np.power(10, log_space)
    return n_values

