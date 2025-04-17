import numpy as np
import os
from tree import *
from utils import *
from algorithms import *
from entropy import *
from compression import *
from tqdm import tqdm
from typing import List, Tuple
import matplotlib.pyplot as plt


# Assume all other imports and functions remain the same
def generate_values(n, px, pz, dist, z_dist, save_dir, load =  False, save = False):
    if load:
        x, y = load_sequences(n, save_dir)
        return x,y
    
    if dist == "markov_1st_order":
        transitionMatrix1 = [[px, 1-px], [1-px, px]]
        x = generate_markov1(n, transitionMatrix1)
        print(x)
    elif dist == "markov_2nd_order":
        transitionMatrix2 = [[px, 1 - px],  # 00 -> 00, 01
                            [1 - px, px],  # 01 -> 10, 11
                            [1 - px, px],  # 10 -> 00, 01
                            [px, 1 - px]]  # 11 -> 10, 11

        x = generate_markov2(n, transitionMatrix2)
        print(x)
    elif dist == "iid":
        x = generate_iid_sequence(n, p = px)

    if z_dist == "iid":
        z = generate_iid_sequence(n, p=pz)
    else:
        z = generate_markov1(n, [[pz, 1 - pz],[1 - pz, pz]])

    y = bitwise_xor(x, z)

    if save:
        save_sequences(n, x, y, save_dir)
    
    return x, y

def save_sequences(n, x, y, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f'px_{p}_pz_{pz}_n_{n}.txt')
    
    with open(save_path, 'w') as f:
        # Write full x
        f.write(''.join(map(str, x)) + '\n')
        
        # Write full y
        f.write(''.join(map(str, y)) + '\n')
    
    print(f"Sequences saved to {save_path}")

def load_sequences(n, save_dir):
    load_path = os.path.join(save_dir, f'px_{p}_pz_{pz}_n_{n}.txt')
    
    with open(load_path, 'r') as f:
        lines = f.readlines()
        x = lines[0].strip()
        y = lines[1].strip()
    print(f"Sequences loaded from {load_path}")
    return x, y

def majority_vote_guessing(x, y, l, num_runs):
    total = [0] * len(x)
    for _ in range(num_runs):
        guessed_x = guessing(x[:l], y)[:len(x)]
        #guessed_x = new_guessing(x[:l], y)
        for i, bit in enumerate(guessed_x):
            total[i] += int(bit)
    
    # Compute majority vote
    result = ''
    for sum_val in total:
        if sum_val / num_runs > 0.5:
            result += '1'
        else:
            result += '0'
    
    return result

def calculate_accuracy(x: str, y: str, l: int, n: int, jump: int, guessing_method: callable) -> Tuple[List[float], float]:
    total_correct_bits = np.zeros(n // jump)
    xor_sum = 0
    guessed_x = []
    if guessing_method.__name__ == 'decode_series_random':
        guessed_x = guessing_method(y)
    elif guessing_method.__name__ in ['guessing', 'new_guessing']:
        print(guessing_method.__name__, l, "starting")
        done = 0
        tries = 0

        while not done:
            try:
                #guessed_x = guessing_method(x[:l], y)
                #guessed_x = fast_majority_vote_guessing(x[:l], y, guessing_method , num_runs=51)
                if guessing_method.__name__ == 'guessing':
                    guessed_x = fast_majority_vote_guessing(x[:l], y, guessing_method , num_runs=21)
                else:
                    guessed_x = fast_majority_vote_guessing(x[:l], y, guessing_method , num_runs=5)
                done = 1
                print(guessing_method.__name__ ,l," done")
            except Exception as e:
                print(f"Error occurred: {e}. Retrying...")
                tries += 1
                print("failed",guessing_method.__name__, f"with {tries} tries")
                
                done = 0
    else:
        raise ValueError(f"Unknown guessing method: {guessing_method.__name__}")
    
    guessed_x = guessed_x[:len(x)]
    
    correct_bits = []
    xor_sum = sum(int(x_bit) != int(g_bit) for x_bit, g_bit in zip(x[l:], guessed_x[l:])) / (n - l)
    
    for i in range(0, n, jump):
        end_idx = min(i + jump, n)
        segment_x = x[i:end_idx]
        segment_guessed_x = guessed_x[i:end_idx]
        correct_bits.append(sum(int(x_bit) == int(g_bit) for x_bit, g_bit in zip(segment_x, segment_guessed_x)) / len(segment_x) * 100)
    
    total_correct_bits[:len(correct_bits)] = correct_bits
    percent = 100 - (xor_sum * 100)
    #print(x[n//2:n//2 + 100])
    #print("hey")
    #print(guessed_x[n//2:n//2 + 100])
    return total_correct_bits, percent

    

def plot_algorithm_comparison(n: int, jump: int, p: float, pz: float, dist_list: List[str], z_dist_list: List[str], save_dir: str, load: bool = False, save: bool = False):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 6), sharey=True)
    
    algorithms = [("Algorithm A2", guessing, 'solid'), ("Algorithm A3", new_guessing, 'solid')]
    
    lines_by_algorithm = [[], []]
    labels_by_algorithm = [[], []]

    for dist in dist_list:
        for z_dist in z_dist_list:
            name = f"{dist}_{z_dist}_px{str(p).replace('.', '')}_pz{str(pz).replace('.', '')}"
            current_save_dir = os.path.join(save_dir, f"{dist}_{z_dist}/")
            os.makedirs(current_save_dir, exist_ok=True)
            
            x, y = generate_values(n, p, pz, dist, z_dist, current_save_dir, load, save)
            
            l_values = [int(l * n) for l in [0.01, 0.05, 0.1,0.2,0.3]] #*0.05
            colors = plt.cm.rainbow(np.linspace(0, 1, len(l_values)))
            
            for idx, (ax, (algorithm_name, algorithm, linestyle)) in enumerate(zip([ax1, ax2], algorithms)):
                for l_idx, l in enumerate(l_values):
                    average_correct_bits, percent = calculate_accuracy(x, y, l, n, jump, algorithm)
                    label = f'l={l} bits, accuracy = {percent:.2f}%'
                    line = ax.plot(np.array(range(len(average_correct_bits))) * jump, average_correct_bits, 
                                   color=colors[l_idx], linestyle=linestyle, label=label)
                    lines_by_algorithm[idx].extend(line)
                    labels_by_algorithm[idx].append(label)
                
                ax.set_title(f'{algorithm_name}', pad=10)
                ax.set_xlabel("Bit's index")
                ax.grid(True, linestyle=':', alpha=0.7)
            
            ax1.set_ylabel(f"% correct guesses per {jump} bits")

    # Adjust layout and add separate legends below each plot
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.3)  # Make room for the legends

    # Create separate legends for each algorithm
    for idx, (ax, lines, labels) in enumerate(zip([ax1, ax2], lines_by_algorithm, labels_by_algorithm)):
        legend = ax.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
                           ncol=1, fontsize='small', title=f"Overall Accuracy: {algorithms[idx][0]}")
        ax.add_artist(legend)
    filename = os.path.join(current_save_dir, name)
    #plt.savefig(filename,dpi=300, bbox_inches='tight')
    
    
    plt.show()



def fast_majority_vote_guessing(x_partial, y, algo, num_runs=3):
    total = np.zeros(len(y), dtype=int)
    for _ in range(num_runs):
        guessed_x = algo(x_partial, y)[:len(y)]
        total += np.fromiter(map(int, guessed_x), dtype=int)
    
    return ''.join(np.where(total > num_runs // 2, '1', '0'))

if __name__ == "__main__":
    n = int(1e5)
    jump = 5000
    p = 0.8
    pz = 0.5
    
    dist_list = ["iid"]
    z_dist_list = ["iid"]

    save_dir = "C:/Users/Razye/Desktop/with_legend_n/"
    
    plot_algorithm_comparison(n, jump, p, pz, dist_list, z_dist_list, save_dir, load=False, save=True)
    print("done")