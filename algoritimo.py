import random

# Define as constantes do jogo
EMPTY = 0
BLUE = 1
RED = 2
GREY = 3

# Define as constantes do movimento
PLACE_BLUE = 1
PLACE_RED = 2
PLACE_GREY = 3
SLIDE_UP = 'U'
SLIDE_DOWN = 'D'
SLIDE_LEFT = 'L'
SLIDE_RIGHT = 'R'

# Define a função de avaliação
def evaluate(state, player):
    """
    Retorna a pontuação de um determinado estado do jogo para o jogador especificado.
    """
    score = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] == player:
                score += 1
            elif state[i][j] != EMPTY:
                score -= 1
    return score




def can_slide(tabuleiro, linha_atual, coluna_atual, direcao):
    """
    Verifica se a peça na posição (linha_atual, coluna_atual) no tabuleiro pode deslizar na direção especificada.
    Retorna True se puder deslizar, False caso contrário.
    """
    tamanho_tabuleiro = len(tabuleiro)
    proxima_linha, proxima_coluna = linha_atual, coluna_atual
    
    if direcao == 'L':
        while proxima_coluna > 0:
            proxima_coluna -= 1
            if tabuleiro[linha_atual][proxima_coluna] == '#':
                return False
            if tabuleiro[linha_atual][proxima_coluna] == '@':
                return True
        return False

    if direcao == 'R':
        while proxima_coluna < tamanho_tabuleiro - 1:
            proxima_coluna += 1
            if tabuleiro[linha_atual][proxima_coluna] == '#':
                return False
            if tabuleiro[linha_atual][proxima_coluna] == '@':
                return True
        return False

    if direcao == 'U':
        while proxima_linha > 0:
            proxima_linha -= 1
            if tabuleiro[proxima_linha][coluna_atual] == '#':
                return False
            if tabuleiro[proxima_linha][coluna_atual] == '@':
                return True
        return False

    if direcao == 'D':
        while proxima_linha < tamanho_tabuleiro - 1:
            proxima_linha += 1
            if tabuleiro[proxima_linha][coluna_atual] == '#':
                return False
            if tabuleiro[proxima_linha][coluna_atual] == '@':
                return True
        return False



def get_valid_moves(state, player):
    """
    Retorna uma lista de movimentos válidos para o jogador especificado a partir do estado atual do jogo.
    """
    valid_moves = []
    for i in range(4):
        for j in range(4):
            if state[i][j] == EMPTY:
                if player == BLUE:
                    valid_moves.append((PLACE_BLUE, i, j))
                elif player == RED:
                    valid_moves.append((PLACE_RED, i, j))
                elif player == GREY:
                    valid_moves.append((PLACE_GREY, i, j))
    if can_slide(state, player, SLIDE_UP):
        valid_moves.append((SLIDE_UP,))
    if can_slide(state, player, SLIDE_DOWN):
        valid_moves.append((SLIDE_DOWN,))
    if can_slide(state, player, SLIDE_LEFT):
        valid_moves.append((SLIDE_LEFT,))
    if can_slide(state, player, SLIDE_RIGHT):
        valid_moves.append((SLIDE_RIGHT,))


def make_move(state, move, player):
    """
    Aplica o movimento especificado no estado atual do jogo e retorna o novo estado resultante.
    """
    new_state = [row[:] for row in state]  # cria uma cópia do estado atual
    if move[0] == PLACE_BLUE:
        new_state[move[1]][move[2]] = BLUE
    elif move[0] == PLACE_RED:
        new_state[move[1]][move[2]] = RED
    elif move[0] == PLACE_GREY:
        new_state[move[1]][move[2]] = GREY
    elif move[0] == SLIDE_UP:
        for i in range(1, 4):
            if new_state[i][move[1]] != EMPTY:
                break
            new_state[i][move[1]] = new_state[i-1][move[1]]
            new_state[i-1][move[1]] = EMPTY
    elif move[0] == SLIDE_DOWN:
        for i in range(2, -1, -1):
            if new_state[i][move[1]] != EMPTY:
                break
            new_state[i][move[1]] = new_state[i+1][move[1]]
            new_state[i+1][move[1]] = EMPTY
    elif move[0] == SLIDE_LEFT:
        for j in range(1, 4):
            if new_state[move[1]][j] != EMPTY:
                break
            new_state[move[1]][j] = new_state[move[1]][j-1]
            new_state[move[1]][j-1] = EMPTY
    elif move[0] == SLIDE_RIGHT:
        for j in range(2, -1, -1):
            if new_state[move[1]][j] != EMPTY:
                break
            new_state[move[1]][j] = new_state[move[1]][j+1]
            new_state[move[1]][j+1] = EMPTY
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

    # Verifica se algum jogador já venceu
    for player in [BLUE, RED, GREY]:
        if evaluate(state, player) == 4:
            return True

    # Se nenhuma das condições acima for atendida, o jogo não terminou
    return False


# Define a função minimax
def minimax(state, depth, alpha, beta, maximizing_player):
    """
    Executa a busca minimax até a profundidade especificada e retorna a melhor jogada possível
    para o jogador atual a partir do estado atual do jogo.
    """
    if depth == 0 or is_terminal(state):
        return None, evaluate(state, maximizing_player)

    if maximizing_player:
        max_score = float('-inf')
        best_move = None
        for move in get_valid_moves(state, maximizing_player):
            new_state = make_move(state, move, maximizing_player)
            _, score = minimax(new_state, depth-1, alpha, beta, False)
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
        for move in get_valid_moves(state, maximizing_player):
            new_state = make_move(state, move, maximizing_player)
            _, score = minimax(new_state, depth-1, alpha, beta, True)
            if score < min_score:
                min_score = score
                best_move = move
            beta = min(beta, min_score)
            if beta <= alpha:
                break
        return best_move, min_score