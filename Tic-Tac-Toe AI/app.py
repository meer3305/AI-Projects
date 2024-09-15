from flask import Flask, render_template, jsonify, request, redirect, url_for
import random

app = Flask(__name__)

# Initialize the game board and variables
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'  # Player always starts as 'X'
mode = None  # No mode selected initially (welcome page)
winner_line = []

def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != ' ':
            return board[row][0], [(row, 0), (row, 1), (row, 2)]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col], [(0, col), (1, col), (2, col)]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    return None, []

def is_board_full(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

# Minimax algorithm for AI
def minimax(board, is_maximizing):
    winner, _ = check_winner(board)
    if winner == 'X':  # Player wins
        return -1
    elif winner == 'O':  # AI wins
        return 1
    elif is_board_full(board):
        return 0  # Tie

    if is_maximizing:  # AI's turn (maximize score)
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, False)
                    board[i][j] = ' '  # Undo the move
                    best_score = max(score, best_score)
        return best_score
    else:  # Player's turn (minimize score)
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, True)
                    board[i][j] = ' '  # Undo the move
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'  # AI is 'O'
                score = minimax(board, False)
                board[i][j] = ' '  # Undo the move
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        row, col = best_move
        board[row][col] = 'O'  # AI makes the best move

@app.route('/')
def welcome():
    # Welcome page that lets the user choose between modes
    return render_template('welcome.html')

@app.route('/start_game')
def start_game():
    global board, current_player, winner_line, mode
    if mode is None:
        return redirect(url_for('welcome'))  # Redirect to welcome page if no mode is selected
    board = [[' ' for _ in range(3)] for _ in range(3)]  # Reset board
    current_player = 'X'  # Player 'X' always starts first
    winner_line = []  # Reset winner line
    return render_template('index.html', board=board, current_player=current_player, mode=mode, winner_line=winner_line)
def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

@app.route('/move', methods=['POST'])
def make_move():
    global board, current_player, winner_line, mode

    data = request.get_json()
    row = data['row']
    col = data['col']

    # Check if the move is valid
    if board[row][col] == ' ':
        board[row][col] = current_player  # Place player's mark

        # Check if the current player won
        winner, winner_line = check_winner(board)
        if winner:
            return jsonify({'status': 'win', 'winner': winner, 'board': board, 'winnerLine': winner_line})

        # Check if the board is full (tie game)
        if is_board_full(board):
            return jsonify({'status': 'draw', 'board': board})  # Return 'draw' status

        # Switch to the other player
        if mode == 'pvp':  # Player vs Player mode
            current_player = 'O' if current_player == 'X' else 'X'
        elif mode == 'pvai':  # Player vs AI mode
            if current_player == 'X':  # Player's turn just ended, now AI plays
                ai_move()  # AI makes its move
                winner, winner_line = check_winner(board)
                if winner:
                    return jsonify({'status': 'win', 'winner': 'AI', 'board': board, 'winnerLine': winner_line})
                if is_board_full(board):
                    return jsonify({'status': 'draw', 'board': board})  # Return 'draw' status

            current_player = 'X'  # Player is always 'X'

    return jsonify({'status': 'continue', 'board': board, 'currentPlayer': current_player})

@app.route('/restart')
def restart():
    global board, current_player, winner_line
    board = [[' ' for _ in range(3)] for _ in range(3)]  # Reset board
    current_player = 'X'
    winner_line = []
    return redirect(url_for('start_game'))

@app.route('/set_mode/<string:new_mode>')
def set_mode(new_mode):
    global mode
    mode = new_mode  # Set the game mode ('pvp' or 'pvai')
    return redirect(url_for('start_game'))

@app.route('/home')
def home():
    return redirect(url_for('welcome'))  # Redirect to the home page

if __name__ == '__main__':
    app.run(debug=True)
