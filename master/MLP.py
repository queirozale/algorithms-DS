#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random 
import math
import matplotlib.pyplot as plt


# In[3]:


class Neuronio:
    def __init__(self, n_entradas):
        self.b = random.random() - 0.5
        self.w = [random.random() - 0.5 for _ in range(n_entradas)]
        
    def funcao_ativacao(self, u):
        try:
            y = 1.0 / (1.0 + math.exp(-u))
        except OverflowError:
            y = 1.0 / (1.0 + math.inf)
            
        return y

    def saida(self, entradas):
        u = self.b
        for i in range(len(entradas)):
            u += entradas[i] * self.w[i]
            
        return self.funcao_ativacao(u)


# In[5]:


class MLP():
    def __init__(self, n_entradas, n_oculta, n_saida):
        self.camada_oculta = [Neuronio(n_entradas) for _ in range(n_oculta)]
        self.camada_saida = [Neuronio(n_oculta) for _ in range(n_saida)]
        
    def testar(self, exemplo):
        y_h = [n.saida(exemplo) for n in self.camada_oculta]
        y_s = [n.saida(y_h) for n in self.camada_saida]
        
        return y_s
        
        
    def treinar(self, treino_entradas, treino_saidas, eta):
        erro = 1
        erros = []
        while erro > 0.001:
            erro = 0
            
            for ex_index in range(len(treino_entradas)):
                # exemplo
                entrada = treino_entradas[ex_index]
                saida = treino_saidas[ex_index]
                
                # calcular saída
                y_h = [n.saida(entrada) for n in self.camada_oculta]
                y_s = [n.saida(y_h) for n in self.camada_saida]
                
                # calcula erro
                erro_neuronios = []
                erro_medio = 0.0
                for k in range(len(y_s)):
                    erro_neuronio = saida[k] - y_s[k]
                    erro_neuronios.append(erro_neuronio)
                    erro_medio += erro_neuronio ** 2
                    
                erro_medio = 0.5 * erro_medio
                erro += erro_medio
                
                # calcular deltas
                delta_s = []
                for k in range(len(self.camada_saida)):
                    delta_neuronio = erro_neuronios[k] * y_s[k] * (1 - y_s[k])
                    delta_s.append(delta_neuronio)
                
                delta_h = []
                for j in range(len(self.camada_oculta)):
                    delta_neuronio = y_h[j] * (1.0 - y_h[j])
                    soma = 0.0
                    for k in range(len(self.camada_saida)):
                        soma += delta_s[k] * self.camada_saida[k].w[j]
                        
                    delta_neuronio = delta_neuronio * soma
                    delta_h.append(delta_neuronio)
                    
                for k in range(len(self.camada_saida)):
                    self.camada_saida[k].b += eta * delta_s[k]
                    for j in range(len(self.camada_saida[k].w)):
                        self.camada_saida[k].w[j] += eta * delta_s[k] * y_h[j]
                        
                for j in range(len(self.camada_oculta)):
                    self.camada_oculta[j].b += eta * delta_h[j]
                    for i in range(len(self.camada_oculta[j].w)):
                        self.camada_oculta[j].w[i] += eta * delta_h[j] * entrada[i]
                
            print(erro)
            erros.append(erro)

        plt.plot(erros)



