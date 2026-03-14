# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I ran the app for the first time, the core logic was broken in multiple ways. The most obvious bug was that the game gave backwards hints (telling me to go higher when my guess was already too high). Additionally, the secret number was changing on every single button click because the Streamlit app reruns from top-to-bottom on every interaction without persisting standard variables. Finally, the app was crashing with a `TypeError` because the guess and secret were not being safely cast to integers before comparison.

## 2. How did you use AI as a teammate?

I used **GitHub Copilot** alongside **ChatGPT** to debug and expand the project.

- **Correct Suggestion:** I used Copilot's "Generate Tests" smart action to quickly scaffold advanced edge-case tests (like checking negative numbers and extremely large integers). It correctly generated the `pytest` assertions, and I verified them by running the test suite in my terminal.
- **Incorrect Suggestion:** When I asked Copilot to refactor `app.py` logic into `logic_utils.py`, it mistakenly tried to move `st.session_state` calls into the utility file. I rejected this because it violates the principle of keeping business logic independent from the UI framework, which would have ruined my ability to run headless unit tests.

## 3. Debugging and testing your fixes

I decided a bug was fixed when the logic passed isolated unit tests without the browser open, and then subsequently worked cleanly in the UI. For Challenge 1, I ran an advanced `pytest` suite that tested edge cases like `parse_guess("42.5")`. The test proved that my new code successfully rejected the decimal with a friendly error message instead of crashing. AI helped me design these tests by identifying potential breaking points (like extreme integers and empty strings) that I hadn't originally considered.

## 4. What did you learn about Streamlit and state?

I would explain Streamlit to a friend by comparing it to a very forgetful artist. Every time you press a button, the artist throws away the canvas and redraws the entire page from scratch based on the code. Because of this, normal variables are forgotten immediately. To fix this, you have to use a special memory box called `st.session_state` to store important things (like the score or the secret number) so the artist remembers them on the next redraw.

## 5. Looking ahead: your developer habits

One habit I want to reuse is separating my business logic into a pure, testable utility file (like `logic_utils.py`) separate from the user interface. Next time I work with AI, I will focus more heavily on writing docstrings *before* asking the AI to write the logic, as it helps constrain the AI to my exact expectations. This project changed the way I view AI: it is a powerful typist and brainstormer, but it fundamentally lacks architectural foresight, meaning human engineering judgment is more critical than ever.

## 🤖 Challenge 5: AI Model Comparison

To fix the initial "State Bug" (where the number kept changing), I compared **Copilot Chat (in VS Code)** to a standard browser-based LLM (**ChatGPT**).

- **Copilot** gave a much more immediate, readable code fix because it had direct context of my file via the `#file` command. It essentially wrote the exact snippet I needed to paste.
- **ChatGPT**, however, did a significantly better job explaining the *why*. It gave me a thorough, conceptual breakdown of Streamlit's execution model and `session_state`. Ultimately, Copilot was better for fast implementation, while ChatGPT was superior for foundational learning.