import random
import numpy as np
import matplotlib.pyplot as plt


class Maze:
    def __init__(self, maze_map, inicio, objetivo):
        self.maze_map = maze_map
        self.inicio = inicio
        self.objetivo = objetivo
        self.movimentos = ["UP", "DOWN", "LEFT", "RIGHT"]
        
    def move(self, posicao, movimento):
        mov = {"NONE":[0,0], "UP":[-1,0], "DOWN":[1,0], "LEFT":[0,-1], "RIGHT":[0,1]}
        nova_posicao = [sum(x) for x in zip(posicao, mov[movimento])]
        if nova_posicao[0] < 0 or nova_posicao[0] >= len(self.maze_map) or nova_posicao[1] < 0 or nova_posicao[1] >= len(self.maze_map[0]):
            return None # Retorna None se o movimento for inválido
        if self.maze_map[nova_posicao[0]][nova_posicao[1]] == 0:
            return nova_posicao
        else:
            return None # Retorna None se o movimento for inválido

class Cromossomo():
    def __init__(self, mapa):
        self.mapa = mapa
        self.genes = np.random.choice(mapa.movimentos, size=50)
        self.avalia()
        
    def avalia(self):
        atual = self.mapa.inicio
        qtd_mov = 0
        for gene in self.genes:
            if atual == self.mapa.objetivo:
                break
            qtd_mov += 1
            prox = self.mapa.move(atual, gene)
            if prox is not None:
                atual = prox
        dist = (atual[0] - self.mapa.objetivo[0]) ** 2
        dist += (atual[1] - self.mapa.objetivo[1]) ** 2
        dist = dist ** 0.5
        self.fitness = dist + qtd_mov
    
def avalia_todos(populacao):
    for cromossomo in populacao:
        cromossomo.avalia()
        
def seleciona(populacao):
    pais = []
    for _ in range(len(populacao)):
        c1 = np.random.choice(populacao)
        c2 = np.random.choice(populacao)
        pai = c1 if c1.fitness < c2.fitness else c2
        pais.append(pai)
    return pais

def crossover(p1, p2):
    f1 = Cromossomo(p1.mapa)
    f2 = Cromossomo(p1.mapa)
    pt_corte = random.randint(0, len(p1.genes)-1)
    
    f1.genes[:pt_corte] = p1.genes[:pt_corte]
    f1.genes[pt_corte:] = p2.genes[pt_corte:]
    
    f2.genes[:pt_corte] = p2.genes[:pt_corte]
    f2.genes[pt_corte:] = p1.genes[pt_corte:]
    
    return f1, f2

def mutacao(filho):
    if random.random() < 0.5:
        idx = random.randint(0, len(filho.genes)-1)
        filho.genes[idx] = np.random.choice(filho.mapa.movimentos)
    return filho

def operacoes_geneticas(pais):
    filhos = []
    for i in range(0, len(pais) // 2):
        p1 = pais[2*i]
        p2 = pais[2*i + 1]
        f1, f2 = crossover(p1, p2)
        f1 = mutacao(f1)
        f2 = mutacao(f2)
        filhos.append(f1)
        filhos.append(f2)
    return filhos

def melhor_cromossomo(populacao):
    populacao.sort(key = lambda x : x.fitness)
    return populacao[0]

def GA(maze, n_populacao, n_geracoes):
    populacao = [Cromossomo(maze) for _ in range(n_populacao)]
    hist_fitness = []
    for _ in range(n_geracoes):
        avalia_todos(populacao)
        populacao.sort(key = lambda x : x.fitness)
        p0 = populacao[0]
        p1 = populacao[1]
        
        hist_fitness.append(melhor_cromossomo(populacao).fitness)
        pais = seleciona(populacao)
        filhos = operacoes_geneticas(pais)
        populacao = filhos
        populacao.append(p0)
        populacao.append(p1)
    
    avalia_todos(populacao)
    hist_fitness.append(melhor_cromossomo(populacao).fitness)
    plt.plot(hist_fitness)
    
    return melhor_cromossomo(populacao)

def main():

    map1 = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
    
    maze1 = Maze(map1, [0,0], [9,9])

    map2 = [[0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0]]

    maze2 = Maze(map2, [0,0], [0,5])

    solucao = GA(maze=maze1, n_populacao = 100, n_geracoes = 100)
    print(solucao.genes, solucao.fitness)

main()

