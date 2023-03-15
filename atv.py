import testes
from copy import deepcopy
import random

EMPTY = 0
AZUL  = 'A'
CINZA = 'C'
VERMELHO = 'V'

# Define as constantes do movimento
PLACE_BLUE = AZUL
PLACE_RED = VERMELHO
PLACE_GREY = CINZA






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


def melhorLugarCor(tabuleiro: list, cor: str):
  
    movimentosValidos = []      
    for i in range(4):
        for j in range(4):
            if tabuleiro[i][j] == EMPTY:
                if cor == AZUL:
                    movimentosValidos.append((PLACE_BLUE, i, j))
                elif cor == VERMELHO:
                    movimentosValidos.append((PLACE_RED, i, j))
                elif cor == CINZA:
                    movimentosValidos.append((PLACE_GREY, i, j))

    def incrementaProximosmovimentos(tab, c):
        movs = coresProximoMovimento(tab, c)
        for mov in movs:
            i, j = mov[0]
            tab[i][j] = mov[1]
            
    melhores = []
    profundidade = len(movimentosValidos)
    for valid in movimentosValidos:
        print(valid)
        estado = deepcopy(tabuleiro)
        estado[valid[1]][valid[2]] = {'cor': valid[0], 'valor': 1}
        incrementaProximosmovimentos(estado, cor)
        mini_max = testes.minimax(estado, profundidade, float('-inf'), float('inf'),True,  '')
        melhores.append((mini_max[1],valid))
    
    if len(melhores) >  0:
        maximo = max(melhores, key=lambda x: x[0])

        empates = [i for i in melhores if maximo[0] == i [0]]
        
        return  random.choice(empates)
    else:
        return False



print(melhorLugarCor(testes.tab3, 'V'))


tab = [
    [ 0, {'cor': 'C', 'valor' : 1}, 0, {'cor': 'V', 'valor' : 9}],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 3} ],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, 0, {'cor': 'C', 'valor' : 1}],
    [{'cor': 'A', 'valor' : 3}, {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 1}]
    ]


tab1 = [
    [ {'cor': 'C', 'valor' : 1}, {'cor': 'V', 'valor' : 1},  {'cor': 'C', 'valor' : 1}, {'cor': 'C', 'valor' : 2}],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 3} ],
    [{'cor': 'C', 'valor' : 2}, {'cor': 'C', 'valor' : 3}, {'cor': 'V', 'valor' : 3}, {'cor': 'C', 'valor' : 9}],
    [{'cor': 'A', 'valor' : 3}, {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 1}]
    ]

tab2 = [
    [ 0, {'cor': 'V', 'valor' : 9},  {'cor': 'V', 'valor' : 1}, 0],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, {'cor': 'C', 'valor' : 9}, {'cor': 'C', 'valor' : 3} ],
    [{'cor': 'C', 'valor' : 2}, {'cor': 'C', 'valor' : 3}, {'cor': 'V', 'valor' : 3}, {'cor': 'C', 'valor' : 9}],
    [{'cor': 'A', 'valor' : 3}, {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 1}]
    ]

tab3 = [
    [{'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 2},  {'cor': 'C', 'valor' : 1}, {'cor': 'V', 'valor' : 9}],
    [{'cor': 'C', 'valor' : 1}, 0, 0,0],
    [0, 0, 0,0],
    [0, 0, 0,{'cor': 'C', 'valor' : 1}],
    ]

tab4 = [
    [0, 0,  0, 0],
    [0, 0, 0,0],
    [0, 0, 0,0],
    [0, 0, 0,0],
    ]



