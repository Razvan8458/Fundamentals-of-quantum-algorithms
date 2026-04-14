#%%
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
# %%
def build_adder(n, a, b):

    qc = QuantumCircuit(2 * n + 2, n + 1)

    #The first n qubits represent the first number, the next n qubits the second number
    #After that, the last two qubits are:
    #One representing a carry bit, to hold the qubit, that can overflow from the addition of the numbers
    #and the last one being an ancilla qubit, meant to hold the temporary carry between qubits

    binary_string = f'{a:0{n}b}'
    for index, bit in enumerate(reversed(binary_string)):
        if bit == "1":
            qc.x(index)
    binary_string = f'{b:0{n}b}'
    for index, bit in enumerate(reversed(binary_string)):
        if bit == "1":
            qc.x(n + index)

    
    #We first calculate the carry's
    for i in range(n):
        #For each step we have a carry-in qubit, and two qubits we wish to add
        #Here we are only calculating the carry for the next pair of qubits
        #The carry-in is the ancilla qubit, and it is also where the carry-out is calculated
        #To calculate the carry, we apply two cx gates and one ccx gate
        #The cx gates are controlled by the carry-in bit, and modify each of the qubits we add
        #The ccx is controlled by the two qubits, and modify the carry-in / now the carry-out qubit
        #Mathematically, this results in ab xor ac xor bc, which is 1 if at least two of the three
        #qubits are 1 (a = qubit from first number, b = qubit from second number, c = carry_in)

        qc.cx(2 * n + 1, i)
        qc.cx(2 * n + 1, n + i)
        qc.ccx(i, n + i, 2 * n + 1)
        qc.barrier()
    
    qc.barrier()
    #We now entagle the state of the ancilliary qubit with the last carry-out qubit
    #in the case of computation basis states, it copies the qubit
    qc.cx(2 * n + 1, 2 * n)

    qc.barrier()
    qc.barrier()

    #We now uncompute the ancilliary qubit, and a part of the operation, and make the finishing calculations
    for i in range(n - 1, -1, -1):
        #Uncomputing the carry qubit
        qc.ccx(i, n + i, 2 * n + 1)
        #Turning the first number to its origin
        qc.cx(2 * n + 1, i)
        #Making the final calculation (in the second number, we dont undo this cx, because it is part of the calculation)
        qc.cx(i, n + i)
        #The qubit becomes a xor b xor c (a = qubit from first number, b = qubit from second number, c = carry_in)
        #Which makes the qubit 1 only if the number of qubits equal to 1 are an odd number
        qc.barrier()


    qc.measure(range(n, 2 * n + 1), range(n + 1))
    
    # The result of the calculation is in the qubits of the second number
    # plus the carry bit we had 

    return qc


    


# %%

display(build_adder(5, 10, 20).draw(output = "mpl"))

# %%
num_qubits = 7
a = 3
b = 5
print("The number of qubits is:", num_qubits)
print("The two numbers are:", a, b)
qc = build_adder(num_qubits, a, b)
display(qc.draw(output = "mpl"))
result = AerSimulator().run(qc, shots = 1, memory = True).result()
measurement = result.get_memory()
print(measurement)
number = 0
for index, bit in enumerate(reversed(measurement[0])):
    if bit == '1':
        number = number + 2**index
print("The result is:", number)


# %%
