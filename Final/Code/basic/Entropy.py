
import math
import numpy as np

def binary_entropy_iid(p):

    entropy = -p * math.log2(p) - (1-p) * math.log2(1-p)
    return entropy

def binary_entropy_markov(TransitionMatrix):

    p = TransitionMatrix[0][0]
    return binary_entropy_iid(p)

# Calculate the stationary distribution
def stationary_distribution(P):
    eigvals, eigvecs = np.linalg.eig(P.T)
    stationary = np.array(eigvecs[:, np.isclose(eigvals, 1)])
    stationary = stationary[:, 0]
    stationary = stationary / stationary.sum()
    return stationary.real

# Calculate the entropy of the Markov chain
def markov_chain_entropy(P):
    stationary_dist = stationary_distribution(P)
    entropy = -np.sum(stationary_dist[:, None] * P * np.log2(P + 1e-9))  # Add a small value to avoid log(0)
    return entropy

# Calculate the entropy

