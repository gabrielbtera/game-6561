import board
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
       return board.slideLeftOuRight(tabuleiro, 'L')[1]
    if direcao == 'R':
       return board.slideLeftOuRight(tabuleiro, 'R')[1]
    if direcao == 'U':
        return board.slideUpDwon(tabuleiro, 'U')[1]
    if direcao == 'D':
        return board.slideUpDwon(tabuleiro, 'D')[1]
    

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
       new_state = board.slideUpDwon(new_state, UP)[0]
    elif move[0] == DOWN:
       new_state = board.slideUpDwon(new_state, DOWN)[0]
    elif move[0] == LEFT:
       new_state = board.slideLeftOuRight(new_state, LEFT)[0]
    elif move[0] == RIGHT:
       new_state = board.slideLeftOuRight(new_state, RIGHT)[0]
    return new_state
    
    


tempo_inicial = time.time()
def is_terminal(state):
    """
    Verifica se o jogo terminou a partir do estado atual do jogo.
    Retorna True se o jogo terminou, False caso contrário.
    """

    print(len(pegaMovimentosValidos(state, '')))
    global tempo_inicial
    # Verifica se o tabuleiro está completamente preenchido
    if all(cell != EMPTY for row in state for cell in row) and not len(pegaMovimentosValidos(state, '')):
        return True

    # Verifica se algum jogador não tem mais peças no tabuleiro
    if not any(EMPTY in row for row in state) and not len(pegaMovimentosValidos(state, '')):
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

print(minimax(tab, 16, float('-inf'), float('inf'),True,  ''))

def pegarQuantidadeDeVazios(tabuleiro: list) -> str:
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
    for i in len(novo_tab):
        tabuleiro[i] = novo_tab[i]
    return movimento[0]



def getAcao(tipoCor: int) -> str:
    opcoes = {0: 'B', 
              1: 'C', 
              2 : 'D1',
              3: 'V', 
              4 : 'D1'
              }
    return opcoes[tipoCor]


TABULEIRO = [[0,0,0, 0] for _ in range(4)]

def main():

    entrada = sys.stdin.readline()
    
    contadorJogadas = 0
    contadorIteracoes = 0
    if (entrada.strip() == "A"):
        
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
                    print()




        

            print(str(lc))

            sys.stdout.flush()

            entrada = sys.stdin.readline()

            acao = getAcao(entrada)

            contadorJogadas += 1
            contadorIteracoes += 1

                


            
    else:
        # Estou jogando como Order
        memoria = []
        while (True):
            if (entrada.strip() == "Quit"):
                break
            lc = random.randint(11, 44)
            # memoria.append(entrada[1]+entrada[2])
            # Escolha aleatoria de peca existente
            # random.shuffle(memoria)
            # peca = memoria[0]
            # memoria.remove(peca)
            # Laço para definir local destino
            # Tem que respeitar horizontal ou vertical
            # random.shuffle(linhas)
            # random.shuffle(colunas)
            # lc = linhas[0]+colunas[0]
            # while ((lc in memoria) or (lc[0]!=peca[0]) or (lc[1]!=peca[1])):
            #     random.shuffle(linhas)
            #     random.shuffle(colunas)
            #     lc = linhas[0]+colunas[0]
            # memoria.append(lc)
            # #Saida da jogada
            # print(peca+lc)
            lc = random.randint(11, 44);

            print(lc)

            sys.stdout.flush()
            # Leitura da jogada do adversario Chaos
            
            entrada = sys.stdin.readline()



# main()

