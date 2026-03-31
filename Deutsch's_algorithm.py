#%%
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, array_to_latex
from qiskit.result import marginal_distribution
from qiskit.circuit.library import UGate
from math import pi
import random
from qiskit_aer import AerSimulator
# %%
def deutsch_function(case: int):
    # generates the 4 possible functions
    # using a quantum circuit

    if case not in [1, 2, 3 ,4]:
        raise ValueError("case must be 1, 2, 3 or 4")
    
    f = QuantumCircuit(2)

    if case in [2, 3]:
        f.cx(0, 1)
    if case in [3, 4]:
        f.x(1)
    return f
# %%
def compile_circuit(function: QuantumCircuit):

    qc = QuantumCircuit(2, 1)

    qc.x(1)
    qc.h([0, 1])
    qc.barrier()

    qc.compose(function, inplace = True)
    qc.barrier()

    qc.h(0)
    qc.measure(0, 0)

    return qc
# %%
display(compile_circuit(deutsch_function(2)).draw(output = "mpl"))
# %%
def deutsch_algorithm(function: QuantumCircuit):

    qc = compile_circuit(function)

    result = AerSimulator().run(qc, shots = 1, memory = True).result()
    measurement = result.get_memory()
    if measurement[0] == "0":
        return "constant"
    return "balanced"

# %%
function_case = random.randint(1, 4)
print(function_case)
f = deutsch_function(function_case)
display(deutsch_algorithm(f))
# %%
