# 🔐 Quantum Encryption Scheme Based on Taylor Series & Fourier Transform

> **Published in IEEE** | Amrita Vishwa Vidyapeetham, Coimbatore

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-6929C4?style=for-the-badge&logo=qiskit&logoColor=white)](https://qiskit.org)
[![IEEE](https://img.shields.io/badge/Published-IEEE-00629B?style=for-the-badge&logo=ieee&logoColor=white)]()
[![Accuracy](https://img.shields.io/badge/Encrypted%20Accuracy-96.60%25-brightgreen?style=for-the-badge)]()

---

## 📄 Abstract

This paper proposes a novel quantum encryption scheme combining **Quantum Fourier Transform (QFT)**, **Taylor Series**, and **quantum gates** to establish a secure, key-based encryption and decryption pipeline. The scheme is designed to enable **privacy-preserving machine learning** and **federated learning** by performing computations directly on encrypted data using **CKKS-based Homomorphic Encryption**.

The proposed approach achieves identical accuracy on encrypted vs plaintext inference — **96.60% accuracy** on a 2000-sample diabetes dataset — demonstrating that secure computation does not compromise model performance.

---

## 🏗️ System Architecture

```
Classical Data
      │
      ▼
Ry Gates (encode data into quantum states)
      │
      ▼
Quantum Fourier Transform (QFT) — domain transformation
      │
      ▼
Rz Gates (public key — Euler phase shifts)
      │
      ▼
Rx Gates (secret signal embedding from Taylor series)
      │
      ▼
Encrypted Quantum State → Measurement (1024 shots)
      │
      ▼
Inverse QFT + Remove Taylor signal → Decrypted State
```

---

## 📁 Repository Structure

```
Quantum-Encryption-QFT-Taylor/
├── README.md
├── requirements.txt
├── src/
│   ├── ckks_encryption.py       # CKKS scheme with TenSEAL
│   ├── quantum_circuit.py       # QFT + gate-based encryption circuit
│   ├── taylor_keygen.py         # Taylor series private key generation
│   ├── homomorphic_inference.py # Encrypted model inference
│   └── evaluate.py              # Accuracy comparison: plaintext vs encrypted
├── notebooks/
│   └── Quantum_Encryption_Demo.ipynb
├── results/
│   ├── encrypted_state_distribution.png
│   ├── decrypted_state_distribution.png
│   └── classification_report.txt
├── images/
│   └── quantum_circuit_diagram.png
└── LICENSE
```

---

## ⚙️ Methods

### 1. CKKS Homomorphic Encryption

| Parameter | Value |
|-----------|-------|
| Scheme | CKKS (Cheon-Kim-Kim-Song) |
| Poly Modulus Degree | 8192 |
| Coeff Mod Bit Sizes | [60, 40, 40, 60] |
| Global Scale | 2^40 |
| Library | TenSEAL (Python) |

- Supports approximate arithmetic on encrypted real-valued data
- Galois keys generated for rotation operations
- Plaintext → polynomial encoding → encryption → homomorphic ops → decrypt

### 2. Proposed Quantum Encryption Scheme

| Component | Role |
|-----------|------|
| Ry Gates | Encode classical data into quantum states |
| QFT | Transform data into frequency domain |
| Rz Gates | Apply public key (Euler phase shifts) |
| Rx Gates | Embed Taylor series secret signal |
| Measurement | 1024 shots over basis states {|00⟩, |01⟩, |10⟩, |11⟩} |

### 3. Taylor Series Key Generation
The private key is derived from a Taylor expansion:
```
f(x) = Σ (f^n(a)/n!) * (x-a)^n
```
The function `f` and expansion terms are known only to the key holder. The generated signal is added to data before QFT transformation.

---

## 📊 Results

### CKKS Encrypted Inference — Diabetes Dataset

| Metric | Plaintext | Encrypted |
|--------|-----------|-----------|
| Accuracy (100 samples) | 97.00% | 97.00% |
| Accuracy (2000 samples) | **96.60%** | **96.60%** |

> Zero accuracy loss under homomorphic encryption — privacy-preserving inference confirmed.

### Classification Report (Logistic Regression on Encrypted Data)

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0 | 0.85 | 0.79 | 0.82 | 192 |
| 1 | 0.98 | 0.99 | 0.98 | 1808 |

### Quantum State Measurement (1024 shots)

| Quantum State | Decrypted | Encrypted |
|---------------|-----------|-----------|
| \|00⟩ | 277 | 246 |
| \|01⟩ | 251 | 255 |
| \|10⟩ | 236 | 246 |
| \|11⟩ | 260 | 277 |

> Near-uniform distributions confirm successful encryption. Decrypted distribution recovers original state.

---

## 🚀 Getting Started

```bash
pip install -r requirements.txt
```

### Run CKKS Encrypted Inference
```bash
python src/homomorphic_inference.py --dataset diabetes
```

### Run Quantum Circuit Demo
```bash
python src/quantum_circuit.py --shots 1024
```

### Evaluate Plaintext vs Encrypted Accuracy
```bash
python src/evaluate.py
```

---

## 📦 Requirements

```
tenseal==0.3.14
qiskit==0.44.1
numpy==1.24.3
scikit-learn==1.3.0
pandas==2.0.3
matplotlib==3.7.2
```

---

## 👥 Authors

| Name | Roll No. |
|------|----------|
| Hari Sudharsan G | CB.AI.U4AIM24113 |
| **Nithin S** | **CB.AI.U4AIM24133** |
| Amirthavarshini B | CB.AI.U4AIM24154 |
| Devadharshini M | CB.AI.U4AIM24126 |

Institution: Amrita Vishwa Vidyapeetham, Coimbatore

---

## 📚 Citation

```bibtex
@inproceedings{harisudharsan2024quantum,
  title     = {Quantum Encryption Scheme based on Taylor Series and Fourier Transform},
  author    = {Hari Sudharsan, G. and Nithin, S. and Amirthavarshini, B. and Devadharshini, M.},
  booktitle = {IEEE},
  year      = {2024},
  institution = {Amrita Vishwa Vidyapeetham, Coimbatore}
}
```

---

## 📜 References
1. Hong, C. Recent advances of privacy-preserving ML based on Homomorphic Encryption. *Security and Safety*, 2025.
2. Dutta et al. Federated Learning with Quantum Computing and FHE. *arXiv:2409.11430*, 2024.
3. Patel, M. Diabetes prediction dataset. *Kaggle*, 2025.

---

<div align="center">
📍 Amrita Vishwa Vidyapeetham, Coimbatore, Tamil Nadu &nbsp;|&nbsp; Published in IEEE
</div>
