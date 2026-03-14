# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
1. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
1. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
1. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
1. **Refactor & Test.** - Move the logic into `logic_utils.py`.

- Run `pytest` in your terminal.
- Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose: A web-based interactive number guessing game where a player tries to discover a randomly generated secret number within a limited amount of attempts, utilizing higher/lower hints.
- [x] Detail which bugs you found:

1. **Hint Bug:** The game told the player to go higher when the guess was already too high, and lower when the guess was too low.
1. **Type Casting Bug:** `app.py` was alternating between passing `secret` as an integer and a string, causing a TypeError loop in `check_guess`.
1. **New Game Range Bug:** Starting a new game reset the number's range to a hardcoded 1 to 100, breaking the logic for "Easy" or "Hard" difficulty limits.
1. **Score Bug:** Due to a logic error, getting a "Too High" answer on an even attempt would add 5 points to your score instead of subtracting points.
- [x] Explain what fixes you applied: I refactored all core logic out of `app.py` into `logic_utils.py` to isolate Streamlit UI from pure Python logic. In `check_guess`, I cast both parameters to integers immediately, which safely handles Streamlit's string-passing quirk, and I flipped the `>` and `<` hint strings. I also fixed the tests to unpack the returned tuple correctly.

## 📸 Demo

- [x] *(Insert your screenshot of the winning game running in your browser here!)*

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]