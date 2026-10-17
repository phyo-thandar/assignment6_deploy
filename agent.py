# agent.py

import random
import math

from checkers import (
    PLAYER_X,
    PLAYER_O,
    KING_X,
    KING_O
)


# ============================================================
# BOARD EVALUATION
# ============================================================

def evaluate_board(game, player):
    """
    Evaluate the board from the given player's point of view.

    Positive score = good for player
    Negative score = good for opponent
    """

    opponent = game.opponent(player)

    score = 0

    for row in range(8):
        for col in range(8):
            piece = game.board[row][col]

            if piece == ".":
                continue

            value = 3 if piece.isupper() else 1

            if piece.lower() == player:
                score += value

                # Small reward for controlling central squares
                if 2 <= row <= 5 and 2 <= col <= 5:
                    score += 0.2

            elif piece.lower() == opponent:
                score -= value

                if 2 <= row <= 5 and 2 <= col <= 5:
                    score -= 0.2

    # Mobility
    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(opponent))

    score += 0.1 * (player_moves - opponent_moves)

    return score


# ============================================================
# RANDOM AGENT
# ============================================================

class RandomAgent:
    """
    Easy difficulty.
    Randomly chooses one legal move.
    """

    def __init__(self, player):
        self.player = player
        self.name = "Random"

    def choose_move(self, game):
        moves = game.get_legal_moves(self.player)

        if not moves:
            return None

        return random.choice(moves)


# ============================================================
# HEURISTIC AGENT
# ============================================================

class HeuristicAgent:
    """
    Medium difficulty.

    Tries every legal move and chooses the move that gives
    the best immediate board evaluation.
    """

    def __init__(self, player):
        self.player = player
        self.name = "Heuristic"
        self.candidate_scores = []

    def choose_move(self, game):
        moves = game.get_legal_moves(self.player)

        if not moves:
            return None

        best_score = -math.inf
        best_moves = []

        self.candidate_scores = []

        for move in moves:
            game.make_move(move)

            score = evaluate_board(game, self.player)

            game.undo_move()

            self.candidate_scores.append({
                "move": move,
                "score": round(score, 2)
            })

            if score > best_score:
                best_score = score
                best_moves = [move]

            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)


# ============================================================
# MINIMAX AGENT
# ============================================================

class MinimaxAgent:
    """
    Hard difficulty.

    Uses Minimax search with Alpha-Beta pruning.
    """

    def __init__(self, player, depth=4):
        self.player = player
        self.depth = depth
        self.name = "Minimax"

        self.nodes_explored = 0
        self.cutoffs = 0
        self.candidate_scores = []

    def choose_move(self, game):
        moves = game.get_legal_moves(self.player)

        if not moves:
            return None

        self.nodes_explored = 0
        self.cutoffs = 0
        self.candidate_scores = []

        best_score = -math.inf
        best_moves = []

        alpha = -math.inf
        beta = math.inf

        for move in moves:
            game.make_move(move)

            score = self.minimax(
                game,
                self.depth - 1,
                alpha,
                beta
            )

            game.undo_move()

            self.candidate_scores.append({
                "move": move,
                "score": round(score, 2)
            })

            if score > best_score:
                best_score = score
                best_moves = [move]

            elif score == best_score:
                best_moves.append(move)

            alpha = max(alpha, best_score)

        return random.choice(best_moves)

    def minimax(self, game, depth, alpha, beta):
        self.nodes_explored += 1

        winner = game.get_winner()

        if winner == self.player:
            return 1000 + depth

        if winner == game.opponent(self.player):
            return -1000 - depth

        if game.is_draw():
            return 0

        if depth == 0:
            return evaluate_board(game, self.player)

        current_player = game.current_player
        moves = game.get_legal_moves(current_player)

        if not moves:
            return evaluate_board(game, self.player)

        # Maximizing turn
        if current_player == self.player:
            best_score = -math.inf

            for move in moves:
                game.make_move(move)

                score = self.minimax(
                    game,
                    depth - 1,
                    alpha,
                    beta
                )

                game.undo_move()

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if alpha >= beta:
                    self.cutoffs += 1
                    break

            return best_score

        # Minimizing turn
        else:
            best_score = math.inf

            for move in moves:
                game.make_move(move)

                score = self.minimax(
                    game,
                    depth - 1,
                    alpha,
                    beta
                )

                game.undo_move()

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if alpha >= beta:
                    self.cutoffs += 1
                    break

            return best_score


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":
    from checkers import MyanmarCheckers

    game = MyanmarCheckers()

    print("Testing Random Agent")
    random_agent = RandomAgent(PLAYER_X)
    print(random_agent.choose_move(game))

    print("\nTesting Heuristic Agent")
    heuristic_agent = HeuristicAgent(PLAYER_X)
    move = heuristic_agent.choose_move(game)
    print("Selected move:", move)
    print("Candidate scores:")
    for item in heuristic_agent.candidate_scores:
        print(item)

    print("\nTesting Minimax Agent")
    minimax_agent = MinimaxAgent(PLAYER_X, depth=4)
    move = minimax_agent.choose_move(game)

    print("Selected move:", move)
    print("Nodes explored:", minimax_agent.nodes_explored)
    print("Alpha-Beta cutoffs:", minimax_agent.cutoffs)

    print("Candidate scores:")
    for item in minimax_agent.candidate_scores:
        print(item)