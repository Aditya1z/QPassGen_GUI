# qpassgen_engine.py

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import random
import string
import matplotlib.pyplot as plt

def generate_password_info():
    qc = QuantumCircuit(4)
    qc.h(range(4))
    qc.measure_all()

    simulator = AerSimulator()
    result = simulator.run(qc, shots=100).result()
    counts = result.get_counts()

    sorted_bits = sorted(counts.items(), key=lambda x: -x[1])
    binary_password = sorted_bits[0][0]
    seed = int(binary_password, 2)
    random.seed(seed)

    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(chars, k=12))

    # Analysis
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    char_space = (26 * has_upper) + (26 * has_lower) + (10 * has_digit) + (32 * has_special)
    entropy = length * np.log2(char_space) if char_space else 0
    years = (2**entropy) / (1_000_000_000 * 365 * 24 * 60 * 60)

    return {
        "password": password,
        "entropy": entropy,
        "crack_time": years,
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "counts": counts
    }

def show_distribution(counts):
    plt.figure(figsize=(8, 6))
    plt.bar(counts.keys(), counts.values(), color='blue', alpha=0.7)
    plt.title('Quantum States Distribution')
    plt.xlabel('States')
    plt.ylabel('Counts')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
