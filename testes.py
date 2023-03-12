import player3
from copy import deepcopy

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
    for i in range(4):
        for j in range(4):
            if state[i][j] != EMPTY:
                temp = state[i][j]['valor']
                score += temp
            
    return score



def can_slide(tabuleiro, direcao):
    """
    Verifica se a peça na posição (linha_atual, coluna_atual) no tabuleiro pode deslizar na direção especificada.
    Retorna True se puder deslizar, False caso contrário.
    """

    if direcao == 'L':
       return player3.slideRigthOuLeft(tabuleiro, 'L', True)
    if direcao == 'R':
       return player3.slideRigthOuLeft(tabuleiro, 'R', True)
    if direcao == 'U':
        return player3.slideUPOuDown(tabuleiro, 'U', True)
    if direcao == 'D':
        return player3.slideUPOuDown(tabuleiro, 'D', True)
    




def get_valid_moves(state, player):
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
       player3.slideUPOuDown(new_state, UP)

    elif move[0] == DOWN:
       player3.slideUPOuDown(new_state, DOWN)
    elif move[0] == LEFT:
        player3.slideRigthOuLeft(new_state, LEFT)
    elif move[0] == RIGHT:
       player3.slideRigthOuLeft(new_state, RIGHT)
    return new_state
    
    



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

    # Se nenhuma das condições acima for atendida, o jogo não terminou
    return False


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
        for move in get_valid_moves(state, opc):
            print(move)
            new_state = make_move(state, move)
            _, score = minimax(new_state, depth-1, alpha, beta, False, opc)
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
        for move in get_valid_moves(state, opc):
            new_state = make_move(state, move)
            
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
    [ 0, {'cor': 'V', 'valor' : 9},  {'cor': 'C', 'valor' : 1}, 0],
    [{'cor': 'V', 'valor' : 3}, {'cor': 'A', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 3} ],
    [{'cor': 'C', 'valor' : 2}, {'cor': 'C', 'valor' : 3}, {'cor': 'V', 'valor' : 3}, {'cor': 'C', 'valor' : 9}],
    [{'cor': 'A', 'valor' : 3}, {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 9}, {'cor': 'C', 'valor' : 1}]
    ]

tab2 = [
    [ {'cor': 'V', 'valor' : 1}, {'cor': 'A', 'valor' : 2},  {'cor': 'C', 'valor' : 2}, {'cor': 'C', 'valor' : 1}],
    [0, 0, 0,0],
    [0, 0, 0,0],
    [0, 0, 0,0]
    ]

# get_valid_moves(tab1, 'A')

print(minimax(tab2, 3, float('-inf'), float('inf'),True,  ''))
