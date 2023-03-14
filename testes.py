# import player3
import board
from copy import deepcopy
import sys
import time

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



def evaluate(state, player):
    """
    Retorna a pontuação de um determinado estado do jogo para o jogador especificado.
    """
    score = 0
    zeros = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != EMPTY:
                temp = state[i][j]['valor']
                score += temp
            else:
                zeros += 1
    eq = score - 104976  

    score = 0
    for i in range(4):
        for j in range(4):
            # Add points for each tile that is a multiple of 3
            if state[i][j] != EMPTY:
                if state[i][j]['valor'] % 3 == 0:
                    score += state[i][j]['valor'] // 3
                # Subtract points for each tile that is not a multiple of 3
                else:
                    score -= state[i][j]['valor'] // 3

    # print(score)
    return score



def can_slide(tabuleiro, direcao):
    """
    Verifica se a peça na posição (linha_atual, coluna_atual) no tabuleiro pode deslizar na direção especificada.
    Retorna True se puder deslizar, False caso contrário.
    """

    if direcao == 'L':
       return board.slideLeftOuRight(tabuleiro, 'L')[1]
    if direcao == 'R':
       return board.slideLeftOuRight(tabuleiro, 'R')[1]
    if direcao == 'U':
        return board.slideUpDwon(tabuleiro, 'U')[1]
    if direcao == 'D':
        return board.slideUpDwon(tabuleiro, 'D')[1]
    




def get_valid_moves(state: list, player: str):
    """
    Retorna uma lista de movimentos válidos para o jogador especificado a partir do estado atual do jogo.
    """
    valid_moves = []

   
      
    # if player in [AZUL, CINZA, VERMELHO]:
    for i in range(4):
        for j in range(4):
            if state[i][j] == EMPTY:
                if player == AZUL:
                    valid_moves.append((PLACE_BLUE, i, j))
                elif player == VERMELHO:
                    valid_moves.append((PLACE_RED, i, j))
                elif player == CINZA:
                    valid_moves.append((PLACE_GREY, i, j))
    # else:
        
    if can_slide(state, UP):
        valid_moves.append((UP,))
    if can_slide(state, DOWN):
        valid_moves.append((DOWN,))
    if can_slide(state, LEFT):
        valid_moves.append((LEFT,))
    if can_slide(state, RIGHT):
        valid_moves.append((RIGHT,))
    
   

    return valid_moves



def make_move(state: list, move: tuple):
    """
    Aplica o movimento especificado no estado atual do jogo e retorna o novo estado resultante.
    """

    new_state = deepcopy(state)
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
    if (time.time() - tempo_inicial  >= 50):
        return True
    

    # Se nenhuma das condições acima for atendida, o jogo não terminou
    return False

lista = []

def printa(tab):
    for i in tab:
        print(i)



# Define a função minimax
def minimax(state, depth, alpha, beta, maximizing_player, opc):
    """
    Executa a busca minimax até a profundidade especificada e retorna a melhor jogada possível
    para o jogador atual a partir do estado atual do jogo.
    """
    if depth == 0 or is_terminal(state):
        return None, evaluate(state, opc)
    
   

    if maximizing_player:
        max_score = float('-inf')
        best_move = None
        valids = get_valid_moves(state, opc)
        for move in valids:
            new_state = make_move(state, move)
            printa(state)
            print()
            print('íf', move)
            
            printa(new_state)
            print(valids)
            print()

            _, score = minimax(new_state, depth-1, alpha, beta, False, opc)
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, max_score)
            if beta <= alpha:
                break
        lista.append((best_move, max_score))
        return best_move, max_score
    else:
        min_score = float('inf')
        best_move = None
        valids = get_valid_moves(state, opc)
        for move in valids:
            new_state = make_move(state, move)
            printa(state)
            print()
            print('else', move)
           
            printa(new_state)
            print(valids)
            print()
            _, score = minimax(new_state, depth-1, alpha, beta, True, opc)
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, min_score)
            if beta <= alpha:
                break
        return best_move, min_score


    


tab = [
    [ 0, {'cor': 'C', 'valor' : 1}, 0, {'cor': 'V', 'valor' : 9}],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 3} ],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, 0, {'cor': 'C', 'valor' : 1}],
    [{'cor': 'A', 'valor' : 3}, {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 1}]
    ]


tab1 = [
    [ {'cor': 'C', 'valor' : 1}, {'cor': 'V', 'valor' : 9},  {'cor': 'C', 'valor' : 1}, {'cor': 'C', 'valor' : 2}],
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
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 2},  {'cor': 'C', 'valor' : 2}, {'cor': 'V', 'valor' : 9}],
    [{'cor': 'V', 'valor' : 3}, 0, 0,0],
    [0, 0, 0,0],
    [0, 0, 0,{'cor': 'C', 'valor' : 9}],
    ]

# get_valid_moves(tab1, 'A')

print(minimax(tab,2, float('-inf'), float('inf'),True,  'A'))

# print(get_valid_moves(tab3, ''))
# print(make_move(tab3,('D', )))

# print(get_valid_moves(tab3, ''))

# print('\n', lista)




# Faça algo aqui
tempo_final = time.time()

intervalo_de_tempo = tempo_final - tempo_inicial
print(intervalo_de_tempo)
