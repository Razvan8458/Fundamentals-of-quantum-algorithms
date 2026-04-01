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
#Except for the different type of function
#and the different finishing output
#it uses the Deutch-Josza Algorithm
# %%
def bv_query(s):
    # Create a circuit implementing for a query gate for a random function
    # satisfying the promise for the Bernstein-Vazirani problem.

    qc = QuantumCircuit(len(s) + 1)
    #The function is created so that if the bit of the string s is 1
    #and the bit of the string x is 1, the last qubit is flipped, so the output
    #is the parity of the number of bits that s and x have in common that are 1
    #We achieve this by making a cnot gate from any bit from the string s that is 1
    #applied to the last qubit(the output qubit)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, len(s))
   

    return qc
# %%
display(bv_query("1110").draw(output = "mpl"))
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
def bv_problem(function: QuantumCircuit):

    qc = compile_circuit(function)

    result = AerSimulator().run(qc, shots = 1, memory = True).result()
    measurement = result.get_memory()
    return measurement[0]

# %%
f = bv_query("1100")
display(f.draw("mpl"))
display(bv_problem(f))
# %%
