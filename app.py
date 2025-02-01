from flask import Flask, request, redirect, url_for, jsonify

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
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tic-Tac-Toe</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: url('https://j.top4top.io/p_3318ufj4o1.jpg');
                background-size: cover;
                background-position: center;
            }}
            .container {{
                background-color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .board {{
                display: inline-block;
                margin-top: 20px;
                transition: transform 0.5s ease;
            }}
            .board.celebrate {{
                transform: translateY(-20px);
            }}
            .row {{
                display: flex;
            }}
            .cell {{
                width: 100px;
                height: 100px;
                border: 2px solid #000;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            .cell:hover {{
                background-color: #ddd;
            }}
            .cell[data-player="X"] {{
                background-color: rgba(255, 0, 0, 0.1);
            }}
            .cell[data-player="O"] {{
                background-color: rgba(0, 0, 255, 0.1);
            }}
            #message {{
                margin-top: 20px;
                font-size: 20px;
                color: #4CAF50;
                font-weight: bold;
                animation: celebrate 2s infinite;
            }}
            @keyframes celebrate {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Farah's Game: Tic-Tac-Toe! 🤍</h1>
            <div class="board">
                {"".join(f'''
                <div class="row">
                    {"".join(f'''
                    <div class="cell" data-row="{row}" data-col="{col}" data-player="{board[row][col]}" onclick="makeMove({row}, {col})">
                        {board[row][col]}
                    </div>
                    ''' for col in range(3))}
                </div>
                ''' for row in range(3))}
            </div>
            <div id="message"></div>
        </div>
        <script>
            function makeMove(row, col) {{
                fetch('/move', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/x-www-form-urlencoded',
                    }},
                    body: `row=${{row + 1}}&col=${{col + 1}}`
                }}).then(response => response.json())
                  .then(data => {{
                      if (data.winner) {{
                          document.getElementById('message').innerText = `Player ${{data.winner}} wins! Congratulations! 🎉`;
                          document.querySelector('.board').classList.add('celebrate');
                      }} else if (data.draw) {{
                          document.getElementById('message').innerText = "It's a draw!";
                      }}
                      window.location.href = data.redirect;
                  }});
            }}
        </script>
    </body>
    </html>
    '''

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
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Game Over</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: url('https://j.top4top.io/p_3318ufj4o1.jpg');
                background-size: cover;
                background-position: center;
            }}
            .container {{
                background-color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #4CAF50;
            }}
            a {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}
            a:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>
                { "It's a draw!" if winner == 'draw' else f'Player {winner} wins! Congratulations! 🎉' }
            </h1>
            <a href="/reset">Play Again</a>
        </div>
    </body>
    </html>
    '''

# إعادة تعيين اللعبة
@app.route('/reset')
def reset():
    global board, turn
    board = [[" " for _ in range(3)] for _ in range(3)]
    turn = 0
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
