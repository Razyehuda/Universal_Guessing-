import numpy as np
import random
from BinaryTree import *
   

def make_I(alpha_value, phrase, c_x):
    phrase_list = list(phrase)
    prev = list_to_str(phrase_list[0 : len(phrase_list) - 1])
    if prev in c_x:
        index = c_x[prev]
        pi = index + 1
    else:
        pi = 0
    Ia = int(phrase_list[len(phrase_list) - 1])

    I = alpha_value * pi + Ia
    return I

def encode(x, alpha_value =2):
    end = False
    start, fin = 0, 1
    n = len(x)
    j = 1
    encoded = []
    c_x = {}
    phrase_num = 0
    while not end:
        phrase_num += 1
        phrase = x[start : fin]
        while phrase in c_x:
            fin += 1
            if fin >= len(x):
                end = True
                break
            phrase = x[start : fin]
        if fin >= n:
            break
        I = make_I(alpha_value, phrase, c_x)
        #binary_encode.append(int_to_min_bits(I,math.ceil(math.log(alpha_value*j -1))))
        encoded.append(I)
        c_x[phrase] = phrase_num
        start = fin
        fin += 1
        j += 1
    #encoded = int_to_min_bits(encoded)

    return encoded 

def find_current_I(j, alpha_value, y, previous_I):
    treeRoot = build_tree(j, alpha_value)
    currentNode = treeRoot
    index = 0
    while currentNode.left != None and currentNode.right != None:
        try:
            if y[index] == "0":
                currentNode = currentNode.left
            if y[index] == "1":
                currentNode = currentNode.right
            index +=1
        except:
            return (None, None, None, y)
    I = int(currentNode.data)
    new_y = y[index:]
    if I in previous_I:
        return find_current_I(j, alpha_value, new_y, previous_I) 
    Ia = I % alpha_value
    pi = int((I - Ia)/alpha_value)
    return(I,Ia,pi,new_y)

def decode(y, alpha_value):

    j = 0
    decoded = []
    previous_I = []
    new_y = y
    while True:
        I = y[j]
        j+= 1
        #[I,Ia,pi,new_y] = find_current_I(j, alpha_value, new_y, previous_I)
        Ia = I % alpha_value
        pi = int((I - Ia)/alpha_value)
        previous_I.append(I)
        if len(y)==j:
            #not_over = False
            break
        if pi != 0:
            decoded.append(str(decoded[pi-1]) + str(Ia))
        else:
            decoded.append(str(Ia))
        if len(new_y) == 0:
            break
    return list_to_str(decoded)

def int_to_min_bits(integer, length):
    if not integer:
        return 0

    # Step 2: Calculate the number of bits needed to represent the maximum integer
    num_bits = length.bit_length()

    # Step 3: Convert each integer to its binary representation using the calculated number of bits
    binary_representations = format(integer, f'0{num_bits}b')
    return binary_representations

def min_bits_to_int(binary_list):
    """
    Convert a list of binary strings (with the same bit length) back to a list of integers.

    Parameters:
    binary_list (list): A list of binary strings.

    Returns:
    list: A list of integers.
    """
    integers = [int(binary_str, 2) for binary_str in binary_list]
    return integers

def list_to_str(y):
    y_str = ""
    for i in y:
       y_str += str(i)

    return y_str


def list_to_str(y):
    y_str = ""
    for i in y:
       y_str += str(i)

    return y_str


def generate_iid_sequence(length, p = 1/2):
    return list_to_str(random.choices([0, 1], [p, 1-p], k = length))

def generate_markov(length, transitionMatrix):
    # Define the state names
    states = [0, 1]
    # Choose the starting state
    current = np.random.choice([0,1])  # Start with state 0
    seq = [current]
    prob = 1
    for _ in range(length-1):
        if current == 0:
            change = np.random.choice(states, replace=True, p=transitionMatrix[0])
            if change == 0:
                prob *= transitionMatrix[0][0]
                seq.append(0)
            else:
                prob *= transitionMatrix[0][1]
                current = 1
                seq.append(1)
        elif current == 1:
            change = np.random.choice(states, replace=True, p=transitionMatrix[1])
            if change == 1:
                prob *= transitionMatrix[1][1]
                seq.append(1)
            else:
                prob *= transitionMatrix[1][0]
                current = 0
                seq.append(0)
    return list_to_str(seq)

def generate_markov_second_order(length, transitionMatrix):
    # Define the state names
    states = [0, 1]
    
    # Choose the starting two states
    x_n_minus_2 = np.random.choice(states)
    x_n_minus_1 = np.random.choice(states)
    seq = [x_n_minus_2, x_n_minus_1]
    
    for _ in range(length - 2):  # -2 because we already have 2 states
        state_index = x_n_minus_2 * 2 + x_n_minus_1  # Convert binary state to index (00->0, 01->1, 10->2, 11->3)
        x_n = np.random.choice(states, p=transitionMatrix[state_index])
        
        seq.append(x_n)
        
        # Update states
        x_n_minus_2, x_n_minus_1 = x_n_minus_1, x_n
    
    return list_to_str(seq)

def check_if_iid(x):
    check = 0
    for i in x:
        check += int(i)
    check = check/100

def generate_log_range(start, end, num_dots):
    
    log_start = np.log10(start)
    log_end = np.log10(end)

    log_space = np.linspace(log_start, log_end, num_dots)
    n_values = np.power(10, log_space)
    return n_values

