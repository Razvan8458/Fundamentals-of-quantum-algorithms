#%%
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, array_to_latex
from qiskit.result import marginal_distribution
from qiskit.circuit.library import UGate
from math import pi
import random
from qiskit_aer import AerSimulator
import numpy as np
# %%
def dj_query(num_qubits):
    # Create a circuit implementing for a query gate for a random function
    # satisfying the promise for the Deutsch-Jozsa problem.

    qc = QuantumCircuit(num_qubits + 1)

    if np.random.randint(0, 2):
        # Flip output qubit with 50% chance
        qc.x(num_qubits)
    if np.random.randint(0, 2):
        # return constant circuit with 50% chance
        print("it's constant")
        return qc
    print ("it's balanced")
    # Choose half the possible input strings
    on_states = np.random.choice(
        range(2**num_qubits),  # numbers to sample from
        2**num_qubits // 2,  # number of samples
        replace=False,  # makes sure states are only sampled once
    )

    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc

    for state in on_states:
        qc.barrier()  # Barriers are added to help visualize how the functions are created.
        qc = add_cx(qc, f"{state:0b}")
        qc.mcx(list(range(num_qubits)), num_qubits)
        qc = add_cx(qc, f"{state:0b}")

    qc.barrier()

    return qc
# %%
def compile_circuit(function: QuantumCircuit):

    n = function.num_qubits

    qc = QuantumCircuit(n, n - 1)

    qc.x(n - 1)
    qc.h(range(n))
    qc.barrier()

    qc.compose(function, inplace = True)
    qc.barrier()

    qc.h(range(n - 1))
    qc.measure(range(n - 1), range(n - 1))

    return qc
# %%
def dj_algorithm(function: QuantumCircuit):

    qc = compile_circuit(function)

    result = AerSimulator().run(qc, shots = 1, memory = True).result()
    measurement = result.get_memory()
    if "1" in measurement[0]:
        return "balanced"
    return "constant"

# %%
f = dj_query(3)
display(f.draw("mpl"))
display(dj_algorithm(f))
# %%
