from flask import Flask, request, redirect, url_for, jsonify, send_file

app = Flask(__name__)

# لوحة اللعب
board = [[" " for _ in range(3)] for _ in range(3)]
players = ["X", "O"]
turn = 0

# دالة للتحقق من الفوز
def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# دالة للتحقق من التعادل
def is_full(board):
    return all(board[i][j] != " " for i in range(3) for j in range(3))

# الصفحة الرئيسية
@app.route('/')
def index():
    return send_file('index.html')

# دالة لمعالجة الحركات
@app.route('/move', methods=['POST'])
def move():
    global turn
    player = players[turn % 2]
    row = int(request.form['row']) - 1
    col = int(request.form['col']) - 1

    if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == " ":
        board[row][col] = player
        if check_winner(board, player):
            return jsonify({'winner': player, 'redirect': url_for('game_over', winner=player)})
        elif is_full(board):
            return jsonify({'draw': True, 'redirect': url_for('game_over', winner='draw')})
        turn += 1
    return jsonify({'redirect': url_for('index')})

# صفحة نهاية اللعبة
@app.route('/game_over/<winner>')
def game_over(winner):
    return send_file('game_over.html')

# ملف CSS
@app.route('/style.css')
def style():
    return send_file('style.css')

# إعادة تعيين اللعبة
@app.route('/reset')
def reset():
    global board, turn
    board = [[" " for _ in range(3)] for _ in range(3)]
    turn = 0
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
