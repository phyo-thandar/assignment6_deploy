# app.py

from flask import Flask, render_template, request, jsonify

from checkers import MyanmarCheckers, PLAYER_X, PLAYER_O
from agent import RandomAgent, HeuristicAgent, MinimaxAgent


app = Flask(__name__)

game = MyanmarCheckers()


def get_agent(difficulty):
    """
    Return the selected AI agent.
    AI always plays O.
    """

    difficulty = difficulty.lower()

    if difficulty == "easy":
        return RandomAgent(PLAYER_O)

    if difficulty == "medium":
        return HeuristicAgent(PLAYER_O)

    return MinimaxAgent(PLAYER_O, depth=4)


def game_state(extra=None):
    """
    Return current game information as JSON-ready data.
    """

    winner = game.get_winner()

    data = {
        "board": game.board,
        "current_player": game.current_player,
        "winner": winner,
        "draw": game.is_draw(),
        "game_over": game.is_game_over()
    }

    if extra:
        data.update(extra)

    return data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state")
def state():
    return jsonify(game_state())


@app.route("/reset", methods=["POST"])
def reset():
    global game

    game = MyanmarCheckers()

    return jsonify(game_state())


@app.route("/move", methods=["POST"])
def move():
    """
    Human X makes a move.
    Then AI O responds.
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing request data"}), 400

    if game.is_game_over():
        return jsonify({"error": "Game is already over"}), 400

    if game.current_player != PLAYER_X:
        return jsonify({"error": "It is not the human player's turn"}), 400

    difficulty = data.get("difficulty", "hard")

    path = data.get("path")

    if not path or len(path) < 2:
        return jsonify({"error": "Invalid move path"}), 400

    path = [tuple(position) for position in path]

    legal_moves = game.get_legal_moves(PLAYER_X)

    selected_move = None

    for legal_move in legal_moves:
        if legal_move["path"] == path:
            selected_move = legal_move
            break

    if selected_move is None:
        return jsonify({"error": "Illegal move"}), 400

    game.make_move(selected_move)

    if game.is_game_over():
        return jsonify(game_state())

    ai = get_agent(difficulty)

    ai_move = ai.choose_move(game)

    if ai_move:
        game.make_move(ai_move)

    extra = {
        "ai_move": ai_move,
        "ai_name": ai.name
    }

    if isinstance(ai, HeuristicAgent):
        extra["candidate_scores"] = ai.candidate_scores

    if isinstance(ai, MinimaxAgent):
        extra["candidate_scores"] = ai.candidate_scores
        extra["nodes_explored"] = ai.nodes_explored
        extra["cutoffs"] = ai.cutoffs

    return jsonify(game_state(extra))


@app.route("/legal-moves", methods=["GET"])
def legal_moves():
    moves = game.get_legal_moves(game.current_player)

    return jsonify({
        "player": game.current_player,
        "moves": moves
    })


if __name__ == "__main__":
    app.run(debug=True)