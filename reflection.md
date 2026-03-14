# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I ran the app for the first time, the UI loaded but the underlying mechanics were confusing. If I intentionally guessed a number higher than the secret, the game incorrectly told me to "Go HIGHER!", which meant the greater/less than signs were reversed. Additionally, the `update_score` logic was broken because guessing incorrectly on an even turn actually rewarded me with +5 points, making the scoring system erratic.

## 2. How did you use AI as a teammate?

I used Copilot to help navigate and quickly isolate errors in the codebase. An example of a correct AI suggestion was when it helped me figure out why `pytest` was failing; it correctly pointed out that `check_guess` returns a tuple, but my tests were trying to assert equality against a string, so I needed to unpack the tuple in my tests. An incorrect suggestion happened when I asked the AI to fix `app.py`; instead of keeping the game logic pure, the AI tried to insert `st.session_state` calls directly into `check_guess` inside of `logic_utils.py`, which would have completely broken my ability to run headless Pytests.

## 3. Debugging and testing your fixes

I decided a bug was genuinely fixed when I could pass a unit test without needing the Streamlit browser open. I ran the `test_guess_too_high` pytest, and it confirmed that `check_guess(60, 50)` successfully returned the string "Too High", proving my logic flow was repaired. AI helped me design the testing structure by autocompleting the assertion statements based on my function parameters, making the unit testing process significantly faster.

## 4. What did you learn about Streamlit and state?

I would explain Streamlit to a friend by saying it works like a flipbook that redraws the whole page every time you interact with it (like clicking a button). Because it completely runs the Python file from top to bottom on every click, regular variables get wiped out instantly. To fix this, you have to use a special dictionary called `st.session_state`, which acts like a vault to remember important data (like the secret number) between page redraws.

## 5. Looking ahead: your developer habits

One habit I want to reuse is separating my business logic (like math and string formatting) away from my UI logic (like Streamlit text boxes and buttons). I will also be much more careful to review the exact type of data functions return before writing tests. This project changed the way I think about AI-generated code by showing me that AI is great at writing code that *looks* right, but often fundamentally fails at basic logic and edge cases, meaning human oversight is mandatory.