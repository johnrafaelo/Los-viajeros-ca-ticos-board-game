from flask import Flask, render_template, request
import random

app = Flask(__name__)

board_dimentions = 7 * 7
no_of_bombs = 10
no_of_questions = 25
no_of_powerups = 6

def generate_pos(seed=None):
  global no_of_bombs, no_of_questions, no_of_powerups
  total = no_of_bombs + no_of_questions + no_of_powerups
  bq_total = no_of_bombs + no_of_questions

  if total > board_dimentions:
    raise ValueError(f"Too many marks for a {str(board_dimentions)} board")

  if seed is None:
    seed = random.randint(1000, 100000000)

  rng = random.Random(seed)

  blacklist = [0, 1, 7, 8, 40, 41, 47, 48]
  ipos = rng.sample(range(board_dimentions), total+len(blacklist))
  fpos = [x for x in ipos if x not in blacklist]

  bomb_pos = fpos[:no_of_bombs]
  question_pos = fpos[no_of_bombs:bq_total]
  powerup_pos = fpos[bq_total:]

  return bomb_pos, question_pos, powerup_pos, seed

@app.route("/", methods=["GET", "POST"])
def home():
  if request.method == "POST":
    seed_input = request.form.get("seed", "").strip()
    seed = int(seed_input) if seed_input else None
    bombs, questions, powerups, actual_seed = generate_pos(seed)

    return render_template(
          "index.html",
          bombs=bombs,
          questions=questions,
          powerups=powerups,
          seed=actual_seed
    )
  return render_template("index.html")

if __name__ == "__main__":
  app.run(host="127.0.0.1",
          port=5000,
          debug=False)