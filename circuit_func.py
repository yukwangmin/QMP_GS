#!/usr/bin/env python
# coding: utf-8

#import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
#import math 
#from numpy import log as ln
#pi=math.pi
#import timeit
#from qiskit.tools.monitor import job_monitor
#from qiskit.providers.jobstatus import JobStatus

from qiskit import *






# sols : [Most Significant <-> Least Singnificant]
def oracle(circuit, q, size, sols : list) -> QuantumCircuit:
    for i in range(min(len(sols),size)):
        if sols[size-1-i] == 0:
            circuit.x(q[i])

    circuit.h(q[0])
    circuit.mct([q[i+1] for i in range(size-1)], q[0], None, mode='noancilla')
    circuit.h(q[0])

    for i in range(min(len(sols),size)):
        if sols[size-1-i] == 0:
            circuit.x(q[i])

    return circuit


# sols : [Most Significant <-> Least Singnificant]
def oracleCircuit(size, sols : list) -> QuantumCircuit:
    circuit = QuantumCircuit(size, name='Oracle')
    
    for i in range(min(len(sols),size)):
        if sols[size-1-i] == 0:
            circuit.x(i)

    circuit.h(0)
    circuit.mct([i+1 for i in range(size-1)], 0, None, mode='noancilla')
    circuit.h(0)

    for i in range(min(len(sols),size)):
        if sols[size-1-i] == 0:
            circuit.x(i)

    return circuit


# sols : [Most Significant <-> Least Singnificant]
def oracleTwoSolCircuit(size, sols1 : list, sols2 : list) -> QuantumCircuit:
    circuit = QuantumCircuit(size, name='Oracle')
    
    for i in range(min(len(sols1),size)):
        if sols1[size-1-i] == 0:
            circuit.x(i)

    circuit.h(0)
    circuit.mct([i+1 for i in range(size-1)], 0, None, mode='noancilla')
    circuit.h(0)

    for i in range(min(len(sols1),size)):
        if sols1[size-1-i] == 0:
            circuit.x(i)


    for i in range(min(len(sols2),size)):
        if sols2[size-1-i] == 0:
            circuit.x(i)

    circuit.h(0)
    circuit.mct([i+1 for i in range(size-1)], 0, None, mode='noancilla')
    circuit.h(0)

    for i in range(min(len(sols1),size)):
        if sols2[size-1-i] == 0:
            circuit.x(i)
            
    return circuit





# solution : [Most Significant <-> Least Singnificant]
# solutions : list of solutions
def oracleMultiSolCircuit(size, solutions : list) -> QuantumCircuit:
    circuit = QuantumCircuit(size, name='Oracle')

    for sol in solutions:
        
        if len(sol) != size:
            print(f'The solution length is {n}. But the size is {size}. They should be same!')
            return None;
        
        for i in range(min(len(sol),size)):
            if sol[size-1-i] == 0:
                circuit.x(i)

        circuit.h(0)
        circuit.mct([i+1 for i in range(size-1)], 0, None, mode='noancilla')
        circuit.h(0)

        for i in range(min(len(sol),size)):
            if sol[size-1-i] == 0:
                circuit.x(i)

            
    return circuit





# sols : [Most Significant <-> Least Singnificant]
def oracleDeviceCircuit(size, sols : list) -> QuantumCircuit:
    circuit = QuantumCircuit(size, name='Oracle')
    
    ctrled = 0
    ctrl = range(1, size)
    
    for i in range(min(len(sols),size)):
        if sols[size-1-i] == 0:
            circuit.x(i)

    if len(ctrl) == 2:
        circuit.h(0)
        CCX(circuit, ctrl[0], ctrl[1], ctrled)
        circuit.h(0)
    elif len(ctrl) == 3:
        C3P(circuit, pi, ctrl, ctrled)
    elif len(ctrl) == 4:
        C4P(circuit, pi, ctrl, ctrled)
    elif len(ctrl) == 5:
        C5P(circuit, pi, ctrl, ctrled)
        

    for i in range(min(len(sols),size)):
        if sols[size-1-i] == 0:
            circuit.x(i)

    return circuit






#
# I - 2 |s><s|
#
# 2 qubit case
# |  0.5 -0.5 -0.5 -0.5 |
# | -0.5  0.5 -0.5 -0.5 |
# | -0.5 -0.5  0.5 -0.5 |
# | -0.5 -0.5 -0.5  0.5 |
#
def diff(circuit, q, size, exclude = None) -> QuantumCircuit:
    ctrl = list(range(size))

    if exclude != None:
        for i in exclude:
            ctrl.remove(i)

    ctrled = min(ctrl)
    ctrl.remove(ctrled)

    addH(circuit,q, [i for i in ctrl])
    circuit.z(q[ctrled])

    for i in [i for i in ctrl]:
        circuit.x(q[i])

    circuit.mct([q[i] for i in ctrl], q[ctrled], None, mode='noancilla')

    for i in [i for i in ctrl]:
        circuit.x(q[i])

    circuit.z(q[ctrled])
    addH(circuit,q, [i for i in ctrl])


    return circuit

#
# I - 2 |s><s|
#
# 2 qubit case
# |  0.5 -0.5 -0.5 -0.5 |
# | -0.5  0.5 -0.5 -0.5 |
# | -0.5 -0.5  0.5 -0.5 |
# | -0.5 -0.5 -0.5  0.5 |
#
def diffCircuit(size, exclude = None) -> QuantumCircuit:
    circuit = QuantumCircuit(size, name='Diffusor')
                             
    ctrl = list(range(size))

    if exclude != None:
        for i in exclude:
            ctrl.remove(i)

    ctrled = min(ctrl)
    ctrl.remove(ctrled)

    for i in ctrl:
        circuit.h(i)
    circuit.z(ctrled)

    for i in [i for i in ctrl]:
        circuit.x(i)

    circuit.mct([i for i in ctrl], ctrled, None, mode='noancilla')

    for i in [i for i in ctrl]:
        circuit.x(i)

    circuit.z(ctrled)
    for i in ctrl:
        circuit.h(i)


    return circuit



#
# I - 2 |s><s|
#
# 2 qubit case
# |  0.5 -0.5 -0.5 -0.5 |
# | -0.5  0.5 -0.5 -0.5 |
# | -0.5 -0.5  0.5 -0.5 |
# | -0.5 -0.5 -0.5  0.5 |
#
def diffDeviceCircuit(size, exclude = None) -> QuantumCircuit:
    circuit = QuantumCircuit(size, name='Diffusor')
                             
    ctrl = list(range(size))

    if exclude != None:
        for i in exclude:
            ctrl.remove(i)

    ctrled = min(ctrl)
    ctrl.remove(ctrled)

    for i in ctrl:
        circuit.h(i)
    

    for i in [i for i in ctrl]:
        circuit.x(i)
    
    if len(ctrl) == 2:
        circuit.z(ctrled)
        CCX(circuit, ctrl[0], ctrl[1], ctrled)
        circuit.z(ctrled)
    elif len(ctrl) == 3:
        circuit.h(ctrled)
        circuit.x(ctrled)
        C3P(circuit, pi, ctrl, ctrled)
        circuit.x(ctrled)
        circuit.h(ctrled)
    elif len(ctrl) == 4:
        circuit.h(ctrled)
        circuit.x(ctrled)
        C4P(circuit, pi, ctrl, ctrled)
        circuit.x(ctrled)
        circuit.h(ctrled)
    elif len(ctrl) == 5:
        circuit.h(ctrled)
        circuit.x(ctrled)
        C5P(circuit, pi, ctrl, ctrled)
        circuit.x(ctrled)
        circuit.h(ctrled)
        
    

    for i in [i for i in ctrl]:
        circuit.x(i)

    
    for i in ctrl:
        circuit.h(i)


    return circuit



def addH(circuit, q, pos=None) -> QuantumCircuit:
    
    if pos == None:
        circuit.h(q)
    else:
        for i in pos:
            circuit.h(q[i])
            
def addX(circuit, q, pos=None) -> QuantumCircuit:
    
    if pos == None:
        circuit.x(q)
    else:
        for i in pos:
            circuit.x(q[i])
            
def initalX(circuit, q, pos, sols) -> QuantumCircuit:
    
    for i in range(len(pos)):
        
        if sols[i] == 1:
            
            circuit.x(q[pos[i]])
            
        else: continue
            

def ccz(circuit, q, pos) -> QuantumCircuit:
    
    #pos[0] and pos[1] are the controls.
    #pos[2] is the target.
    
    circuit.cx(q[pos[1]], q[pos[2]])
    circuit.tdg(q[pos[2]])
    circuit.cx(q[pos[0]], q[pos[2]])
    circuit.t(q[pos[2]])
    circuit.cx(q[pos[1]], q[pos[2]])
    circuit.tdg(q[pos[2]])
    circuit.cx(q[pos[0]], q[pos[2]])
    circuit.t(q[pos[1]])
    circuit.t(q[pos[2]])
    circuit.cx(q[pos[0]], q[pos[1]])
    circuit.h(q[pos[2]])
    circuit.t(q[pos[0]])
    circuit.tdg(q[pos[1]])
    circuit.cx(q[pos[0]], q[pos[1]])
    circuit.h(q[pos[2]])
    
    return circuit

def cccy(circuit, q, pos) -> QuantumCircuit:
    
    #pos[1] is the ancillar qubit and needs to have the connection to pos[0,2,3]
    
    circuit.h(pos[1])
    circuit.t(pos[1])
    circuit.cx(pos[0],pos[1])
    circuit.tdg(pos[1])
    circuit.h(pos[1])
    circuit.cx(pos[2],pos[1])
    circuit.t(pos[1])
    circuit.cx(pos[3],pos[1])
    circuit.tdg(pos[1])
    circuit.cx(pos[2],pos[1])
    circuit.t(pos[1])
    circuit.cx(pos[3],pos[1])
    circuit.tdg(pos[1])
    circuit.h(pos[1])
    circuit.t(pos[1])
    circuit.cx(pos[0],pos[1])
    circuit.tdg(pos[1])
    circuit.h(pos[1])
    
    return circuit

def cccy_dg(circuit, q, pos) -> QuantumCircuit:
    
    #pos[1] is the ancillar qubit and needs to have the connection to pos[0,2,3]
    
    circuit.h(pos[1])
    circuit.t(pos[1])
    circuit.cx(pos[0],pos[1])
    circuit.tdg(pos[1])
    circuit.h(pos[1])
    circuit.t(pos[1])
    circuit.cx(pos[3],pos[1])
    circuit.tdg(pos[1])
    circuit.cx(pos[2],pos[1])
    circuit.t(pos[1])
    circuit.cx(pos[3],pos[1])
    circuit.tdg(pos[1])
    circuit.cx(pos[2],pos[1])
    circuit.h(pos[1])
    circuit.t(pos[1])
    circuit.cx(pos[0],pos[1])
    circuit.tdg(pos[1])
    circuit.h(pos[1])
    
    return circuit

def ccy(circuit, q, pos) -> QuantumCircuit:
    
    #pos[0] and pos[1] are the control qubits; pos[2] is the target qubit.
    
    circuit.u3(pi/4,0,0,q[pos[2]])
    circuit.cx(q[pos[1]], q[pos[2]])
    circuit.u3(pi/4,0,0,q[pos[2]])
    circuit.cx(q[pos[0]], q[pos[2]])
    circuit.u3(-pi/4,0,0,q[pos[2]])
    circuit.cx(q[pos[1]], q[pos[2]])
    circuit.u3(-pi/4,0,0,q[pos[2]])
    
    return circuit
    
    
    
#Oracle operators
    

def oracle(circuit, q, pos, sols:list) -> QuantumCircuit:
    
    for i in range(len(sols)):
        
        if sols[i] == 2:
            
            continue
        
        elif sols[i] == 0:
            circuit.x(q[pos[i]])
            
    
    cccy(circuit, q, [pos[0],pos[1],pos[2],pos[3]])
    
    #circuit.swap(q[1],q[3])
    
    ccz(circuit, q, [pos[1],pos[4],pos[5]])
    
    #circuit.swap(q[1],q[3])
    
    cccy_dg(circuit, q, [pos[0],pos[1],pos[2],pos[3]])
    
    
    for i in range(len(sols)):
        
        if sols[i] == 2:
            
            continue
        
        elif sols[i] == 0:
            circuit.x(q[pos[i]])
    
    return circuit

def oracle_uncompute(circuit, q, pos, sols:list) -> QuantumCircuit:
    
    for i in range(len(sols)):
        
        if sols[i] == 2:
            
            continue
        
        elif sols[i] == 0:
            circuit.x(q[pos[i]])
            
    
    cccy(circuit, q, [pos[0],pos[1],pos[2],pos[3]])
    
    #circuit.swap(q[1],q[3])
    
    ccz(circuit, q, [pos[1],pos[4],pos[5]])
    
    
    for i in range(len(sols)):
        
        if sols[i] == 2:
            
            continue
        
        elif sols[i] == 0:
            circuit.x(q[pos[i]])
    
    return circuit



#Diffusion operators
    
    
def diffusion_5q(circuit, q, pos) -> QuantumCircuit:
    
    #pos[0,2,3,4,5] are working qubits.
    #pos[1] is the ancillary qubit.
    
    addH(circuit, q, [pos[0],pos[2],pos[3],pos[4],pos[5]])
    addX(circuit, q, [pos[0],pos[2],pos[3],pos[4],pos[5]])

    
    cccy(circuit, q, [pos[0],pos[1],pos[2],pos[3]])
    
    #circuit.swap(q[1],q[3])
    
    ccz(circuit, q, [pos[1],pos[4],pos[5]])
    
    #circuit.swap(q[1],q[3])
    
    cccy_dg(circuit, q, [pos[0],pos[1],pos[2],pos[3]])
    
    addX(circuit, q, [pos[0],pos[2],pos[3],pos[4],pos[5]])
    addH(circuit, q, [pos[0],pos[2],pos[3],pos[4],pos[5]])
    
    return circuit


def diffusion_3q(circuit, q, pos) -> QuantumCircuit:
    
    addH(circuit, q, pos)
    addX(circuit, q, pos)
    
    ccz(circuit, q, pos)
    
    addX(circuit, q, pos)
    addH(circuit, q, pos)
    
    return circuit


def diffusion_2q(circuit, q, pos) -> QuantumCircuit:
    
    addH(circuit, q, pos)
    addX(circuit, q, pos)
    
    circuit.cz(q[pos[0]],q[pos[1]])
    
    addX(circuit, q, pos)
    addH(circuit, q, pos)
    
    return circuit


#Circuits

def qc_D5M5(sol):

    q = QuantumRegister(6, 'q')
    c = ClassicalRegister(5, 'c')
    
    sol = np.insert(sol,1,2)

    qc = QuantumCircuit(q, c)  # 0 applications of Q, only a single A operator

    addH(qc, q, [0,2,3,4,5]) # Qubit 0,2,3,4 are the wroking qubits. Qubit 1 is the ancillary qubit.


    oracle(qc,q,[0,1,2,3,4,5],sol)


    diffusion_5q(qc, q, [0,1,2,3,4,5])


    qc.measure(q[0],c[0])
    qc.measure(q[2],c[1])
    qc.measure(q[3],c[2])
    qc.measure(q[4],c[3])
    qc.measure(q[5],c[4])
    
    #qc_trans = qiskit.transpile(qc, backend=trans_backend, optimization_level=3, initial_layout = trans_layout)
    
    return qc

def qc_D5D5M5(sol):

    q = QuantumRegister(6, 'q')
    c = ClassicalRegister(5, 'c')
    
    sol = np.insert(sol,1,2)

    qc = QuantumCircuit(q, c)  # 0 applications of Q, only a single A operator

    addH(qc, q, [0,2,3,4,5]) # Qubit 0,2,3,4 are the wroking qubits. Qubit 1 is the ancillary qubit.


    oracle(qc,q,[0,1,2,3,4,5],sol)


    diffusion_5q(qc, q, [0,1,2,3,4,5])
    
    oracle(qc,q,[0,1,2,3,4,5],sol)


    diffusion_5q(qc, q, [0,1,2,3,4,5])


    qc.measure(q[0],c[0])
    qc.measure(q[2],c[1])
    qc.measure(q[3],c[2])
    qc.measure(q[4],c[3])
    qc.measure(q[5],c[4])
    
    #qc_trans = qiskit.transpile(qc, backend=trans_backend, optimization_level=3, initial_layout = trans_layout)
    
    return qc


def qc_G3D2M2(sol):

    q = QuantumRegister(6, 'q')
    c = ClassicalRegister(2, 'c')
    
    qc = QuantumCircuit(q, c)

    guess_pos = [0,2,3]
    guess_sol = [sol[0],sol[1],sol[2]]

    search_pos =   [4,5]  

    addH(qc, q, search_pos)
    
    initalX(qc, q, guess_pos, guess_sol)
    
    sol = np.insert(sol,1,2)

    oracle_uncompute(qc,q,[0,1,2,3,4,5],sol)

    diffusion_2q(qc, q, [4,5])

    qc.measure(q[4],c[0])
    qc.measure(q[5],c[1])
    
    #qc_trans = qiskit.transpile(qc, backend=trans_backend, optimization_level=3, initial_layout = trans_layout)
    
    return qc
    

def qc_G2D3M3(sol, guess_sol = None) -> QuantumCircuit:

    q = QuantumRegister(6, 'q')
    c = ClassicalRegister(3, 'c')
    
    qc = QuantumCircuit(q, c)

    guess_pos = [0,2]
    if guess_sol == None:
        guess_sol = [sol[0],sol[1]]

    search_pos =   [3,4,5]  

    addH(qc, q, search_pos)
    
    initalX(qc, q, guess_pos, guess_sol)
    
    sol = np.insert(sol,1,2)

    oracle(qc,q,[0,1,2,3,4,5],sol)

    diffusion_3q(qc, q, [3,4,5])
    

    
    #qc_trans = qiskit.transpile(qc, backend=trans_backend, optimization_level=3, initial_layout = trans_layout)
    
    return qc
    

def qc_D3M3(sol):

    q = QuantumRegister(6, 'q')
    c = ClassicalRegister(3, 'c')
    
    qc = QuantumCircuit(q, c)
    
    #sol[0], sol[3] = sol[3], sol[0]
    #sol[1], sol[4] = sol[4], sol[1]


    search_pos =   [0,2,3,4,5]  

    addH(qc, q, search_pos)
    
    sol = np.insert(sol,1,2)

    oracle(qc,q,[0,1,2,3,4,5],sol)

    diffusion_3q(qc, q, [0,2,3])
    
    qc.measure(q[0],c[0])
    qc.measure(q[2],c[1])
    qc.measure(q[3],c[2])
    
    #qc_trans = qiskit.transpile(qc, backend=trans_backend, optimization_level=3, initial_layout = trans_layout)
    
    return qc


def qc_D2M2(sol):

    q = QuantumRegister(6, 'q')
    c = ClassicalRegister(2, 'c')
    
    qc = QuantumCircuit(q, c)
    
    sol[0], sol[3] = sol[3], sol[0]
    sol[1], sol[4] = sol[4], sol[1]

    search_pos =   [0,2,3,4,5]  

    addH(qc, q, search_pos)
    
    sol = np.insert(sol,1,2)

    oracle_uncompute(qc,q,[0,1,2,3,4,5],sol)

    diffusion_2q(qc, q, [4,5])

    qc.measure(q[4],c[0])
    qc.measure(q[5],c[1])
    
    #qc_trans = qiskit.transpile(qc, backend=trans_backend, optimization_level=3, initial_layout = trans_layout)
    
    return qc


#job generate

def job_generate(circuit,backend,n,shots):
    
    job = []
    
    for i in range(n):
        
        job.append(execute(circuit, backend, shots=shots))
        
    return job


def job_generate_monitor(circuit,backend,n,shots):
    
    jobs = []
    
    for i in range(n):
        job = backend.run(circuit, shots=shots)
        job_id = job.job_id()
        print("Job id", job_id)
        job_monitor(job)
        
        #while job.status() is not JobStatus.DONE:
        #    print("Job status is", job.status() )
        #    time.sleep(1)
        
        print(f'Job status is {job.status()} of Job ID: {job.job_id()}')
        
        if job.status() == JobStatus.DONE:
            jobs.append(job)
        else:
            jobs.append(None)
            
    return jobs


def count_generate(jobs):
    
    n = len(jobs)
    
    counts = []
    
    
    for i in range(n):
        
        result = jobs[i].result()
        counts.append(result.get_counts())
        
    return counts


#Data processing


def count_find(counts,find_targ):
    
    num = len(counts)
    
    #frequent = counts.most_frequent()
    
    counts = list(counts.items())
    
    #find_num = 0
    
    for i in range(num):
        
        if counts[i][0] == find_targ:
            
            find_num = counts[i][1]
            
        else: continue
            
    return find_num

def count_second_find(counts,find_targ):
    
    num = len(counts)
    
    #frequent = counts.most_frequent()
    
    counts = list(counts.items())
    
    new_list = []
    
    for i in range(num):
        
        if counts[i][0] == find_targ:
            
            continue
            
        else: new_list.append(counts[i][1])
    
    if len(new_list) == 0:
        
        return 0
    
    else: return max(new_list)
    
def out_prob(counts,shots,target):
    
    num = len(counts)
    
    prob = []
    
    second_prob = []
    
    for i in range(num):
        
        frequency = count_find(counts[i],target)
        
        second_frequency = count_second_find(counts[i],target)
        
        prob.append(frequency/shots)
        
        second_prob.append(second_frequency/shots)
        
    return [prob,second_prob]