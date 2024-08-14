import chess
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('/Users/ardapalit/Desktop/chess/chessmodel2.keras')

def fen_to_matrix(fen):
    rows = fen.split(' ')[0].split('/')
    board = np.zeros((8, 8))
    piece_to_int = {
        'r': -4, 'n': -3, 'b': -2, 'q': -5, 'k': -6, 'p': -1,
        'R': 4, 'N': 3, 'B': 2, 'Q': 5, 'K': 6, 'P': 1
    }
    for i, row in enumerate(rows):
        col = 0
        for char in row:
            if char.isdigit():
                col += int(char)
            else:
                board[i, col] = piece_to_int[char]
                col += 1
    return board

def negamax(board, depth, alpha, beta, color):
    if depth == 0 or board.is_game_over():
        fen = board.fen()
        board_matrix = fen_to_matrix(fen).reshape(-1, 8, 8, 1)
        eval = color * model.predict(board_matrix)[0][0]
        return eval, None

    max_eval = -np.inf
    best_move = None

    for move in board.legal_moves:
        board.push(move)
        eval, _ = negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()

        if eval > max_eval:
            max_eval = eval
            best_move = move

        alpha = max(alpha, eval)
        if alpha >= beta:
            break

    return max_eval, best_move

board = chess.Board()


while not board.is_game_over():
    if board.turn:

        print(board)
        move = input("Hamleyi giriniz: ")
        board.push(chess.Move.from_uci(move))
    else:
        print(f"Bilgisayar düşünüyor...")
        eval, best_move = negamax(board, depth=2, alpha=-np.inf, beta=np.inf, color=1)
        adjusted_eval = eval
        board.push(best_move)
        print(f"Bilgisayarın hamlesi: {best_move}")
        print(f"Olası hamlenin ouanı: {adjusted_eval}")

print("Şah mat!")
print(board.result())
