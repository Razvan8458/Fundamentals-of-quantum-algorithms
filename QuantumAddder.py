#%%
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
# %%
def build_adder(n, a, b):

    qc = QuantumCircuit(2 * n + 2, n + 1)

    #The first n qubits represent the first number, the next n qubits the second number
    #and the last 2 qubits are auxiliary qubits

    binary_string = f'{a:0{n}b}'
    for index, bit in enumerate(reversed(binary_string)):
        if bit == "1":
            qc.x(index)
    binary_string = f'{b:0{n}b}'
    for index, bit in enumerate(reversed(binary_string)):
        if bit == "1":
            qc.x(n + index)

    switch = 0
    #This variable helps with switching between using the first and second auxiliary qubits

    for i in range(n):

        #We make the auxiliary qubit carry the "and" between the two qubits we are adding
        #making the auxiliary qubit the carry bit
        qc.ccx(i, i + n, 2 * n + switch)

        #We prepare the next carry bit, for the next pair of qubits, in the other auxiliary qubit
        if i != n - 1: 
            qc.ccx(n + i + 1, 2 * n + switch, 2 * n + (1 - switch))

        #We add the current carry bit, to the second pair of qubits
        if i != n - 1:
            qc.cx(2 * n + switch, n + i + 1)

        #We uncompute the current carry bit
        if i != n - 1:
            qc.ccx(i, i + n, 2 * n + switch)

        #We add the two qubits toghether
        qc.cx(i, n + i)

        #We reverse the switch

        switch = 1 - switch

        qc.barrier()
    
    qc.measure(range(n, 2 * n), range(n))

    qc.measure(2 * n + (1 - switch), n)
    
    # The result of the calculation is in the qubits of the second number
    # plus the carry bit we had 

    return qc


    


# %%

display(build_adder(3, 2, 3).draw(output = "mpl"))

# %%
num_qubits = 3
a = 7
b = 5
print("The number of qubits is: ", num_qubits)
print("The two numbers are: ", a, b)
qc = build_adder(num_qubits, a, b)
display(qc.draw(output = "mpl"))
result = AerSimulator().run(qc, shots = 1, memory = True).result()
measurement = result.get_memory()
number = 0
for index, bit in enumerate(reversed(measurement[0])):
    if bit == '1':
        number = number + 2**index
print("The result is: ", number)


# %%
