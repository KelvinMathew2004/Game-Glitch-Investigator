"""
Game Logic Utilities

This module contains the core business logic for the Number Guessing Game.
It is separated from the UI (Streamlit) to ensure it is highly testable
and adheres to PEP 8 professional linting standards.
"""

def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """
    Determine the inclusive numerical range based on the selected difficulty.

    Args:
        difficulty (str): The chosen difficulty level ('Easy', 'Normal', 'Hard').

    Returns:
        tuple[int, int]: A tuple containing the (low, high) bounds for the secret number.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """
    Parse and validate user input into an integer guess.

    Args:
        raw (str): The raw string input provided by the user.

    Returns:
        tuple[bool, int | None, str | None]: A tuple containing a success boolean, 
        the parsed integer (if successful), and an error message (if applicable).
    """
    if not raw or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            return False, None, "Please enter a whole number, not a decimal."
        value = int(raw)
    except ValueError:
        return False, None, "That is not a valid number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """
    Compare the player's guess to the secret number and determine the outcome.

    Args:
        guess (int): The player's parsed integer guess.
        secret (int): The target secret number.

    Returns:
        tuple[str, str]: A tuple containing the outcome key ('Win', 'Too High', 'Too Low')
        and the corresponding user-friendly hint message.
    """
    try:
        guess_val = int(guess)
        secret_val = int(secret)
    except (ValueError, TypeError):
        return "Error", "Invalid input types."

    if guess_val == secret_val:
        return "Win", "🎉 Correct!"

    if guess_val > secret_val:
        return "Too High", "📉 Go LOWER!"
    
    return "Too Low", "📈 Go HIGHER!"


def get_temperature_hint(guess: int, secret: int) -> str:
    """
    Calculate how close the guess is to the secret and return a Hot/Cold emoji.

    Args:
        guess (int): The player's guess.
        secret (int): The target secret number.

    Returns:
        str: An emoji representing temperature (proximity to the secret).
    """
    distance = abs(guess - secret)
    if distance == 0:
        return "🎯"
    elif distance <= 5:
        return "🥵 BOILING!"
    elif distance <= 10:
        return "🔥 HOT!"
    elif distance <= 20:
        return "🟡 WARM"
    else:
        return "❄️ COLD"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Calculate and update the player's score based on the guess outcome.

    Args:
        current_score (int): The player's score before this guess.
        outcome (str): The outcome of the guess ('Win', 'Too High', 'Too Low').
        attempt_number (int): The number of attempts used so far.

    Returns:
        int: The new calculated score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ["Too High", "Too Low"]:
        return current_score - 5

    return current_score