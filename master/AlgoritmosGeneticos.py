import numpy as np
import string
import random

correct_word = 'ABC'

def eval_word(word):
    score = 0
    for i in range(len(word)):
        if word[i] == correct_word[i]:
            score += 1
            
    score = 100 * (score/len(correct_word))    
    return score

def tournament_selection(population, k):
    n_selected = []
    while len(n_selected) < len(population):
        tournament_individuals =  np.random.choice(population, k)
        tournament_scores = [eval_word(i) for i in tournament_individuals]
        max_index = tournament_scores.index(max(tournament_scores))
        n_selected.append(tournament_individuals[k-1])
    
    return n_selected

def crossover(parents):
    
    return parents[0][:3] + parents[1][3:], parents[1][:3] + parents[0][3:]

def select_parents(population):
    parents = []
    for i in range(int(len(population)/2)):
        parents.append([population[2*i], population[2*i+1]])
    
    return parents

def mutation(population):
    alphabet = [letter for letter in string.ascii_uppercase]
    mutation_rate = 0.15
    ind_mut = int(mutation_rate * len(population))
    pop_normal = population[ind_mut:]
    n_muted = len(population[:ind_mut])
    
    pop_mut = []
    for individual in range(n_muted):
        random_word = ''.join(str(elem) for elem in np.random.choice(alphabet, len(correct_word)))
        pop_mut.append(random_word)
    
    return pop_normal + pop_mut

def main():
    # Geração da população aleatória
    alphabet = [letter for letter in string.ascii_uppercase]

    n_population = 100
    population = []
    for individual in range(n_population):
        initial_word = ''.join(str(elem) for elem in np.random.choice(alphabet, len(correct_word)))
        population.append(initial_word)

    scores = [eval_word(word) for word in population]

    gen = 0
    while max(scores) < 100:
        print('GERAÇÃO: ', gen, 'SCORE:', max(scores), 'BEST WORD: ', population[scores.index(max(scores))])

        # Selecionar indivíduos
        population = tournament_selection(population, 10)

        # Aplicar operadores genéticos
        parents = select_parents(population)
        next_generation = []
        for couple in parents:
            children = crossover(couple)
            for child in children:
                next_generation.append(child)
                
        population = next_generation
        population = mutation(population)
        
        # Calcular aptidão
        scores = [eval_word(word) for word in population]
                
        gen += 1
        
    print('GERAÇÃO: ', gen, 'SCORE:', max(scores), 'BEST WORD: ', population[scores.index(max(scores))])

if __name__ == '__main__':
    main()
        



