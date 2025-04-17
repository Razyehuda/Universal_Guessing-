import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from utils import *
import os
from algorithms import guessing, new_guessing


def png_to_binary_bit_sequence(file_path, threshold=128):
    with Image.open(file_path) as img:
        img_array = np.array(img.convert('L'))
    img_binary = (img_array < threshold).astype(int)
    return img_binary.flatten().tolist(), img_binary.shape

def display_bit_sequence_as_image(bit_list, original_shape, ax=None, title=None, highlight_region=None, save = False):
    img_array = np.array(bit_list).reshape(original_shape)
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img_array, cmap='binary')
    ax.axis('off')
    if title:
        ax.set_title(title)
   
    if highlight_region:
        l, height, width = highlight_region
        rows = l // width
        last_row_cols = l % width
        
        # Highlight the guessed part (from l to the end)
        rect = Rectangle((0, rows), width, height - rows, fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)
        if last_row_cols > 0:
            rect = Rectangle((last_row_cols, rows - 1), width - last_row_cols, 1, fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)

    if save:
        # Normalize the array to the range [0, 255]
        normalized_array = ((1 - img_array) * 255).astype(np.uint8)
        
        # Create a PIL image from the array
        image = Image.fromarray(normalized_array)
        
        # Save the image
        #image.save(save_path)
            

def save_binary_image(file_path, output_path, threshold=128):
    with Image.open(file_path) as img:
        img_array = np.array(img.convert('L'))
    img_binary = (img_array > threshold).astype(np.uint8) * 255
    Image.fromarray(img_binary).save(output_path)

def majority_vote_guessing(x, y, l, num_runs=11):
    total = [0] * len(x)
    for _ in range(num_runs):
        #guessed_x = guessing(x[:l], y)[:len(x)]
        guessed_x = new_guessing(x[:l], y)
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

    save_dir = "C:/Users/Razye/Desktop/code/results/new_guessing/images/"
    os.makedirs(save_dir, exist_ok=True)

    noise_num = 1
    image_path = 'lena512.png'
    noise_path = f'noises/{noise_num}.png'
    noise_image = True
    
    # Load and convert image to binary sequence
    input_list, shape = png_to_binary_bit_sequence(image_path)
    input_str = list_to_str(input_list)

    n = len(input_str)
    l = int(0.2*n)
    
    # Generate noise and apply to image
    pz = 0.3
    transitionMatrix1 = [[1 - pz, pz],  # 0 -> 0, 1
                         [pz, 1 - pz]]   # 1 -> 0, 1
    stat_p = 0.5
    dist = "iid"

    if noise_image:    
        noise_list = png_to_binary_bit_sequence(noise_path, threshold=128)[0]
        noise_str = list_to_str(noise_list)
    else:
        if dist == "iid":
            noise_str = generate_iid_sequence(n, pz)
            save_path = os.path.join(save_dir, f"iid_noise_pz_{pz}.png")
        elif dist == "markov1st":
            noise_str = generate_markov1(n, transitionMatrix1, stat_p = stat_p)
            save_path = os.path.join(save_dir, f"markov1st_noise_pz_{pz}_stat_p_{stat_p}.png")
        noise_list = [int(i) for i in noise_str]

    noisy_str = bitwise_xor(input_str, noise_str)
    noisy_list = [int(i) for i in noisy_str]
    
    # Perform guessing algorithm
    #guessed_str = majority_vote_guessing(input_str, noisy_str, l)
    guessed_str = guessing(input_str[:l], noisy_str)
    guessed_list = [int(i) for i in guessed_str[:n]]
    
    # Display results
    fig, axs = plt.subplots(1, 4, figsize=(15, 10))
    title = f'Image Guessing:'

    if not noise_image:
        title += f' {dist} noise, pz = {pz}, l = {l/n*100:.0f}%'
        if dist == "markov1st":
            title += f', stationary distrubotion - {stat_p}'

    fig.suptitle(title, fontsize=16)
    display_bit_sequence_as_image(input_list, shape, ax=axs[0], title='Original')
    display_bit_sequence_as_image(noise_list, shape, ax=axs[1], title='Noise')
    display_bit_sequence_as_image(noisy_list, shape, ax=axs[2], title='Noisy')
    display_bit_sequence_as_image(guessed_list, shape, ax=axs[3], title='Guessing',
                                  highlight_region=(l, shape[0], shape[1]))
    plt.tight_layout()
    

    if noise_image:
        name = f'noise_{noise_num}.png'
    else:
        name = f'{dist}_noise_pz_{pz}_l_{l/n*100:.0f}%.png'
        if dist == "markov1st":
            name = f'stat_p_{stat_p}_' + name

    save_path = os.path.join(save_dir, name)
    #plt.savefig(save_path)
    
    # Calculate and print accuracy
    fails = sum(int(bit) for bit in bitwise_xor(input_str[l:], guessed_str[l:])) / (n - l)
    accuracy = (1 - fails) * 100
    print(f"l: {l}, accuracy: {accuracy:.2f}%")

    plt.show(block = True)