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
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
#%%
def permute_query(n, m, qc):
    for i in range(n, n+m):
        for j in range(i + 1, n+m):
            #swap the i and j qbits (qbits from the second register) with a 50% chance
            if random.randint(1, 2) == 1:
                qc.swap(i, j)
    for i in range(n, n+m):
        #flip the i qbit (qbit from the second register) with a 50% chacne
        if random.randint(1, 2) == 1:
            qc.x(i)
    return qc
# %%
def simon_query(m, s):
    n = len(s)
    qc = QuantumCircuit(n + m)
    #We make the function that transform the string x
    #in the string x0....0
    for i in range(n):
        qc.cx(i, i + n)
    
    #We make f(x xor s) = f(x)
    s = s[::-1]

    if "1" not in s:
        #s is the 0^n string
        return permute_query(qc, n ,m)
    
    i = s.find('1')
    #we find the first qubit that is a 1
    #we can separate x from x xor s by the fact 
    #that they will have a different qubit in the places where
    #s has a 1
    #so to get f(x) = f(x xor s), we flip every qbit that has a 1 in
    #the writing of s, if one of the qubits that have 1 in the writing of s
    #also are 1 in the writing of x
    #in this case we choose the first qubit that has 1
    #example: s = 1101, x = 0001
    # f(x) = 0001
    # x xor s is 1100
    # we flip the qubits 0, 2, 3
    #so f(x xor s) = f(1100) = 0001

    for q in range(n):
        if s[q] == '1':
            qc.cx(i, q + n)
    
    #Now we switch some of the qubits from the second register
    #and flip some of them
    #it will still keep the property of f(x) = f(x xor s), but the
    #value of f(x) wont be x anymore but a random string

    return permute_query(n, m, qc)



    
# %%
display(simon_query(3, "101").draw(output = "mpl"))
# %%
def compile_circuit(n, m, function: QuantumCircuit):

    qc = QuantumCircuit(n + m, n)
    
    qc.h(range(n))
    qc.barrier()

    qc.compose(function, inplace = True)
    qc.barrier()

    qc.h(range(n))
    qc.measure(range(n), range(n))
    display(qc.draw(output = "mpl"))
    return qc

# %%
def simon_problem(n, m, function: QuantumCircuit):

    qc = compile_circuit(n, m, function)
    fake_backend = FakeManilaV2()
    hardware_simulator = AerSimulator.from_backend(fake_backend)
    transpiled_qc = transpile(qc, backend = hardware_simulator)
    result = hardware_simulator.run(transpiled_qc, shots = n + 15).result()
    statistics = result.get_counts()
    display(plot_histogram(statistics))
# %%
f = simon_query(2, "11")
display(f.draw(output = "mpl"))
display(simon_problem(2, 2, f))

# %%
