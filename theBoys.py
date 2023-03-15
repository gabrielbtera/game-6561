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
    
    """
    Faz o deslizamento e verifica tambem se o deslizamento eh feito ou nao
    para a esquerda L ou para direita R

    """
    
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
    """
    Faz o deslizamento e verifica tambem se o deslizamento eh feito ou nao
    para a esquerda L ou para direita R

    """
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
    Adcio
    """
    zeros = 0
    score = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != EMPTY:
                if state[i][j]['valor'] % 3 == 0:
                    # Adiciona uma pontuacao para cada pedra que seja multipla de 3
                    score += (state[i][j]['valor'] // 3) 
              
                else:
                    # Subitrai uma pontuacao para cada pedra que nao seja multipla de 3
                    score -= (state[i][j]['valor'] // 3)
            else:
                zeros += 1 # Faz uma conta de quantos espacos vazios existem no tabuleiro
    
    # Retorna a soma dos multiplos ou nao e dos zeros, equilibrando a ideia 
    # de ter mais pontos e espacos vazios pra jogar
    return score + zeros



def fazSlide(tabuleiro, direcao) -> bool:
    # Unifica as funcoes de slide e as executa

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
    # Retorna uma novo espaco de estados
    return new_state

def simulaMovimento(tabuleiro: list):
    # Auxilia no caso base da minimax verificando se no tabuleiro com todos os espacos preenchidos
    # ainda se pode fazer algum algum movimento

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
    movimenta = simulaMovimento(state) # ver se existe algum movimento se o tabuleiro estiver preenchido

    if movimenta:
        return False
    
    # Verifica se o tabuleiro está completamente preenchido
    if all(cell != EMPTY for row in state for cell in row):
        return True

    # Verifica se algum jogador não tem mais peças no tabuleiro
    if not any(EMPTY in row for row in state):
        return True

    # Se a funcao esta de morando mais de 3 segundos pra responder, isso para a execucao dela
    if (time.time() - tempo_inicial  >= 3):
        tempo_inicial = time.time()
        return True
    

    # Se nenhuma das condições acima for atendida, o jogo não terminou
    return False



from itertools import permutations

# Define a função minimax alpha beta
def minimax(tabuleiro, profundidade, alpha, beta, maximizando_player, opc):
    """
    Executa a busca minimax até a profundidade especificada e retorna a melhor jogada possível
    para o jogador atual a partir do estado atual do jogo.
    """
    # Caso base da funcao
    if profundidade == 0 or is_terminal(tabuleiro):
        return None, avaliacao(tabuleiro, opc) ## Funcao de avaliacao
    

    if maximizando_player:
        max_score = float('-inf')
        best_move = None
        valids = pegaMovimentosValidos(tabuleiro, opc) # Lista de movimentos validos
        
        for move in valids:
            new_state = executarMovimentos(tabuleiro, move) # Cria um novo estado de movimentos
            _, score = minimax(new_state, profundidade-1, alpha, beta, False, opc) # Aplica a recursao
            # Verifica a pontuacao
            if score > max_score:
                max_score = score
                best_move = move
            # Verifica a poda
            alpha = max(alpha, max_score)
            if beta <= alpha:
                break
        return best_move, max_score
    else:
        min_score = float('inf')
        best_move = None
        valids = pegaMovimentosValidos(tabuleiro, opc) # Lista de movimentos validos
        for move in valids:
            new_state = executarMovimentos(tabuleiro, move) # Cria um novo estado de movimentos
            _, score = minimax(new_state, profundidade-1, alpha, beta, True, opc) # Aplica a recursao
            # Verifica a pontuacao
            if score < min_score:
                min_score = score
                best_move = move
            # Verifica a poda
            beta = min(beta, min_score)
            if beta <= alpha:
                break
        return best_move, min_score


    

def coresProximoMovimento(tabuleiro: list, cor: str):
    """
    Esta funcao faz uma estimativas de quais sao as cores dos proximos movimentos
    ela usa uma politica de desempates por melhor vizinho, se existir um 
    vizinho com a mesma cor e valor ela prioriza o indice desse movimento, e faz ao contrio
    pega o pior vizinho tambem e cria uma zonha mista, assumindo que o oponente nao eh 
    tao inteligente

    """
    movimentosValidos = []      
    for i in range(4):
        for j in range(4):
            if tabuleiro[i][j] == EMPTY:
                movimentosValidos.append((i, j))
    
    cores = {AZUL : [VERMELHO, CINZA], VERMELHO: [CINZA], CINZA: []} # Movimentos e seus sucessores

    movimentosEVizinhos = []
    # Pega os seu melhor vizinho
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
            
            if all(dic != dicionario for dicionario in vizinhos): # aqui ele simula o pior cenario de vizinhos
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
            if len(movimentosValidos):
                mvVal = random.choice(movimentosValidos)
                final.append((mvVal, {'cor': color, 'valor': 1}))
    
    # Retorna uma lista de tuplas com o melhor indice e a cor correspondente desse na simulacao, se nao existir nenhuma ele randomiza
    return final


def verificaSeTodosSaoZero(tabuleiro): # verifica tabuleiro vazio
    tabs = 0
    for i in range(4):
     for j in range(4):
        if tabuleiro[i][j] == EMPTY:
            tabs += 1
    return bool(tabs)


def melhorLugarCor(tabuleiro: list, cor: str) -> tuple or bool:

    """
    Define qual o melhor lugar para adicionar uma dada cor 
    ela se baseia em uma simulacao de movimentos distintos e randomizados
    criando varios estados e aplicando a minimax nesses estados para retorna o
    melhor movimento
    """
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
        if verificaSeTodosSaoZero(tab):
            movs = coresProximoMovimento(tab, c)
            for mov in movs:
                i, j = mov[0]
                tab[i][j] = mov[1]
            
    melhores = []
    profundidade = 5
    for valid in movimentosValidos:
        estado = deepcopy(tabuleiro)
        estado[valid[1]][valid[2]] = {'cor': valid[0], 'valor': 1}
        incrementaProximosmovimentos(estado, cor) # Cria um novo estado com uma nova simulacao
        mini_max = minimax(estado, profundidade, float('-inf'), float('inf'),True,  '') # aplica a minimax
        melhores.append((mini_max[1],valid)) # Salva os valores numa lista
    
    if len(melhores) >  0:
        maximo = max(melhores, key=lambda x: x[0]) # obtemos o maximo desta lista

        empates = [i for i in melhores if maximo[0] == i [0]] # verificamos se existem empates
        
        return  random.choice(empates)[1] # resolvemos esses empates randomizando os melhores
    else:
        return False # Retonamos false caso nao exista movimento



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
    """
    Funcao principal que une toda a logica de pegar a melhor posicao de uma peca
    """

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
    """
    Funcao principal que une toda a logica de pegar o melhor slide
    """
    PROFUNDIDADE = 6
    
    def getMovimento(resultado: tuple) -> tuple:
        return resultado[0]
    
    resultadoMinimax = minimax(tabuleiro, PROFUNDIDADE, float('-inf'), float('inf'),True,  '')
    movimento = getMovimento(resultadoMinimax)
    novo_tab =  executarMovimentos(tabuleiro, movimento)

    for i in range(len(novo_tab)):
        tabuleiro[i] = novo_tab[i]

    return movimento[0]



def getAcao(tipoCor: int) -> str:
    # Pega uma acao
    opcoes = {0: 'A', 
              1: 'C', 
              2 : 'D1',
              3: 'V', 
              4 : 'D1'
              }
    return opcoes[tipoCor]

def acaoOponente(tipoCor: int ) -> str:
    # pega uma acao do oponente
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

    # Exeutar moviemntos do oponente no meu tabuleiro, logica de jogo

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




TABULEIRO = [[0,0,0, 0] for _ in range(4)] # tabuleiro

def main():
    # Funcao de execucao principal
    entrada = sys.stdin.readline().strip()

    player = entrada
    
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

            oponente = executarMovimentosOponente(TABULEIRO, entrada, contadorJogadas, player)
            if not oponente:
                print('Quit')
                sys.stdout.flush()
            # for i in TABULEIRO:
            #     print(i)

            contadorJogadas += 1
            contadorIteracoes += 1

                


            
    else:
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

            
            oponente = executarMovimentosOponente(TABULEIRO, entrada, contadorJogadas, player)
            

            if contadorJogadas in [0,2,3]:
                cor = acaoOponente(contadorJogadas)
                posicao = mainNovaPeca(TABULEIRO, cor)
                sys.stdout.flush()
                if posicao == 'Quit':
                    break

            if contadorJogadas in [1,4]:
                dado = pegarQuantidadeDeVazios(TABULEIRO)
            
                if not dado:
                    print(mainMovimento(TABULEIRO))
                else:
                    print(dado)
                sys.stdout.flush()
        
        
            contadorJogadas += 1
            contadorIteracoes += 1

main()


