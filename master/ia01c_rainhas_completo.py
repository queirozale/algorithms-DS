# -*- coding: utf-8 -*-
"""
Codigo baseado no fornecido pelo Prof. Fabrício Olivetti: https://folivetti.github.io/teaching/

"""
from time import time
import random
import numpy as np

def numero_ataques(sol):
    if len(sol) == 0:
        return 0
    ataques = [s for i, s in enumerate(sol[1:]) 
               if s == sol[0] 
               or s == sol[0] + i + 1 
               or s == sol[0] - i - 1]
    
    return len(ataques) + numero_ataques(sol[1:])

def next_idx(i,j):
    j = j%8 + 1
    i = i if j>1 else i+1
    return i, j
    
def gera_vizinho(v, i, j):
    while v[i] == j:
        i, j = next_idx(i,j)
    
    v[i] = j
    i, j = next_idx(i,j)     
    
    return v, i, j
    
def vizinhanca(sol):
    vizinhos = (sol.copy() for _ in range(8*7))
    i, j = 0, 1
    
    for v in vizinhos:
        vi, i, j = gera_vizinho(v, i, j)
        yield vi

def HillClimbing(s):
    mudou = True
    n_lateral = 0
    while mudou:
        mudou = False
        vizinhos = [v for v in vizinhanca(s)]
        n_ataques = numero_ataques(s)
        for vizinho in vizinhos:
            n_ataques_v = numero_ataques(vizinho)
            if n_ataques_v == n_ataques and n_lateral < 100:
                n_ataques = n_ataques_v
                s = vizinho
                mudou = True
                n_lateral += 1
            if n_ataques_v < n_ataques:
                n_ataques = n_ataques_v
                s = vizinho
                mudou = True
                n_lateral = 0
    return s


def SimulatedAnnealing(s):
    temp = 10000
    while temp > 0.00001:
        vizinhos = [v for v in vizinhanca(s)]
        v_i = random.randint(0, len(vizinhos) - 1)

        n_ataques = numero_ataques(s)
        n_ataques_v = numero_ataques(vizinhos[v_i])
        if (n_ataques_v < n_ataques) or (random.random() < np.math.exp((n_ataques - n_ataques_v) / temp)):
            s = vizinhos[v_i]
        temp = temp * 0.99
    return s

def Testa(Funcao):
    erros=0
    sucessos=0
    for _ in range(100):
        s0 = list(np.random.randint(1,9, size=8))
        s = Funcao(s0)
        if numero_ataques(s) == 0:
            sucessos += 1
        else:
            erros += 1
    print("Erros=", erros, "Sucessos=", sucessos)

inicio = time()
Testa(HillClimbing)
print("Tempo HillClimbing:", time() - inicio)

inicio = time()
Testa(SimulatedAnnealing)
print("Tempo SimulatedAnnealing:", time() - inicio)