# checkers.py

BOARD_SIZE = 8

EMPTY = "."
PLAYER_X = "x"   # Human / White
PLAYER_O = "o"   # AI / Black

KING_X = "X"
KING_O = "O"

# Project-defined draw rule because the assignment does not specify one.
DRAW_LIMIT = 40


class MyanmarCheckers:

    def __init__(self):
        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = PLAYER_X
        self.no_capture_moves = 0
        self.history = []
        self.setup_board()

    # ---------------------------------------------------------
    # Board setup
    # ---------------------------------------------------------

    def setup_board(self):
        for row in range(3):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = PLAYER_O

        for row in range(5, 8):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = PLAYER_X

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def inside_board(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def opponent(self, player):
        return PLAYER_O if player.lower() == PLAYER_X else PLAYER_X

    def belongs_to_player(self, piece, player):
        return piece != EMPTY and piece.lower() == player.lower()

    def is_king(self, piece):
        return piece in (KING_X, KING_O)

    # ---------------------------------------------------------
    # Normal movement
    # ---------------------------------------------------------

    def get_simple_moves(self, row, col):
        piece = self.board[row][col]
        moves = []

        # Flying king: any distance diagonally until blocked.
        if self.is_king(piece):
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                r, c = row + dr, col + dc

                while self.inside_board(r, c) and self.board[r][c] == EMPTY:
                    moves.append({
                        "path": [(row, col), (r, c)],
                        "captures": []
                    })
                    r += dr
                    c += dc

            return moves

        # Men move one diagonal square forward.
        directions = [(-1, -1), (-1, 1)] if piece == PLAYER_X else [
            (1, -1), (1, 1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc

            if self.inside_board(r, c) and self.board[r][c] == EMPTY:
                moves.append({
                    "path": [(row, col), (r, c)],
                    "captures": []
                })

        return moves

    # ---------------------------------------------------------
    # Capture generation
    # ---------------------------------------------------------

    def get_capture_moves(self, row, col):
        piece = self.board[row][col]
        results = []

        self._search_captures(
            row, col, piece,
            [(row, col)],
            [],
            results
        )

        return results

    def _search_captures(self, row, col, piece, path, captures, results):
        if self.is_king(piece):
            found = self._search_king_captures(
                row, col, piece, path, captures, results
            )
        else:
            found = self._search_man_captures(
                row, col, piece, path, captures, results
            )

        if not found and captures:
            results.append({
                "path": path,
                "captures": captures
            })

    def _search_man_captures(self, row, col, piece, path, captures, results):
        """
        Myanmar draughts men may capture forward or backward.
        """
        found = False
        enemy = self.opponent(piece.lower())

        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            mid_r, mid_c = row + dr, col + dc
            land_r, land_c = row + 2 * dr, col + 2 * dc

            if not self.inside_board(land_r, land_c):
                continue

            middle = self.board[mid_r][mid_c]

            if (
                middle != EMPTY
                and middle.lower() == enemy
                and self.board[land_r][land_c] == EMPTY
            ):
                found = True

                self.board[row][col] = EMPTY
                self.board[mid_r][mid_c] = EMPTY
                self.board[land_r][land_c] = piece

                self._search_captures(
                    land_r,
                    land_c,
                    piece,
                    path + [(land_r, land_c)],
                    captures + [(mid_r, mid_c)],
                    results
                )

                self.board[land_r][land_c] = EMPTY
                self.board[mid_r][mid_c] = middle
                self.board[row][col] = piece

        return found

    def _search_king_captures(self, row, col, piece, path, captures, results):
        """
        Flying king:
        searches diagonally until it sees an enemy.
        It may land on any empty square beyond that enemy.
        """
        found = False
        enemy = self.opponent(piece.lower())

        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr, col + dc
            enemy_pos = None

            while self.inside_board(r, c):

                cell = self.board[r][c]

                if cell == EMPTY:
                    if enemy_pos is not None:
                        found = True

                        er, ec = enemy_pos
                        captured_piece = self.board[er][ec]

                        self.board[row][col] = EMPTY
                        self.board[er][ec] = EMPTY
                        self.board[r][c] = piece

                        self._search_captures(
                            r,
                            c,
                            piece,
                            path + [(r, c)],
                            captures + [(er, ec)],
                            results
                        )

                        self.board[r][c] = EMPTY
                        self.board[er][ec] = captured_piece
                        self.board[row][col] = piece

                    r += dr
                    c += dc
                    continue

                # Friendly piece blocks the diagonal.
                if cell.lower() == piece.lower():
                    break

                # First enemy may be jumped.
                if cell.lower() == enemy and enemy_pos is None:
                    enemy_pos = (r, c)
                    r += dr
                    c += dc
                    continue

                # Second occupied square blocks capture.
                break

        return found

    # ---------------------------------------------------------
    # Legal moves
    # ---------------------------------------------------------

    def get_legal_moves(self, player=None):
        if player is None:
            player = self.current_player

        captures = []
        simple_moves = []

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]

                if not self.belongs_to_player(piece, player):
                    continue

                captures.extend(self.get_capture_moves(row, col))
                simple_moves.extend(self.get_simple_moves(row, col))

        # Must Capture variant.
        if captures:
            # Myanmar rule: maximum number of captures must be taken.
            max_captures = max(len(move["captures"]) for move in captures)

            return [
                move for move in captures
                if len(move["captures"]) == max_captures
            ]

        return simple_moves

    # ---------------------------------------------------------
    # Make / undo move
    # ---------------------------------------------------------

    def make_move(self, move):
        legal_moves = self.get_legal_moves(self.current_player)

        if move not in legal_moves:
            return False

        self.history.append({
            "board": [row[:] for row in self.board],
            "current_player": self.current_player,
            "no_capture_moves": self.no_capture_moves
        })

        path = move["path"]
        captures = move["captures"]

        start_row, start_col = path[0]
        end_row, end_col = path[-1]

        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = EMPTY

        for row, col in captures:
            self.board[row][col] = EMPTY

        # Promotion occurs after the complete move.
        if piece == PLAYER_X and end_row == 0:
            piece = KING_X

        elif piece == PLAYER_O and end_row == BOARD_SIZE - 1:
            piece = KING_O

        self.board[end_row][end_col] = piece

        if captures:
            self.no_capture_moves = 0
        else:
            self.no_capture_moves += 1

        self.current_player = self.opponent(self.current_player)

        return True

    def undo_move(self):
        if not self.history:
            return False

        state = self.history.pop()

        self.board = [row[:] for row in state["board"]]
        self.current_player = state["current_player"]
        self.no_capture_moves = state["no_capture_moves"]

        return True

    # ---------------------------------------------------------
    # Game state
    # ---------------------------------------------------------

    def count_pieces(self, player):
        return sum(
            self.belongs_to_player(piece, player)
            for row in self.board
            for piece in row
        )

    def get_winner(self):
        if self.count_pieces(PLAYER_X) == 0:
            return PLAYER_O

        if self.count_pieces(PLAYER_O) == 0:
            return PLAYER_X

        if not self.get_legal_moves(self.current_player):
            return self.opponent(self.current_player)

        return None

    def is_draw(self):
        return self.no_capture_moves >= DRAW_LIMIT

    def is_game_over(self):
        return self.get_winner() is not None or self.is_draw()

    def clone(self):
        new_game = MyanmarCheckers()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        new_game.no_capture_moves = self.no_capture_moves
        new_game.history = []
        return new_game

    # ---------------------------------------------------------
    # Terminal display
    # ---------------------------------------------------------

    def print_board(self):
        print("\n   0 1 2 3 4 5 6 7")
        print("  -----------------")

        for row in range(BOARD_SIZE):
            print(row, "|", " ".join(self.board[row]))

        print("\nCurrent player:", self.current_player)


# -------------------------------------------------------------
# Simple test
# -------------------------------------------------------------

if __name__ == "__main__":
    game = MyanmarCheckers()

    game.print_board()

    print("X pieces:", game.count_pieces(PLAYER_X))
    print("O pieces:", game.count_pieces(PLAYER_O))
    print("Available moves:", len(game.get_legal_moves()))
    print("Winner:", game.get_winner())
    print("Draw:", game.is_draw())
    print("Game over:", game.is_game_over())