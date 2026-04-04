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
from qiskit.circuit.library import QFT
# %%
def angle_query():
    
    factor = random.randint(1, 20)
    angle = 2*pi / factor
    return angle

# %%
def compile_circuit(angle, num_qubits):

    qc = QuantumCircuit(num_qubits +  1, num_qubits)

    qc.h(range(0, num_qubits))
    qc.x(num_qubits)
    qc.barrier()

    number_of_gates = 1
    for i in range(0, num_qubits):
        for j in range(number_of_gates):
            qc.cp(angle, i, num_qubits)
        qc.barrier()
        number_of_gates *= 2
    
    qc = qc.compose(QFT(num_qubits, inverse = True), range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))
    return qc
# %%
def phase_factoring(num_qubits):

    angle = angle_query()
    print("The phase is: ")
    display(angle / (2 * pi))
    qc = compile_circuit(angle, num_qubits)
    print("The circuit is: ")
    display(qc.draw(output = "mpl"))

    fake_backend = FakeBrisbane()
    hardware_simulator = AerSimulator.from_backend(fake_backend)
    transpiled_qc = transpile(qc, backend = hardware_simulator)
    result = hardware_simulator.run(transpiled_qc, shots = 128).result()
    statistics = result.get_counts()
    display(plot_histogram(statistics))
    max_key = max(statistics, key = lambda k: statistics[k])
    print("The answer we found: ")
    value_found = float(int(max_key, 2)) / (2**num_qubits)
    print(value_found)

# %%
phase_factoring(6)
# %%
