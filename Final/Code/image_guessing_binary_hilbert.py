import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from utils import *
import os
from algorithms import guessing, new_guessing
from scipy.spatial import distance

def hilbert_curve_index(x, y, n):
    """
    Returns the index of the point (x, y) on the Hilbert curve of order n.
    """
    h = 0
    d = 1 << (n - 1)
    for s in range(n):
        rx = (x & d) > 0
        ry = (y & d) > 0
        h += d * d * ((3 * rx) ^ ry)
        x, y = rot(n, x, y, rx, ry)
        d >>= 1
    return h

def rot(n, x, y, rx, ry):
    """
    Rotate/flip a quadrant appropriately.
    """
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        # Swap x and y
        x, y = y, x
    return x, y

def hilbert_curve_transform(image_array):
    """
    Transform an image array into a vector using the Hilbert curve.
    """
    n = int(np.log2(image_array.shape[0]))
    
    vector = []
    for y in range(image_array.shape[0]):
        for x in range(image_array.shape[1]):
            index = hilbert_curve_index(x, y, n)
            vector.append((index, image_array[y, x]))
    
    vector.sort()  # Sort based on Hilbert curve index
    return [v[1] for v in vector]

def hilbert_curve_inverse_transform(vector, shape):
    """
    Transform a Hilbert curve-ordered vector back into an image array.
    """
    n = int(np.log2(shape[0]))
    image_array = np.zeros(shape)
    
    index_to_pos = {}
    for y in range(shape[0]):
        for x in range(shape[1]):
            index = hilbert_curve_index(x, y, n)
            index_to_pos[index] = (y, x)
    
    for i, val in enumerate(vector):
        y, x = index_to_pos[i]
        image_array[y, x] = val
    
    return image_array

def png_to_binary_bit_sequence(file_path, threshold=128):
    with Image.open(file_path) as img:
        img_array = np.array(img.convert('L'))
    img_binary = (img_array < threshold).astype(int)
    
    hilbert_vector = hilbert_curve_transform(img_binary)
    return hilbert_vector, img_binary.shape

def display_bit_sequence_as_image(bit_list, original_shape, ax=None, title=None, draw_rect = False):
    img_array = hilbert_curve_inverse_transform(bit_list, original_shape)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img_array, cmap='binary')
    ax.axis('off')
    if title:
        ax.set_title(title)

    width = int(math.sqrt(l))
    height = width

    if draw_rect:
        rect = Rectangle((0, 0), width, height, fill=False, edgecolor='red', linewidth=2)
        #ax.add_patch(rect)


def save_binary_image(file_path, output_path, threshold=128):
    with Image.open(file_path) as img:
        img_array = np.array(img.convert('L'))
    img_binary = (img_array < threshold).astype(np.uint8) * 255
    Image.fromarray(img_binary).save(output_path)

def majority_vote_guessing(x, y, l,algo, num_runs=11):
    total = [0] * len(x)
    for _ in range(num_runs):
        #print(_)
        #guessed_x = guessing(x[:l], y)[:len(x)]
        guessed_x = algo(x[:l], y)
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

   
if __name__ == "__main__":

    #save_dir = "C:/Users/keren/Documents/school/fourth year/second semester/project/graphs/image_guessing/"
    #os.makedirs(save_dir, exist_ok=True)

    noise_num = 1
    image_path = 'lena512.png'
    noise_path = f'noises/{noise_num}.png'
    noise_image = False
    
    # Load and convert image to binary sequence
    input_list, shape = png_to_binary_bit_sequence(image_path)
    input_str = list_to_str(input_list)

    n = len(input_str)
    l = int(0.2*n)
    
    # Generate noise and apply to image
    pz = 0.3
    transitionMatrix1 = [[pz, 1 - pz],  # 0 -> 0, 1
                         [1 - pz, pz]]   # 1 -> 0, 1
    stat_p = 0.01
    dist = "iid"

    if noise_image:    
        noise_list = png_to_binary_bit_sequence(noise_path, threshold=200)[0]
        noise_str = list_to_str(noise_list)
    else:
        if dist == "iid":
            noise_str = generate_iid_sequence(n, pz)
        elif dist == "markov1st":
            noise_str = generate_markov1(n, transitionMatrix1, stat_p = stat_p)
        noise_list = [int(i) for i in noise_str]



    noisy_str = bitwise_xor(input_str, noise_str)
    noisy_list = [int(i) for i in noisy_str]
    
    # Perform guessing algorithm
    guessed_str = majority_vote_guessing(input_str, noisy_str, l,guessing,num_runs = 11)
    print('done A2')
    guessed_str2 = majority_vote_guessing(input_str, noisy_str, l,new_guessing, num_runs = 1)
    print('done A3')
    guessed_list = [int(i) for i in guessed_str[:n]]
    guessed_list2 = [int(i) for i in guessed_str2[:n]]
    # Display results
    fig, axs = plt.subplots(1, 2, figsize=(15, 10))
    title = f'Image Guessing:'

    if not noise_image:
        title += f' {dist} noise, pz = {pz}, l = {l/n*100:.0f}%'
        if dist == "markov1st":
            title += f', stationary distrubotion - {stat_p}'

    fig.suptitle(title, fontsize=16)
    display_bit_sequence_as_image(guessed_list, shape, ax=axs[0], title='A2', draw_rect = False)
    display_bit_sequence_as_image(guessed_list2, shape, ax=axs[1], title='A3')

    plt.tight_layout()
    

    if noise_image:
        name = f'hilbert_noise_{noise_num}.png'
    else:
        name = f'{dist}_noise_pz_{pz}_l_{l/n*100:.0f}%.png'
        if dist == "markov1st":
            name = f'stat_p_{stat_p}_' + name

    #save_path = os.path.join(save_dir, name)
    #plt.savefig(save_path)
    
    # Calculate and print accuracy
    fails = sum(int(bit) for bit in bitwise_xor(input_str[l:], guessed_str[l:])) / (n - l)
    accuracy = (1 - fails) * 100
    fails2 = sum(int(bit) for bit in bitwise_xor(input_str[l:], guessed_str2[l:])) / (n - l)
    accuracy2 = (1 - fails2) * 100
    print(f"l: {l}, accuracy for A2: {accuracy:.2f}%")
    print(f"l: {l}, accuracy for A3: {accuracy2:.2f}%")
    plt.show(block = True)
