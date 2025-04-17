from tree import *
from utils import *
from algorithms import *
from entropy import *
from compression import *
import matplotlib.pyplot as plt
import numpy as np
import time
import os

def generate_values(pz, px, n_values, num_iter, generate_sequence, generate_entropy, iid = False):
    compression = []
    entropy_list = []

    for n in n_values:
        n = int(n)
        print (f"starting with n = {n}")
        comp_sum = 0
        entropy_sum = 0

        iterations = max(int(num_iter * (1 - (np.log2(n) / np.log2(n_max)))), 1)

        for _ in range(iterations):
            z = generate_iid_sequence(n, p=pz)
            x = generate_sequence(n, px)
            y = bitwise_xor(x, z)
            if iid:
                entropy = generate_entropy(px,pz)
            else:
                if n == n_values[-1]:
                    entropy = generate_entropy(x, y)
            ClogC = encode_series(x, y)[2]
            comp_sum += ClogC / n
            if iid or n == n_values[-1]:
                entropy_sum += entropy

        compression.append(comp_sum / iterations)
        if iid:
            entropy_list.append(entropy_sum / iterations)
        else:
            if n == n_values[-1]:
                entropy_list.append(entropy_sum)

    entropy_avg = sum(entropy_list) / len(entropy_list)
    entropy_list = [entropy_avg] * len(n_values)
    return n_values, compression, entropy_list

def plot(values, compression, entropy, pz, color):

    plt.plot(values, compression, label=f'pz = {pz}', linewidth=3, color=color)
    plt.plot(values, entropy, label=f'H(X|Y), pz = {pz}', linestyle='--', linewidth=1, color=color)
    plt.ylabel('Compression rate')
    plt.xlabel('length')
    plt.legend(loc='upper right')




save_dir = ""#C:/Users/keren/Documents/school/fourth year/second semester/project/graphs/SI compression/"

start_time = time.time()
px_values = [0.1, 0.2, 0.5]
pz_values = [0.01, 0.1, 0.3, 0.5]
colors = ['red', 'blue', 'green', 'purple']
n_max = 1e4
n_values = generate_log_range(start=1, end=n_max, num_dots=20)
#n_values = np.logspace(0, 6, num = 50, dtype=int)
num_iter = 20

for px in px_values:
    print(f"\nstarting with px = {px}")
    transitionMatrix1 = [[px, 1 - px],  # 0 -> 0, 1
                        [1 - px, px]]   # 1 -> 0, 1
    
    transitionMatrix2 = [[px, 1 - px],  # 00 -> 00, 01
                        [1 - px, px],  # 01 -> 10, 11
                        [1 - px, px],  # 10 -> 00, 01
                        [px, 1 - px]]  # 11 -> 10, 11

    #i.i.d
    print(f"\ni.i.d")
    plt.figure()
    dist = "iid"
    for pz, color in zip(pz_values, colors):
        print(f"\nstarting with pz = {pz}")
        n_values, compression, entropy = generate_values(pz, px, n_values, num_iter, generate_iid_sequence, conditional_entropy_iid, iid = True)
        plot(n_values, compression, entropy, pz, color)
    plt.title(f'Conditioned Compression of i.i.d sequence With px = {px}')
    plt.tight_layout()
    save_path = os.path.join(save_dir, f'x_{dist}/px_{px}.png')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)

    #first order markov
    print(f"\nmarkov first order") 
    plt.figure()
    dist = "markov1st"
    for pz, color in zip(pz_values, colors):
        print(f"starting with pz = {pz}")
        n_values, compression, entropy = generate_values(pz, transitionMatrix1, n_values, num_iter, generate_markov1, binary_entropy_markov1)
        plot(n_values, compression, entropy, pz, color)
    plt.title(f'Conditioned Compression of First Order Markov Chain With px = {px}')
    plt.tight_layout()
    save_path = os.path.join(save_dir, f'x_{dist}/px_{px}.png')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)

    #second order markov
    print(f"\nmarkov second order") 
    plt.figure()
    dist = "markov2nd"
    for pz, color in zip(pz_values, colors):
        print(f"starting with pz = {pz}")
        n_values, compression, entropy = generate_values(pz, transitionMatrix2, n_values, num_iter, generate_markov2, binary_entropy_markov2)
        plot(n_values, compression, entropy, pz, color)
    plt.title(f'Conditioned Compression of Second Order Markov Chain With px = {px}')
    plt.tight_layout()
    save_path = os.path.join(save_dir, f'x_{dist}/px_{px}.png')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)

end_time = time.time()
print(f"Execution time: {(end_time - start_time)/60:.2f} minutes")
# Show the figures only once at the end
plt.show(block = True)
