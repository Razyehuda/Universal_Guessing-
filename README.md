# Universal Guessing with Side Information for Binary Sequence Estimation

## Authors
**Keren Mazaki and Raz Yehuda**

**Advisor:** Prof. Asaf Cohen

---

## Abstract
This project explores advanced algorithmic techniques for binary sequence estimation using universal guessing methods with side information. Three innovative variants of Lempel-Ziv (LZ) compression-based algorithms were implemented, enhancing the foundational universal guessing algorithm by A. Cohen and N. Merhav. The project focused on:

1. **Baseline Estimation**: Using side information for sequence guessing.
2. **Enhanced Estimation**: Leveraging known prefixes for improved accuracy.
3. **Advanced Optimization**: Combining learned patterns with LZ decoding for robust performance.

Detailed evaluation demonstrated the practical utility of these techniques in areas such as binary image reconstruction, offering significant improvements in denoising under challenging noise conditions.

---

## Introduction
Estimating unknown sequences from noisy observations is a cornerstone problem in information theory, communication systems, and cryptography. This project addresses this challenge by:

- Implementing and analyzing Lempel-Ziv compression algorithms.
- Innovating on universal guessing algorithms by incorporating side information and partial sequence knowledge.
- Designing solutions that bridge theoretical algorithms with real-world applications, such as image reconstruction and denoising.

The project highlights the integration of foundational theory with engineering rigor to develop scalable and adaptive solutions.

---

## Methods

### 1. Lempel-Ziv Compression

#### Standard LZ Compression
- **Encoding**: Parses input sequences into unique phrases using dynamic dictionaries.
- **Decoding**: Reconstructs the original sequence from compressed data with high fidelity.

#### LZ Compression with Side Information
- Enhances standard LZ compression by leveraging correlated side information, reducing entropy and improving compression rates.

### 2. Universal Guessing Algorithms
Three distinct algorithms were developed:

- **A1: Baseline Approach**
  Utilizes side information to guess sequences without prior training.

- **A2: Learning from Prefixes**
  Integrates a known prefix of the sequence to adaptively improve guessing accuracy.

- **A3: Advanced Pattern Matching**
  Uses observed patterns from prefixes to inform guesses without modifying existing dictionaries, ensuring robustness against noise.

---

## Results

### Compression Rate Analysis
Compression rates were analyzed for:
1. Independent and identically distributed (i.i.d.) sequences.
2. First-order and second-order Markov chains.

#### Key Findings:
- Compression rates converge to theoretical entropy limits.
- Incorporating side information significantly improves compression efficiency.

### Algorithm Performance
The algorithms were tested under diverse conditions, including:
1. Binary sequence estimation with varying noise levels.
2. Image reconstruction tasks with i.i.d. and structured noise.

#### Highlights:
- **Algorithm A2** exhibited the highest accuracy for long sequences, showcasing its ability to learn correlations effectively.
- Majority voting further enhanced the robustness of predictions, reducing error rates significantly.
- Image reconstruction accuracy exceeded baseline methods, validating the algorithms' practical effectiveness.

#### Binary Sequence Results:
- A2 demonstrated strong performance in noisy environments, with accuracy improvements of up to 15% over baseline approaches.
- A3 excelled in scenarios requiring consistent performance with shorter training data.

#### Image Reconstruction Results:
- Binary images were reconstructed with over 85% accuracy under moderate noise conditions.
- Both A2 and A3 algorithms outperformed standard denoising techniques, proving their applicability in real-world tasks.

---

## Practical Applications

### Binary Image Reconstruction
The algorithms were extended to image processing tasks, where they:
- Converted grayscale images into binary sequences.
- Applied advanced guessing methods to reconstruct noisy images.

Results demonstrated:
- Over 85% accuracy in reconstructing images degraded by both i.i.d. and structured noise.
- Clear improvements in feature recovery and denoising, outperforming elementary techniques.

### Broader Implications
This work can be adapted to:
- Error correction in communication systems.
- Enhancing storage efficiency in data compression tasks.
- Denoising and restoration in medical imaging and other critical applications.


