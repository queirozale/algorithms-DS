# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:50:00 2020

@author: paulo.pisani
"""

import pandas as pd

class KNN():
    def __init__(self, ds_treino):
        self.ds_treino = ds_treino
        
    def distancia(self, exemplo, referencia):
        soma = 0.0
        for i in range(len(exemplo)):
            soma += (exemplo[i] - referencia[i]) ** 2
        return soma ** 0.5
        
    def teste(self, exemplo, k = 3):
        dist = []
        for i in range(len(self.ds_treino)):
            tmp = self.distancia(exemplo,
                        self.ds_treino.iloc[i].values)
            dist.append(tmp)
           
        self.ds_treino[5] = dist
        ord = self.ds_treino.sort_values(by=[5])
        ord = ord[:k]
        return ord[4].value_counts().index[0]

ds = pd.read_csv("iris.data", sep=',', header=None)


ds_treino = ds.sample(100)
ds_teste = ds.drop(ds_treino.index)

modelo = KNN(ds_treino)

acertos = 0
erros = 0
for i in range(len(ds_teste)):
    exemplo = ds_teste.iloc[i].values[:4]
    rotulo_verd = ds_teste.iloc[i].values[4]
    rotulo_pred = modelo.teste(exemplo, k=3)
    if rotulo_verd == rotulo_pred:
        acertos += 1
    else:
        erros += 1
        
print("Acertos =", acertos, " Erros =", erros)


    
    
    