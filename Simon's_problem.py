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
    fake_backend = FakeBrisbane()
    hardware_simulator = AerSimulator.from_backend(fake_backend)
    transpiled_qc = transpile(qc, backend = hardware_simulator)
    result = hardware_simulator.run(transpiled_qc, shots = n + 1024).result()
    statistics = result.get_counts()
    
    final_statistics = {}
    for key, value in statistics.items():
        measured = key[:n]
        final_statistics[measured] = value
    display(plot_histogram(final_statistics))
    #we take the n qubits with the highest counts, which for small n, with an addition
    #of 2024 shots will probably the correct string, even accounting for noise
    
    final_statistics = dict(sorted(final_statistics.items(), key = lambda item:item[1], reverse = True))
    first_n = dict(list(final_statistics.items())[:n])
    print(first_n)

    matrix = np.array([list(bitstring) for bitstring, count in first_n.items()]).astype(int)
    for i in range(len(matrix)):
        print(matrix[i])
    
    #Transpose the matrix and append the identity matrix
    matrix = Matrix(matrix).T
    augmented_matrix = Matrix(np.hstack([matrix, np.eye(matrix.shape[0], dtype = int)]))

    #Perform Gauss-Jordan elimination
    reduced_row = augmented_matrix.rref(iszerofunc=lambda x: x % 2 == 0)

    #Convert matrix
    final_result = np.array(reduced_row[0])
    final_result = np.mod(final_result, 2)

    if all(value == 0 for value in final_result[-1, :matrix.shape[1]]):
        result = "".join(str(c) for c in final_result[-1, matrix.shape[1]:])
    else:
        result = "0" * matrix.shape[0]
    print("Result is: ", result)

# %%
f = simon_query(5, "10101")
display(f.draw(output = "mpl"))
display(simon_problem(5, 5, f))

# %%

