import numpy as np

# movimentações possíveis: U, L, D, R
# up, left, down, right
possible_directions = ['U', 'L', 'D', 'R']

# position = (x, y)

def action(direction):
    if direction == 'U':
        return np.array([0, 1])
    elif direction == 'L':
        return np.array([-1, 0])
    elif direction == 'D':
        return np.array([0, -1])
    else:
        return np.array([1, 0])
    
def clean(position):
    x, y = position[0], position[1]
    if space[x][y] == 1:
        space[x][y] = 0 # clean
        print("Posição {},{} limpa!".format(x,y))

# Fazendo as direções para o aspirador varrer o espaço
def directions():
    directions = []
    for i in range(1, N+1):
        first, last = N*(i-1), N*i
        if i%2 != 0:
            move = 'U'
        else:
            move = 'D'
        c = first
        while c < last-1:
            directions.append(move)
            c += 1
            
        if i != N:
            directions.append('R')
        
    return directions
    
    
def transition(position, direction):
    next_position = position + action(direction)
    if next_position[0] < 0 or next_position[0] > N or next_position[1] < 0 or next_position[1] > N:
        return np.array(position)
    else:
        return next_position
    
def goal_test(space):
    dirty_squares = 0
    for i in range(N):
        for j in range(N):
            if space[i][j] == 1:
                dirty_squares += 1
                
                
# tamanho do espaço
N = 3

# Criando o espaço NxN com sujeiras aleatórias
space = []
for i in range(N):
    v = np.zeros(N)
    v[0], v[N-1] = 1, 1
    np.random.shuffle(v)
    space.append(v)
    
space = np.array(space)

print(space)


# Posição inicial
pos = np.array([0, 0])
next_dir = directions()

for direction in next_dir:
    clean(pos)
    pos = transition(pos, direction)
    print(space)
    
clean(pos)
print(space)

