import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
    
    def expand(self):
        for move in self.state.get_moves():
            child_state = self.state.make_move(move)
            child_node = Node(child_state, parent=self)
            self.children.append(child_node)
    
    def select_child(self, exploration_constant=1.4):
        log_total_visits = math.log(sum(child.visits for child in self.children))
        best_score = float("-inf")
        best_child = None
        for child in self.children:
            exploitation_score = child.value / child.visits
            exploration_score = exploration_constant * math.sqrt(log_total_visits / child.visits)
            uct_score = exploitation_score + exploration_score
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child
    
    def update(self, reward):
        self.visits += 1
        self.value += reward
        if self.parent:
            self.parent.update(reward)
    
    def is_leaf(self):
        return len(self.children) == 0
    
class State:
    def __init__(self, board):
        self.board = board
    
    def get_moves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    continue
                moves.append((i, j))
        return moves
    
    def make_move(self, move):
        i, j = move
        new_board = [row[:] for row in self.board]
        new_board[i][j] = 1
        return State(new_board)
    
    def is_terminal(self):
        return self.get_winner() is not None
    
    def get_winner(self):
        for i in range(len(self.board)):
            row = self.board[i]
            if row[0] != 0 and row.count(row[0]) == len(row):
                return row[0]
        for j in range(len(self.board[0])):
            column = [self.board[i][j] for i in range(len(self.board))]
            if column[0] != 0 and column.count(column[0]) == len(column):
                return column[0]
        diagonal1 = [self.board[i][i] for i in range(len(self.board))]
        if diagonal1[0] != 0 and diagonal1.count(diagonal1[0]) == len(diagonal1):
            return diagonal1[0]
        diagonal2 = [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]
        if diagonal2[0] != 0 and diagonal2.count(diagonal2[0]) == len(diagonal2):
            return diagonal2[0]
        if all(self.board[i][j] != 0 for i in range(len(self.board)) for j in range(len(self.board[0]))):
            return 0
        return None

class MCTS:
    def __init__(self, exploration_constant=1.4):
        self.exploration_constant = exploration_constant
    
    def search(self, initial_state, num_simulations):
        root = Node(initial_state)
        for i in range(num_simulations):
            node = root
            state = initial_state
            # Select
            while not node.is_leaf():
                node = node.select_child(self.exploration_constant)
                move = node.state.last_move
                state = state.make_move(move)
            # Expand
            if not state.is_terminal():
                node.expand()
                # Randomly select a child
                node = random.choice(node.children)
                state = state.make_move(node.state.last_move)
            # Simulate
            while not state.is_terminal():
                moves = state.get_moves()
                move = random.choice(moves)
                state = state.make_move(move)
            # Backpropagate
            winner = state.get_winner()
            while node is not None:
                if winner == 0:
                    reward = 0.5
                elif winner == node.state.current_player:
                    reward = 1
                else:
                    reward = 0
                node.update(reward)
                node = node.parent
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.state.last_move


def get_score(state):
    if state.is_terminal():
        winner = state.get_winner()
        if winner == 'A':
            return (1, -1)
        elif winner == 'C':
            return (-1, 1)
        else:
            return (0, 0)
    
    scores = {'A': 0, 'C': 0}
    for i in range(len(state.matrix)):
        for j in range(len(state.matrix[i])):
            if isinstance(state.matrix[i][j], dict):
                scores[state.matrix[i][j]['cor']] += state.matrix[i][j]['valor']
    
    return (scores['A'], scores['C'])

tab3 = [
    [{'cor': 'V', 'valor' : 2}, {'cor': 'A', 'valor' : 2},  {'cor': 'C', 'valor' : 2}, {'cor': 'C', 'valor' : 1}],
    [{'cor': 'C', 'valor' : 1}, 0, 0,0],
    [0, 0, 0,0],
    [0, 0, 0,0]
    ]

initial_state = State(tab3)
mcts = MCTS(exploration_constant=1.4)
best_move = mcts.search(initial_state, 1000)
print("Melhor jogada: ", best_move)



def minimax_coop(state, depth, alpha, beta, maximizing_player, is_cooperative, opc):
    """
    Executa a busca minimax até a profundidade especificada e retorna a melhor jogada possível
    para o jogador atual a partir do estado atual do jogo.
    """
    if depth <= 0 or is_terminal(state, is_cooperative):
        return None, evaluate(state, is_cooperative)

    if maximizing_player:
        max_score = float('-inf')
        best_move = None
        valids = get_valid_moves(state, is_cooperative)
        for move in valids:
            new_state = make_move(state, move)
            _, score = minimax(new_state, depth-1, alpha, beta, False, True, )
            if score > max_score:
                max_score = score
                best_move = move
            alpha = max(alpha, max_score)
            if beta <= alpha:
                break
        return best_move, max_score
    else:
        if is_cooperative:
            # Jogador 2 é cooperativo
            min_score = float('inf')
            best_move = None
            valids = get_valid_moves(state, is_cooperative)
            for move in valids:
                new_state = make_move(state, move)
                _, score = minimax(new_state, depth-1, alpha, beta, True, is_cooperative, opc)
                if score < min_score:
                    min_score = score
                    best_move = move
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return best_move, min_score
        else:
            # Jogador 2 é egoísta
            max_score = float('-inf')
            best_move = None
            valids = get_valid_moves(state, is_cooperative)
            for move in valids:
                new_state = make_move(state, move)
                _, score = minimax(new_state, depth-1, alpha, beta, True, is_cooperative)
                if score > max_score:
                    max_score = score
                    best_move = move
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return best_move, max_score