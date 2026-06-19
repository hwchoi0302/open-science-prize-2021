from qiskit.circuit.random import random_circuit

from isl.recompilers import ISLRecompiler, ISLConfig
from qiskit import QuantumCircuit, transpile
import numpy as np

# Setup the circuit
from isl.utils.entanglement_measures import EM_TOMOGRAPHY_CONCURRENCE

qc = random_circuit(5, 5, seed=2)

# Recompile
config = ISLConfig(sufficient_cost=1e-3, max_2q_gates=25)
recompilers = [ISLRecompiler(qc, entanglement_measure='EM_TOMOGRAPHY_CONCURRENCE', isl_config=config) for _ in range(10)]
results = [recompiler.recompile() for recompiler in recompilers]
recompiled_circuits = [result['circuit'] for result in results]

# See the original circuit
print(qc)

# See the recompiled solution
# print(recompiled_circuit)

# Transpile the original circuits to the common basis set
qc_in_basis_gates = transpile(qc, basis_gates=['u1', 'u2', 'u3', 'cx'], optimization_level=3)
print(qc_in_basis_gates.count_ops())
print(qc_in_basis_gates.depth())

# Compare with recompiled circuit
print(np.mean([recompiled_circuit.count_ops().get('cx', 0) for recompiled_circuit in recompiled_circuits]))
print(np.mean([recompiled_circuit.count_ops().get('u1', 0) for recompiled_circuit in recompiled_circuits]))
print(np.mean([recompiled_circuit.count_ops().get('u2', 0) for recompiled_circuit in recompiled_circuits]))
print(np.mean([recompiled_circuit.count_ops().get('u3', 0) for recompiled_circuit in recompiled_circuits]))
print(np.std([recompiled_circuit.count_ops().get('cx', 0) for recompiled_circuit in recompiled_circuits]))
print(np.mean([recompiled_circuit.depth() for recompiled_circuit in recompiled_circuits]))
print(np.std([recompiled_circuit.depth() for recompiled_circuit in recompiled_circuits]))

