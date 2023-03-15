#!/usr/bin/env python3

from copy import deepcopy
import sys
import time

import random

sys.setrecursionlimit(10000) # Set the recursion limit to 1500 calls

# Define as constantes do jogo

EMPTY = 0
AZUL  = 'A'
CINZA = 'C'
VERMELHO = 'V'

# Define as constantes do movimento
PLACE_BLUE = AZUL
PLACE_RED = VERMELHO
PLACE_GREY = CINZA

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'



def slideLeftOuRight(tabuleiro: list, direcao: str) -> tuple:
    
    tabuleiro = deepcopy(tabuleiro)

    slide = False
    # Percorre a matriz linha por linha, da direita para a esquerda

    for linha in range(len(tabuleiro)):
        # Inicializa uma lista para armazenar as pecas do tabuleiro
        pecas_tabuleiro = []
        # Percorre a linha e adiciona os valores não nulos à lista
        if direcao == 'L':
            for coluna in range(len(tabuleiro[linha])):
                if tabuleiro[linha][coluna] != 0:
                    pecas_tabuleiro.append(tabuleiro[linha][coluna])
        else:
            for coluna in range(len(tabuleiro) - 1, -1, -1):
                if tabuleiro[linha][coluna] != 0:
                    pecas_tabuleiro.append(tabuleiro[linha][coluna])
                    
        # for coluna in range(len(tabuleiro[linha])):
        #     if tabuleiro[linha][coluna] != 0:
        #         pecas_tabuleiro.append(tabuleiro[linha][coluna])
        indice = 0
        while indice < len(pecas_tabuleiro) - 1:
            
            if pecas_tabuleiro[indice]['cor'] != pecas_tabuleiro[indice+1]['cor'] and pecas_tabuleiro[indice]['valor'] == pecas_tabuleiro[indice+1]['valor']:
                del pecas_tabuleiro[indice]
                tamanho_tab = len(pecas_tabuleiro)
                if tamanho_tab  >= indice:
                    del pecas_tabuleiro[indice]
                if tamanho_tab < indice:
                    del pecas_tabuleiro[indice+1]
                continue
            if pecas_tabuleiro[indice]['cor'] == pecas_tabuleiro[indice+1]['cor'] and pecas_tabuleiro[indice]['valor'] == pecas_tabuleiro[indice+1]['valor']:
                pecas_tabuleiro[indice] = {'cor': pecas_tabuleiro[indice]['cor'], 'valor': pecas_tabuleiro[indice]['valor'] * 3}
                del pecas_tabuleiro[indice+1]
                indice += 1
                continue
            
            indice += 1
       
        
        if direcao == 'R':
            pecas_tabuleiro.reverse()
            pecas_tabuleiro = [0] * (len(tabuleiro[linha]) - len(pecas_tabuleiro)) + pecas_tabuleiro

        elif direcao == 'L':
            pecas_tabuleiro = pecas_tabuleiro + [0] * (len(tabuleiro[linha]) - len(pecas_tabuleiro))
        

        if tabuleiro[linha] != pecas_tabuleiro:
            slide = True
            tabuleiro[linha] = pecas_tabuleiro
    
    return (tabuleiro, slide)


def slideUpDwon(tabuleiro: list, direcao: str) -> tuple:

    tabuleiro = deepcopy(tabuleiro)

    slide = False 

    # Percorre a matriz coluna por coluna, de cima para baixo ou de baixo para cima
    for coluna in range(len(tabuleiro)):
        valores_nao_nulos = []

        if direcao == 'U':
            for linha in range(len(tabuleiro)):
                if tabuleiro[linha][coluna] != 0:
                    valores_nao_nulos.append(tabuleiro[linha][coluna])
        else:
            for linha in range(len(tabuleiro) - 1, -1, -1):
                if tabuleiro[linha][coluna] != 0:
                    valores_nao_nulos.append(tabuleiro[linha][coluna])
            
        
        indice = 0
        while indice < len(valores_nao_nulos) - 1:
            if valores_nao_nulos[indice]['cor'] != valores_nao_nulos[indice+1]['cor'] and valores_nao_nulos[indice]['valor'] == valores_nao_nulos[indice+1]['valor']:
                del valores_nao_nulos[indice]
                tamanho_tab = len(valores_nao_nulos)
                if tamanho_tab  >= indice:
                    del valores_nao_nulos[indice]
                if tamanho_tab < indice:
                    del valores_nao_nulos[indice+1]
                continue
            if valores_nao_nulos[indice]['cor'] == valores_nao_nulos[indice+1]['cor'] and valores_nao_nulos[indice]['valor'] == valores_nao_nulos[indice+1]['valor']:
                valores_nao_nulos[indice] = {'cor': valores_nao_nulos[indice]['cor'], 'valor': valores_nao_nulos[indice]['valor'] * 3}
                del valores_nao_nulos[indice+1]
               
            indice += 1

        if direcao == 'U':
             valores_nao_nulos = valores_nao_nulos + [0] * (len(tabuleiro) - len(valores_nao_nulos))
        else:
            valores_nao_nulos.reverse()
            valores_nao_nulos = [0] * (len(tabuleiro) - len(valores_nao_nulos)) + valores_nao_nulos

        for linha in range(len(tabuleiro)):
            if tabuleiro[linha][coluna] != valores_nao_nulos[linha]:
                slide = True
                tabuleiro[linha][coluna] = valores_nao_nulos[linha]
    return (tabuleiro, slide)


def avaliacao(state: list, player: str) -> int:
    """
    Retorna a pontuação de um determinado estado do jogo para o jogador especificado.
    """
    zeros = 0
    score = 0
    for i in range(4):
        for j in range(4):
            # Add points for each tile that is a multiple of 3
            if state[i][j] != EMPTY:
                if state[i][j]['valor'] % 3 == 0:
                    score += (state[i][j]['valor'] // 3) 
                # Subtract points for each tile that is not a multiple of 3
                else:
                    score -= (state[i][j]['valor'] // 3)
            else:
                zeros += 1
    return score + zeros



def fazSlide(tabuleiro, direcao) -> bool:

    if direcao == 'L':
       return slideLeftOuRight(tabuleiro, 'L')[1]
    if direcao == 'R':
       return slideLeftOuRight(tabuleiro, 'R')[1]
    if direcao == 'U':
        return slideUpDwon(tabuleiro, 'U')[1]
    if direcao == 'D':
        return slideUpDwon(tabuleiro, 'D')[1]
    

def pegaMovimentosValidos(tabuleiro: list, player: str):
    """
    Retorna uma lista de movimentos válidos para o jogador especificado a partir do estado atual do jogo.
    """
    valid_moves = []

    # for i in range(4):
    #     for j in range(4):
    #         if tabuleiro[i][j] == EMPTY:
    #             if player == AZUL:
    #                 valid_moves.append((PLACE_BLUE, i, j))
    #             elif player == VERMELHO:
    #                 valid_moves.append((PLACE_RED, i, j))
    #             elif player == CINZA:
    #                 valid_moves.append((PLACE_GREY, i, j))

    if fazSlide(tabuleiro, UP):
        valid_moves.append((UP,))
    if fazSlide(tabuleiro, DOWN):
        valid_moves.append((DOWN,))
    if fazSlide(tabuleiro, LEFT):
        valid_moves.append((LEFT,))
    if fazSlide(tabuleiro, RIGHT):
        valid_moves.append((RIGHT,))
    
    return valid_moves



def executarMovimentos(tabuleiro: list, move: tuple) -> list:
    """
    Aplica o movimento especificado no estado atual do jogo e retorna o novo estado resultante.
    """

    new_state = deepcopy(tabuleiro)
    if move[0] == PLACE_BLUE:
        new_state[move[1]][move[2]] = {'cor': AZUL, 'valor': 1}
    elif move[0] == PLACE_RED:
        new_state[move[1]][move[2]] = {'cor': VERMELHO, 'valor': 1}
    elif move[0] == PLACE_GREY:
        new_state[move[1]][move[2]] = {'cor': CINZA, 'valor': 1}

    elif move[0] == UP:
       new_state = slideUpDwon(new_state, UP)[0]
    elif move[0] == DOWN:
       new_state = slideUpDwon(new_state, DOWN)[0]
    elif move[0] == LEFT:
       new_state = slideLeftOuRight(new_state, LEFT)[0]
    elif move[0] == RIGHT:
       new_state = slideLeftOuRight(new_state, RIGHT)[0]
    return new_state

def simulaMovimento(tabuleiro: list):

    if fazSlide(tabuleiro, UP):
        return True
    if fazSlide(tabuleiro, DOWN):
        return True
    if fazSlide(tabuleiro, LEFT):
        return True
    if fazSlide(tabuleiro, RIGHT):
        return True
    


tempo_inicial = time.time()
def is_terminal(state):
    """
    Verifica se o jogo terminou a partir do estado atual do jogo.
    Retorna True se o jogo terminou, False caso contrário.
    """

    global tempo_inicial
    movimenta = simulaMovimento(state)

    if movimenta:
        return False
    
    # Verifica se o tabuleiro está completamente preenchido
    if all(cell != EMPTY for row in state for cell in row):
        return True

    # Verifica se algum jogador não tem mais peças no tabuleiro
    if not any(EMPTY in row for row in state):
        return True

    # # Verifica se algum jogador já venceu
    # for player in [BLUE, RED, GREY]:
    #     if evaluate(state, player) == 4:
    #         return True
    if (time.time() - tempo_inicial  >= 6):
        tempo_inicial = time.time()
        return True
    

    # Se nenhuma das condições acima for atendida, o jogo não terminou
    return False



from itertools import permutations

# Define a função minimax
def minimax(tabuleiro, profundidade, alpha, beta, maximizando_player, opc):
    """
    Executa a busca minimax até a profundidade especificada e retorna a melhor jogada possível
    para o jogador atual a partir do estado atual do jogo.
    """
    if profundidade == 0 or is_terminal(tabuleiro):
        return None, avaliacao(tabuleiro, opc)
    

    if maximizando_player:
        max_score = float('-inf')
        best_move = None
        valids = pegaMovimentosValidos(tabuleiro, opc)
        
        for move in valids:
            new_state = executarMovimentos(tabuleiro, move)
            _, score = minimax(new_state, profundidade-1, alpha, beta, False, opc)
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, max_score)
            if beta <= alpha:
                break
        return best_move, max_score
    else:
        min_score = float('inf')
        best_move = None
        valids = pegaMovimentosValidos(tabuleiro, opc)
        for move in valids:
            new_state = executarMovimentos(tabuleiro, move)
            _, score = minimax(new_state, profundidade-1, alpha, beta, True, opc)
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, min_score)
            if beta <= alpha:
                break
        return best_move, min_score


    

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
        if pos in movimentosValidos:
            movimentosValidos.remove(pos)
        valores.append(val['cor'])
    
    for color in opcoesCores:
        if color not in valores:
            mvVal = random.choice(movimentosValidos)
            final.append((mvVal, {'cor': color, 'valor': 1}))

    return final





def melhorLugarCor(tabuleiro: list, cor: str) -> tuple or bool:
  
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

    def incrementaProximosmovimentos(tab: list, c: str) -> None:
        movs = coresProximoMovimento(tab, c)
        for mov in movs:
            i, j = mov[0]
            tab[i][j] = mov[1]
            
    melhores = []
    profundidade = len(movimentosValidos)
    for valid in movimentosValidos:
        estado = deepcopy(tabuleiro)
        estado[valid[1]][valid[2]] = {'cor': valid[0], 'valor': 1}
        incrementaProximosmovimentos(estado, cor)
        mini_max = minimax(estado, profundidade, float('-inf'), float('inf'),True,  '')
        melhores.append((mini_max[1],valid))
    
    if len(melhores) >  0:
        maximo = max(melhores, key=lambda x: x[0])

        empates = [i for i in melhores if maximo[0] == i [0]]
        
        return  random.choice(empates)[1]
    else:
        return False



def pegarQuantidadeDeVazios(tabuleiro: list) -> str:
    """
    Esta funcao verifica se o tabuleiro esta vazio, se sim retorna
    uma posicao radomizaada se nao retorna vazio
    """
    cont = 0
    for i in range(4):
        for j in range(4):
            if tabuleiro[i][j] == EMPTY:
                cont += 1
    if cont == 16:
        possibilidades = ['1','2','3', '4']
        posi = []
        for i in possibilidades:
            for j in possibilidades:
                posi.append(i+j)
        return random.choice(posi)
    return ''

def getFormataPeca(peca: tuple):
    return {'cor': peca[0], 'valor': 1}

def setNovaPecaTabuleiro(tabuleiro: list, peca: tuple) -> None:
    _, i, j = peca
    tabuleiro[i][j] = getFormataPeca(peca)
    return f'{i+1}{j+1}'



def mainNovaPeca(tabuleiro: list, cor: str) -> str:

    def getFormataPeca(peca: tuple):
        return {'cor': peca[0], 'valor': 1}

    def setNovaPecaTabuleiro(tabuleiro: list, peca: tuple) -> None:
        _, i, j = peca
        tabuleiro[i][j] = getFormataPeca(peca)
        return f'{i+1}{j+1}'

    melhorLugar = melhorLugarCor(tabuleiro, cor)
    if melhorLugar:
        return setNovaPecaTabuleiro(tabuleiro, melhorLugar)
    else:
        return 'Quit'

def mainMovimento(tabuleiro: list, opc= ''):
    PROFUNDIDADE = 10
    
    def getMovimento(resultado: tuple) -> tuple:
        return resultado[0]
    
    
   

   
    resultadoMinimax = minimax(tabuleiro, PROFUNDIDADE, float('-inf'), float('inf'),True,  '')
    movimento = getMovimento(resultadoMinimax)
    novo_tab =  executarMovimentos(tabuleiro, movimento)

    for i in range(len(novo_tab)):
        tabuleiro[i] = novo_tab[i]

    return movimento[0]



def getAcao(tipoCor: int) -> str:
    opcoes = {0: 'A', 
              1: 'C', 
              2 : 'D1',
              3: 'V', 
              4 : 'D1'
              }
    return opcoes[tipoCor]

def acaoOponente(tipoCor: int ) -> str:
    opcoes = {0: 'V', 
              1: 'D1', 
              2 : 'A',
              3: 'C', 
              4 : 'D1'
              }
    return opcoes[tipoCor]


def escreveTabuleiro(tabAntes, tabDepois):
    tamanho = len(tabAntes)
    for i in range(tamanho):
        tabAntes[i] = tabDepois[i]

def executarMovimentosOponente(tabuleiro , opcao, contador, player):
    if opcao in ['U', 'D']:
        tab, sli = slideUpDwon(tabuleiro, opcao)
        escreveTabuleiro(tabuleiro, tab)
        return sli
    elif opcao in ['L', 'R']:
        tab, sli = slideLeftOuRight(tabuleiro, opcao)
        escreveTabuleiro(tabuleiro, tab)
        return sli
    else:
        i,j = int(opcao[0])-1, int(opcao[1])-1
    
        if tabuleiro[i][j] == EMPTY:
            cor = acaoOponente(contador) if player == 'A' else getAcao(contador)
            tabuleiro[i][j] = {'cor': cor, 'valor': 1}
            return True
        else:
            return False




TABULEIRO = [[0,0,0, 0] for _ in range(4)]

def main():

    entrada = sys.stdin.readline().strip()
    
    contadorJogadas = 0
    contadorIteracoes = 0
    if (entrada == "A"):
        
        while (True):
            if contadorJogadas > 4:
                contadorJogadas = 0

            if entrada.strip() == "Quit":
                break
            
            if contadorIteracoes == 999:
                print('Quit')
                sys.stdout.flush()
                break

            if contadorJogadas in [0,1,3]:
                cor = getAcao(contadorJogadas)
                posicao = mainNovaPeca(TABULEIRO, cor)
                print(posicao)
                sys.stdout.flush()
                if posicao == 'Quit':
                    break

            if contadorJogadas in [2,4]:
                dado = pegarQuantidadeDeVazios(TABULEIRO)
                if not dado:
                    print(mainMovimento(TABULEIRO))
                else:
                    print(dado)
                sys.stdout.flush()
            
            # for i in TABULEIRO:
            #     print(i)

            entrada = sys.stdin.readline().strip()

            oponente = executarMovimentosOponente(TABULEIRO, entrada, contadorJogadas, entrada)
            # for i in TABULEIRO:
            #     print(i)

            contadorJogadas += 1
            contadorIteracoes += 1

                


            
    else:
        # Estou jogando como Order
        memoria = []
        while (True):
            entrada = sys.stdin.readline().strip()

            if contadorJogadas > 4:
                contadorJogadas = 0

            if entrada.strip() == "Quit":
                break
            
            if contadorIteracoes == 999:
                print('Quit')
                sys.stdout.flush()
                break

            
            oponente = executarMovimentosOponente(TABULEIRO, entrada, contadorJogadas, entrada)
            

            if contadorJogadas in [0,2,3]:
                cor = acaoOponente(contadorJogadas)
                posicao = mainNovaPeca(TABULEIRO, cor)
                print(posicao, 'ultima', contadorJogadas)
                sys.stdout.flush()
                if posicao == 'Quit':
                    break

            if contadorJogadas in [1,4]:
                dado = pegarQuantidadeDeVazios(TABULEIRO)
                print('aqui', contadorJogadas, dado)
                if not dado:
                    print(mainMovimento(TABULEIRO))
                else:
                    print(dado)
                sys.stdout.flush()
        
        
            contadorJogadas += 1
            contadorIteracoes += 1

main()

