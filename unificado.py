
import random
EMPTY = 0
AZUL  = 'A'
CINZA = 'C'
VERMELHO = 'V'

# Define as constantes do movimento
PLACE_BLUE = AZUL
PLACE_RED = VERMELHO
PLACE_GREY = CINZA



tab3 = [
    [{'cor': 'V', 'valor' : 2}, 0,  {'cor': 'C', 'valor' : 1}, {'cor': 'V', 'valor' : 9}],
    [{'cor': 'C', 'valor' : 1}, 0, 0,0],
    [0, 0, 0,0],
    [0, 0, 0,{'cor': 'C', 'valor' : 1}]
]




def coresProximoMovimento(tabuleiro: list, cor: str):
    movimentosValidos = []      
    for i in range(4):
        for j in range(4):
            if tabuleiro[i][j] == EMPTY:
                movimentosValidos.append((i, j))
    
    cores = {AZUL : [VERMELHO, CINZA], VERMELHO: [CINZA], CINZA: []}

    movimentosEVizinhos = []
    for movimento in movimentosValidos:
        vizinhos = []
        linha, coluna = movimento
        
        if linha > 0:
             vizinhos.append(tabuleiro[linha-1][coluna]) # vizinho acima
        if linha < 3:
            vizinhos.append(tabuleiro[linha+1][coluna]) # vizinho abaixo
        if coluna > 0:
            vizinhos.append(tabuleiro[linha][coluna-1]) # vizinho à esquerda
        if coluna < 3:
            vizinhos.append(tabuleiro[linha][coluna+1]) # vizinho à direita
        
        movimentosEVizinhos.append((movimento, vizinhos))
    
    opcoesCores = cores[cor]

    
    final = []
    for opcaoCor in opcoesCores:
        for movimentoEVizinhos in movimentosEVizinhos:
            dic = {'cor': opcaoCor, 'valor': 1}
            movimento, vizinhos = movimentoEVizinhos
            
            if all(dic != dicionario for dicionario in vizinhos):
                final.append((movimento, dic))
                break
    
    valores = []
    for validos in final:
        pos, val = validos
        movimentosValidos.remove(pos)
        valores.append(val['cor'])
    
    for color in opcoesCores:
        if color not in valores:
            mvVal = random.choice(movimentosValidos)
            final.append((mvVal, {'cor': color, 'valor': 1}))

    return final

coresProximoMovimento(tab3, 'V')


from itertools import permutations

def permutate_colors(tab):
    empty_cells = []
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if tab[i][j] == 0:
                empty_cells.append((i,j))
    
    permutations_list = []
    for combination in permutations(empty_cells, 3):
        permutation = []
        for cell in combination:
            permutation.append((cell, 'R'))
            permutation.append((cell, 'B'))
            permutation.append((cell, 'Y'))
        permutations_list.append(permutation)
    
    return permutations_list


tab3 = [    [{'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 2},  {'cor': 'C', 'valor' : 1}, {'cor': 'V', 'valor' : 9}],
    [0, 0, 0,0],
    [0, 0, 0,0],
    [0, 0, 0,{'cor': 'C', 'valor' : 1}],
]

permutations_list = permutate_colors(tab3)
print(len(permutations_list))
