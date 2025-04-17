import numpy as np
import math

def emperical_entropy(x):
    # Calculate entropy of x
    _, counts = np.unique(x, return_counts=True)
    probabilities = counts / len(x)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

def binary_entropy_iid(p):

    entropy = -p * math.log2(p) - (1-p) * math.log2(1-p)
    return entropy

def joint_entropy(px, py):
    probablities = [px*py, (1-px)*py, (1-py)*px, (1-py)*(1-px)]
    entropy = 0
    for p in probablities:
        entropy += p*math.log2(p)
    return -entropy

def xor_iid_p(p1,p2):
    p = p1*(1-p2) + p2*(1-p1)
    return p


def binary_entropy_markov1(X, Y):
    # Ensure X and Y are lists
    X = list(X)
    Y = list(Y)
    
    # Initialize state counts
    state_counts = {(x, y1, y2): 0 for x in ['0', '1'] for y1 in ['0', '1'] for y2 in ['0', '1']}
    state_x_counts = {(x, y1, y2): 0 for x in ['0', '1'] for y1 in ['0', '1'] for y2 in ['0', '1']}
    #print(state_counts,state_x_counts )
    # Count occurrences
    for i in range(1, len(X) - 1):
        context = (X[i-1], Y[i], Y[i+1])
        state_counts[context] += 1
        state_x_counts[context] += int(X[i])
    
    # Calculate entropy
    entropy = 0
    total_counts = sum(state_counts.values())

    for context, count in state_counts.items():
        if count > 0:
            context_prob = count / total_counts
            p_1 = state_x_counts[context] / count
            p_0 = 1 - p_1
            context_entropy = 0
            if p_0 > 0:
                context_entropy -= p_0 * np.log2(p_0)
            if p_1 > 0:
                context_entropy -= p_1 * np.log2(p_1)
            entropy += context_prob * context_entropy
    
    return entropy

def binary_entropy_markov2(X, Y):
    # Ensure X and Y are lists
    X = list(X)
    Y = list(Y)
    
    # Initialize state counts
    state_counts = {(x1, x2, y1, y2, y3): 0 for x1 in ['0', '1'] for x2 in ['0', '1'] 
                    for y1 in ['0', '1'] for y2 in ['0', '1'] for y3 in ['0', '1']}
    state_x_counts = {(x1, x2, y1, y2, y3): 0 for x1 in ['0', '1'] for x2 in ['0', '1'] 
                      for y1 in ['0', '1'] for y2 in ['0', '1'] for y3 in ['0', '1']}

    # Count occurrences
    for i in range(2, len(X) - 2):
        context = (X[i-2], X[i-1], Y[i], Y[i+1], Y[i+2])
        state_counts[context] += 1
        state_x_counts[context] += int(X[i])
    
    # Calculate entropy
    entropy = 0
    total_counts = sum(state_counts.values())

    for context, count in state_counts.items():
        if count > 0:
            context_prob = count / total_counts
            p_1 = state_x_counts[context] / count
            p_0 = 1 - p_1
            context_entropy = 0
            if p_0 > 0:
                context_entropy -= p_0 * np.log2(p_0)
            if p_1 > 0:
                context_entropy -= p_1 * np.log2(p_1)
            entropy += context_prob * context_entropy
    
    return entropy


def joint_probabilities(px, pz):
    """Calculate joint probabilities P(X, Y)"""
    py_0 = (1 - px) * (1 - pz) + px * pz  # P(Y=0)
    py_1 = (1 - px) * pz + px * (1 - pz)  # P(Y=1)
    p_x0_y0 = (1 - px) * (1 - pz) / py_0  # P(X=0 | Y=0)
    p_x1_y0 = px * pz / py_0  # P(X=1 | Y=0)
    p_x0_y1 = (1 - px) * pz / py_1  # P(X=0 | Y=1)
    p_x1_y1 = px * (1 - pz) / py_1  # P(X=1 | Y=1)
    return py_0, py_1, p_x0_y0, p_x1_y0, p_x0_y1, p_x1_y1

def conditional_entropy_iid(px, pz):
    """Calculate H(X|Y)"""
    py_0 = (1-px)*(1-pz) + px*pz
    py_1 = px*(1-pz) + (1-px)*pz
    px1_given_y0 = (pz*px)/(py_0) #p(y=0|x=1)*p(x=1)/p(y=0)
    px1_given_y1 = ((1-pz)*px)/(py_1) #p(y=1|x=1)*p(x=1)/p(y=1)
    H_X_given_Y0 = binary_entropy_iid(px1_given_y0)
    H_X_given_Y1 = binary_entropy_iid(px1_given_y1)
    return py_0 * H_X_given_Y0 + py_1 * H_X_given_Y1

def conditional_entropy_iid_empiric(X, Y):
   # Ensure X and Y are lists
    X = list(X)
    Y = list(Y)
    
    # Initialize state counts
    state_counts = {(y): 0 for y in ['0', '1']}
    state_x_counts = {(y): 0 for y in ['0', '1']}
    #print(state_counts,state_x_counts )
    # Count occurrences
    for i in range(len(X)):
        context = (Y[i])
        state_counts[context] += 1
        state_x_counts[context] += int(X[i])
    
    # Calculate entropy
    entropy = 0
    total_counts = sum(state_counts.values())

    for context, count in state_counts.items():
        if count > 0:
            context_prob = count / total_counts
            p_1 = state_x_counts[context] / count
            p_0 = 1 - p_1
            context_entropy = 0
            if p_0 > 0:
                context_entropy -= p_0 * np.log2(p_0)
            if p_1 > 0:
                context_entropy -= p_1 * np.log2(p_1)
            entropy += context_prob * context_entropy
    
    return entropy


