# Universal_Guessing-
Universal Guessing with Side Information for Binary Sequence Estimation
# Universal Guessing with Side Information for Binary Sequence Estimation

## Authors
**Keren Mazaki and Raz Yehuda**

**Advisor:** Prof. Asaf Cohen

---

## Abstract
This project showcases advanced algorithmic techniques for binary sequence estimation using universal guessing methods with side information. We explored and implemented three innovative variants of Lempel-Ziv (LZ) compression-based algorithms, enhancing the foundational universal guessing algorithm by A. Cohen and N. Merhav. The project focused on:

1. **Baseline Estimation**: Using side information for sequence guessing.
2. **Enhanced Estimation**: Leveraging known prefixes for improved accuracy.
3. **Advanced Optimization**: Combining learned patterns with LZ decoding for robust performance.

Through detailed evaluation, we demonstrated the practical utility of these techniques in areas such as binary image reconstruction, offering significant improvements in denoising under challenging noise conditions.

---

## Introduction
The challenge of estimating unknown sequences from noisy observations is a cornerstone problem in information theory, communication systems, and cryptography. As an engineer, I tackled this problem by:

- Implementing and analyzing Lempel-Ziv compression algorithms.
- Innovating on universal guessing algorithms by incorporating side information and partial sequence knowledge.
- Designing practical solutions that bridge theoretical algorithms with real-world applications, such as image reconstruction and denoising.

The project reflects my ability to merge foundational theory with engineering rigor to develop scalable and adaptive solutions.

---

## Methods

### 1. Lempel-Ziv Compression

#### Standard LZ Compression
- **Encoding**: Efficiently parsed input sequences into unique phrases using dynamic dictionaries.
- **Decoding**: Reconstructed the original sequence from compressed data with high fidelity.

#### LZ Compression with Side Information
- Enhanced standard LZ compression by leveraging correlated side information, reducing entropy and improving compression rates.

### 2. Universal Guessing Algorithms
As part of the project, I engineered three distinct algorithms:

- **A1: Baseline Approach**
  Utilized side information to guess sequences without prior training.

- **A2: Learning from Prefixes**
  Integrated a known prefix of the sequence to adaptively improve guessing accuracy.

- **A3: Advanced Pattern Matching**
  Used observed patterns from prefixes to inform guesses without modifying existing dictionaries, ensuring robustness against noise.

---

## Results

### Compression Rate Analysis
Compression rates were thoroughly analyzed for:
1. Independent and identically distributed (i.i.d.) sequences.
2. First-order and second-order Markov chains.

#### Key Achievements:
- Achieved convergence of compression rates to theoretical entropy limits.
- Demonstrated that incorporating side information significantly improves compression efficiency.

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

---

## Conclusion
This project illustrates the power of universal guessing algorithms in addressing complex estimation problems. My key contributions include:
- **Innovative Algorithm Design**: Developing and extending Lempel-Ziv-based methods to integrate side information and prefixes.
- **Practical Impact**: Demonstrating the applicability of these techniques in binary image reconstruction and noise handling.
- **Engineering Rigor**: Translating theoretical constructs into efficient, implementable solutions.

### Future Directions
- Developing hybrid algorithms that combine the strengths of A2 and A3.
- Extending the methods to sequences with larger alphabets and higher dimensional data.
- Investigating real-time applications in communication and data storage systems.

---

## References
1. N. Merhav and A. Cohen, "Universal randomized guessing with application to asynchronous decentralized brute-force attacks," *IEEE Transactions on Information Theory*, vol. 66, no. 4, pp. 2651–2671, 2020.
2. J. Ziv and A. Lempel, "Compression of individual sequences via variable-rate coding," *IEEE Transactions on Information Theory*, vol. 24, no. 5, pp. 530–536, 1978.
3. T. M. Cover and J. A. Thomas, *Elements of Information Theory*. Wiley-Interscience, 2nd ed., 2006.
4. T. Uyematsu and S. Kuzuoka, "Conditional lempel-ziv complexity and its application to source coding theorem with side information," *IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences*, vol. E86-A, no. 10, pp. 2615–2617, 2003.
