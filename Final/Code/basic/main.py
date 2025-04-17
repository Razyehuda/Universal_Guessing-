import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from Entropy import *
from BinaryTree import *
from Utils import *
import time

start_time = time.time()

def run_compression_experiment(p, n_values, num_iter, n_max, generate_sequence, calculate_entropy):
    entropy = calculate_entropy(p)
    compression_results = []

    for n in n_values:
        n = int(n)
        print(f"starting with n = {n}")
        total_compression = 0
        iterations = max(int(num_iter * (1 - (math.log2(n) / math.log2(n_max)))), 1)

        for _ in range(iterations):
            sequence = generate_sequence(n, p)
            encoded_sequence = encode(sequence)
            compressed_length = len(encoded_sequence)
            total_compression += (compressed_length * (math.log2(compressed_length)) / n) / iterations

        compression_results.append(total_compression)

    return compression_results, entropy

def plot_compression_results(n_values, compression_data, title, block):
    plt.figure()
    plt.title(title)

    for p, (compression, entropy, color) in compression_data.items():
        plt.plot(n_values, compression, label=f'p = {p}', color=color, linewidth=3)
        plt.plot(n_values, [entropy] * len(n_values), label=f'H(X), p = {p}', color=color, linestyle='--', linewidth=1)

    plt.xlabel('n')
    plt.ylabel(r'$\frac{1}{n} C \cdot \log C$')
    plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show(block=block)

def main():
    n_max = 1e7
    n_values = generate_log_range(start=100, end=n_max, num_dots=20)
    num_iter = 30
    p_values = [0.99, 0.8, 0.5]

    markov_compressions = {}
    iid_compressions = {}
    second_order_markov_compressions = {}

    for p in p_values:
        print(f"\nstarting with p = {p}")
        transitionMatrix1 = [[p, 1 - p],  # 0 -> 0, 1
                            [1 - p, p]]   # 1 -> 0, 1
        
        transitionMatrix2 = [[p, 1 - p],  # 00 -> 00, 01
                            [1 - p, p],  # 01 -> 10, 11
                            [1 - p, p],  # 10 -> 00, 01
                            [p, 1 - p]]  # 11 -> 10, 11
    

        # Run i.i.d. compression experiment
        print("i.i.d")
        iid_compression, iid_entropy = run_compression_experiment(
            p, n_values, num_iter, n_max, generate_iid_sequence, binary_entropy_iid
        )
        iid_compressions[p] = (iid_compression, iid_entropy, "red" if p == 0.99 else "green" if p == 0.8 else "blue")

        # Run first-order Markov compression experiment
        print("markov 1st order")
        markov_compression, markov_entropy = run_compression_experiment(
            transitionMatrix1, n_values, num_iter, n_max, generate_markov, binary_entropy_markov
        )
        markov_compressions[p] = (markov_compression, markov_entropy, "red" if p == 0.99 else "green" if p == 0.8 else "blue")

        # Run second-order Markov compression experiment
        print("markov 2nd order")
        second_order_markov_compression, second_order_markov_entropy = run_compression_experiment(
            transitionMatrix2, n_values, num_iter, n_max, generate_markov_second_order, binary_entropy_markov
        )
        second_order_markov_compressions[p] = (second_order_markov_compression, second_order_markov_entropy, "red" if p == 0.99 else "green" if p == 0.8 else "blue")
    

    end_time = time.time()
    print(f"Execution time: {(end_time - start_time)/60:.2f} minutes")

    # Plot results with block=False except for the last one
    plot_compression_results(n_values, markov_compressions, 'Compression of First-Order Markov Chain', block=False)
    plot_compression_results(n_values, iid_compressions, 'Compression of i.i.d Sequence', block=False)
    plot_compression_results(n_values, second_order_markov_compressions, 'Compression of Second-Order Markov Chain', block=True)



if __name__ == "__main__":
    main()
