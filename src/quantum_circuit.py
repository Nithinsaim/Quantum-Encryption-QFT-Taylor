"""
quantum_circuit.py
Quantum Encryption using QFT + Taylor Series + Quantum Gates
Circuit: Ry (encode) → QFT → Rz (public key) → Rx (secret signal)
"""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def taylor_signal(x, n_terms=5, secret_a=0.5):
    """Generate secret signal from Taylor expansion of e^x around a."""
    result = 0.0
    for n in range(n_terms):
        result += (np.exp(secret_a) / np.math.factorial(n)) * (x - secret_a)**n
    return result

def build_encryption_circuit(data: np.ndarray, public_key: np.ndarray,
                               secret_fn=taylor_signal, n_qubits=2):
    qc = QuantumCircuit(n_qubits, n_qubits)
    # Step 1: Encode data with Ry gates
    for i, val in enumerate(data[:n_qubits]):
        qc.ry(float(val), i)
    # Step 2: QFT
    qc.h(0)
    qc.cp(np.pi/2, 0, 1)
    qc.h(1)
    qc.swap(0, 1)
    # Step 3: Public key — Rz gates (Euler phase shifts)
    for i, phi in enumerate(public_key[:n_qubits]):
        qc.rz(float(phi), i)
    # Step 4: Secret signal — Rx gates (Taylor series)
    for i, val in enumerate(data[:n_qubits]):
        alpha = secret_fn(val)
        qc.rx(float(alpha), i)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def build_decryption_circuit(data, public_key, secret_fn=taylor_signal, n_qubits=2):
    qc = QuantumCircuit(n_qubits, n_qubits)
    for i, val in enumerate(data[:n_qubits]):
        qc.ry(float(val), i)
    # Inverse Rx (remove secret signal)
    for i, val in enumerate(data[:n_qubits]):
        alpha = secret_fn(val)
        qc.rx(-float(alpha), i)
    # Inverse Rz (remove public key)
    for i, phi in enumerate(public_key[:n_qubits]):
        qc.rz(-float(phi), i)
    # Inverse QFT
    qc.swap(0, 1)
    qc.h(1)
    qc.cp(-np.pi/2, 0, 1)
    qc.h(0)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def run_circuit(qc, shots=1024):
    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled, shots=shots).result()
    return result.get_counts()

if __name__ == '__main__':
    data = np.array([np.pi/4, np.pi/3])
    pub_key = np.array([np.pi/6, np.pi/5])
    enc_qc = build_encryption_circuit(data, pub_key)
    dec_qc = build_decryption_circuit(data, pub_key)
    enc_counts = run_circuit(enc_qc, shots=1024)
    dec_counts = run_circuit(dec_qc, shots=1024)
    print("Encrypted State:", enc_counts)
    print("Decrypted State:", dec_counts)
