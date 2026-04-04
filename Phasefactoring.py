#%%
from qiskit import transpile
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, array_to_latex
from qiskit.result import marginal_distribution
from qiskit.circuit.library import UGate
from math import pi
import random
from qiskit_aer import AerSimulator
import numpy as np
from qiskit_ibm_runtime.fake_provider import FakeBrisbane
from sympy import Matrix
# %%
def angle_query():
    
    factor1 = random.randint(1, 1000)
    factor2 = random.randint(1, 1000)
    angle = 2*pi*factor1/factor2
    return angle

# %%
def compile_circuit(angle, num_qubits):

    qc = QuantumCircuit(num_qubits +  1, num_qubits)