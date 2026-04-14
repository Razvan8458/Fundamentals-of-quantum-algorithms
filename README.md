This is some code i wrote while following the course "Fundamentals of quantum algorithms" from ibm quantum learning

#Deutsch's algorithm

Implementation of Deutsch's algorithm for functions with two qubits as input

<img width="732" height="692" alt="image" src="https://github.com/user-attachments/assets/937d2382-b6aa-4378-a2a3-fd7e91ac05ff" />

#Deutsch-Josza-algorithm

Implementation of Deutsch-Josza's algorithm for functions with any number of qubits an input

<img width="1042" height="693" alt="image" src="https://github.com/user-attachments/assets/ded4fee9-1046-4029-9044-d66c81ad0baa" />

#Bernstein-Vazirani_problem

Implementation of the code solving Bernstein-Vazirani problem
It's pretty much using the Deutch-Josza algorithm, except it has a different type of function
and the classical post-processing is different

<img width="678" height="689" alt="image" src="https://github.com/user-attachments/assets/7c549884-ffca-40a9-a564-749d74a73fc0" />

<img width="489" height="479" alt="image" src="https://github.com/user-attachments/assets/a0e3c3c1-196f-4059-bde0-5755541e54c0" />

#Simon's problem

Implementation of code that solves Simon's problem for any function that fulfills the Simon's problem, even if the number of bits of the inputs
is different from the number of bits from the output
The code is ran on a simulation of a real quantum arhitecture from ibm, Brisbane

<img width="841" height="748" alt="image" src="https://github.com/user-attachments/assets/c4a7d6a8-b147-4b62-b440-0b0be1f22d0e" />

<img width="1032" height="656" alt="image" src="https://github.com/user-attachments/assets/42a0acb5-b1f8-4f27-afe9-6994b9229d7b" />

<img width="1044" height="482" alt="image" src="https://github.com/user-attachments/assets/e7112c9f-5f0b-4f86-b898-2f1e78408203" />

<img width="932" height="664" alt="image" src="https://github.com/user-attachments/assets/bc41eabb-c18a-429c-a20c-96f915b1c84f" />

#Phase factoring

Implementation of a code that solves Phase factoring using n qbits for precision of 1/(2^n)
It only uses 1 qubit for keeping the qubit that gets transformed by the function, because i only used it P gates, with a random angle.

In the photos we have the output for the code having 6 qbits for precision and P having the angle 2pi/9

<img width="1054" height="878" alt="image" src="https://github.com/user-attachments/assets/0db8f68d-dc6d-4570-bf56-aeb41281c77c" />

<img width="1007" height="709" alt="image" src="https://github.com/user-attachments/assets/a4b73714-98cb-47dc-a6dc-6f01c90ad8da" />

<img width="1006" height="667" alt="image" src="https://github.com/user-attachments/assets/8dc3c7b8-a0b2-4bad-be1b-24e3198c89d1" />

<img width="1047" height="853" alt="image" src="https://github.com/user-attachments/assets/18def8c7-cc44-4a6e-872c-3415f70571c2" />

<img width="288" height="79" alt="image" src="https://github.com/user-attachments/assets/7d41dac9-b04c-4ec1-95cd-07d4cc6b0dcc" />

#Quantum Fourier Transform

Implementation of a code that computes the circuit for QFT(2^n) in O(n^2) complexity, using recursivity
Here we have the circuit for QFT2, QFT4, QFT8, QFT16 and QFT32

<img width="1024" height="573" alt="image" src="https://github.com/user-attachments/assets/99cc972e-c349-48e9-9242-b9d4b3e84402" />

<img width="1055" height="901" alt="image" src="https://github.com/user-attachments/assets/57ebd33f-6bec-4a72-87ed-129425f87067" />

#Quantum adder

This is the implementation of a quantum adder, for positive numbers. It uses one ancilla qubit, and a total of 2 * n + 2 qubits, n being
the number of qubits the numbers are represented on. It uses 4 * n + 1 cx gate and 2 * n ccx gates. It also measures the qubits if you give it
the argument measure_qubits = True. In the program it also has a little code transforming the measurement into the number that is gained from
adding the two numbers.

-Calculation of the carry's:
  We calculate the carry-out for all the qubits
  This we get from two cx gates and one ccx gate
  We first apply the two cx gates, with the control qubit being the carry-in to the pair of qubits, one from
  each of the numbers we are adding.
  We then apply a ccx gate, with the controls being the two qubits to the carry-in, which makes it the carry-out
  We name a = value of the qubit from the first number at the beginning , b = value of qubit from the second number at the beginning
  and c = carry-in
  So the result in the carry-in, now carry-out is ab xor ac xor bc, which is 1 if at least two of the qubits are 1

  Analysis:
  q0 - qubit in which is stored the value of the qubit from the first number
  q1 - \..\ from the second number
  q2 - qubit where we store the carry-in value

  at the beginning the values are, q0 = a, q1 = b, q2 = c
  after the first two cx gates we have:
  q0 = a xor c
  q1 = b xor c
  after the ccx gate:
  q2 = c xor ((a xor c) * (b xor c))
  q2 = c xor (ab xor ac xor bc xor c)
  The xor operation is commutative ->
  q2 = ab xor ac xor bc
  If one of the values is 1, all the terms will be 0, so the result is 0 (0 xor 0 xor 0 = )
  If two of the values are 1, one of the terms will be 1, so the result is 1 ( 1 xor 0 xor 0 = 1)
  If three of the values are 1, all the terms will be 1, so the results is 1 ( 1 xor 1 xor 1 = 1)

<img width="1040" height="896" alt="image" src="https://github.com/user-attachments/assets/e22ebcb5-944d-45bb-9314-1fac3ea57740" />

<img width="1035" height="520" alt="image" src="https://github.com/user-attachments/assets/f190e88c-ac2f-42a5-ba13-7b037861b3c2" />









