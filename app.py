import random
import os
import streamlit as st
import pandas as pd

from logic_utils import (
    get_range_for_difficulty, 
    parse_guess, 
    check_guess, 
    update_score,
    get_temperature_hint
)

# --- High Score Logic (Challenge 2) ---
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    current_high = load_high_score()
    if score > current_high:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
        return True
    return False

# --- App Setup ---
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="wide")

st.title("🎮 Game Glitch Investigator")
st.caption("Now fully repaired with Advanced UI, Hot/Cold Mechanics, and High Scores!")

# --- Sidebar UI ---
st.sidebar.header("⚙️ Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# High Score Display
current_high_score = load_high_score()
st.sidebar.metric("🏆 All-Time High Score", current_high_score)

# --- State Initialization ---
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []
if "detailed_history" not in st.session_state:
    st.session_state.detailed_history = [] # For Challenge 4 Summary Table

# --- Main Interaction ---
col_main, col_info = st.columns([2, 1])

with col_main:
    st.subheader("Make a guess")
    raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        submit = st.button("Submit Guess 🚀", use_container_width=True)
    with btn_col2:
        new_game = st.button("New Game 🔁", use_container_width=True)
    with btn_col3:
        show_hint = st.checkbox("Show higher/lower hint", value=True)

    if new_game:
        st.session_state.attempts = 0
        st.session_state.secret = random.randint(low, high) 
        st.session_state.score = 0
        st.session_state.status = "playing"
        st.session_state.history = []
        st.session_state.detailed_history = []
        st.rerun()

    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success("You already won. Start a new game to play again.")
        else:
            st.error("Game over. Start a new game to try again.")
        st.stop()

    if submit:
        st.session_state.attempts += 1
        ok, guess_int, err = parse_guess(raw_guess)

        if not ok:
            st.session_state.history.append(raw_guess)
            st.error(err)
            st.session_state.attempts -= 1 # Don't penalize for bad typing
        else:
            st.session_state.history.append(guess_int)
            outcome, message = check_guess(guess_int, st.session_state.secret)
            temp_hint = get_temperature_hint(guess_int, st.session_state.secret)

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            # Record for history table
            st.session_state.detailed_history.append({
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Result": message.replace("🎉 Correct!", "Win"),
                "Proximity": temp_hint
            })

            # Challenge 4: Enhanced UI output
            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                st.success(f"🎉 You won! The secret was {st.session_state.secret}.")
                
                # Check for high score
                if save_high_score(st.session_state.score):
                    st.success(f"🌟 NEW HIGH SCORE: {st.session_state.score}! 🌟")
            else:
                if show_hint:
                    if outcome == "Too High":
                        st.warning(f"{message} | {temp_hint}")
                    else:
                        st.info(f"{message} | {temp_hint}")

                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(f"💀 Out of attempts! The secret was {st.session_state.secret}.")

    # Move current state info below logic processing so it updates immediately
    st.progress((attempt_limit - st.session_state.attempts) / attempt_limit)
    st.info(
        f"🎯 Guess a number between **{low} and {high}**. \n"
        f"⏳ Attempts left: **{attempt_limit - st.session_state.attempts}** | "
        f"🪙 Score: **{st.session_state.score}**"
    )

# --- Challenge 4: Summary Table Sidebar ---
with st.sidebar:
    st.divider()
    st.subheader("📊 Session History")
    if st.session_state.detailed_history:
        df = pd.DataFrame(st.session_state.detailed_history)
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.caption("No guesses yet.")

    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)