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
def quantum_fourier(n):

    if n == 1:
        #The Quantum Fourier Matrix for QFT2 is H
        qc = QuantumCircuit(1)
        qc.h(0)
        return qc
    

    #We recursively get the Quantum Fourier Circuit for QFT(2^(n-1))
    function = quantum_fourier(n - 1)
    display(function.draw(output = "mpl"))
    qc = QuantumCircuit(n)
    qc.compose(function, range(1, n), inplace = True)
    qc.barrier()

    angle = pi / (2**(n-1))
    for i in range(1, n):
        qc.cp(angle, 0, i)
        angle *= 2
    qc.barrier()

    qc.h(0)
    qc.barrier()

    qc.swap(0, n - 1)
    for i in range(0, n - 2):
        qc.swap(i, i + 1)

    return qc


# %%
display(quantum_fourier(5).draw(output = "mpl"))
# %%
