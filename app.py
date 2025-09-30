from flask import Flask, request, jsonify, render_template_string, send_from_directory
import random
import os

app = Flask(__name__)

choices = ["rock", "paper", "scissors"]

def get_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "You win!"
    else:
        return "Computer wins!"

# Route to serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Rock Paper Scissors</title>
  <link rel="icon" href="{{ url_for('favicon') }}" type="image/x-icon">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #2c3e50, #3498db);
      color: white;
      text-align: center;
      height: 100vh;
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .container {
      background: rgba(0, 0, 0, 0.6);
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 8px 15px rgba(0,0,0,0.5);
    }
    h1 {
      margin-bottom: 20px;
    }
    .buttons button {
      background: #3498db;
      border: none;
      color: white;
      padding: 15px 25px;
      margin: 10px;
      border-radius: 10px;
      font-size: 18px;
      cursor: pointer;
      transition: background 0.3s;
    }
    .buttons button:hover {
      background: #1abc9c;
    }
    #result-box {
      margin-top: 20px;
    }
    #result {
      font-size: 24px;
      margin-top: 10px;
    }
    #play-again {
      margin-top: 20px;
      padding: 10px 20px;
      font-size: 16px;
      cursor: pointer;
      display: none;
      border: none;
      border-radius: 8px;
      background: #e67e22;
      color: white;
      transition: background 0.3s;
    }
    #play-again:hover {
      background: #d35400;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Rock Paper Scissors</h1>
    <div class="buttons">
      <button onclick="play('rock')">✊ Rock</button>
      <button onclick="play('paper')">✋ Paper</button>
      <button onclick="play('scissors')">✌️ Scissors</button>
    </div>
    <div id="result-box">
      <p id="player"></p>
      <p id="computer"></p>
      <h2 id="result"></h2>
    </div>
    <button id="play-again" onclick="resetGame()">Play Again</button>
  </div>

  <script>
    async function play(choice) {
      const response = await fetch("/play", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({choice})
      });
      const data = await response.json();
      document.getElementById("player").innerText = "You chose: " + data.player;
      document.getElementById("computer").innerText = "Computer chose: " + data.computer;
      document.getElementById("result").innerText = data.result;
      document.getElementById("play-again").style.display = "inline-block";
    }

    function resetGame() {
      document.getElementById("player").innerText = "";
      document.getElementById("computer").innerText = "";
      document.getElementById("result").innerText = "";
      document.getElementById("play-again").style.display = "none";
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/play", methods=["POST"])
def play_route():
    player_choice = request.json["choice"]
    computer_choice = random.choice(choices)
    result = get_winner(player_choice, computer_choice)
    return jsonify({
        "player": player_choice,
        "computer": computer_choice,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)
