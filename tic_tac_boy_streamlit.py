import streamlit as st
import random

# ------------------- Page Setup -------------------
st.set_page_config(page_title="Tic-Tac-Boy AI", page_icon="🤖", layout="centered")

# ------------------- Game Initialization -------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.player_symbol = ""
    st.session_state.ai_symbol = ""
    st.session_state.turn = ""
    st.session_state.message = ""

# ------------------- AI Logic -------------------
def check_winner(board, symbol):
    for i in range(3):
        if all(cell == symbol for cell in board[i]):
            return True
        if all(board[r][i] == symbol for r in range(3)):
            return True
    if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def ai_move():
    board = st.session_state.board
    ai = st.session_state.ai_symbol
    player = st.session_state.player_symbol

    # Try to win
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = ai
                if check_winner(board, ai):
                    return
                board[r][c] = " "

    # Try to block player
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = player
                if check_winner(board, player):
                    board[r][c] = ai
                    return
                board[r][c] = " "

    # Pick random move
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = ai

# ------------------- Player Move -------------------
def make_move(row, col):
    if st.session_state.board[row][col] == " " and st.session_state.turn == "player":
        st.session_state.board[row][col] = st.session_state.player_symbol

        if check_winner(st.session_state.board, st.session_state.player_symbol):
            st.session_state.message = "🎉 You Win!"
            st.session_state.turn = "none"
            return

        elif is_draw(st.session_state.board):
            st.session_state.message = "😐 It's a Draw!"
            st.session_state.turn = "none"
            return

        # AI's turn
        st.session_state.turn = "ai"
        ai_move()

        if check_winner(st.session_state.board, st.session_state.ai_symbol):
            st.session_state.message = "😔 AI Wins!"
            st.session_state.turn = "none"
        elif is_draw(st.session_state.board):
            st.session_state.message = "😐 It's a Draw!"
            st.session_state.turn = "none"
        else:
            st.session_state.turn = "player"

        st.rerun()

# ------------------- Game Start UI -------------------
st.title("🤖 Tic-Tac-Boy AI")
st.subheader("Play against a smart AI in classic Tic-Tac-Toe")

if not st.session_state.game_started:
    st.markdown("### Choose your symbol to begin:")
    choice = st.radio("Select:", ["X", "O"], index=0, horizontal=True)

    if st.button("Start Game"):
        st.session_state.player_symbol = choice
        st.session_state.ai_symbol = "O" if choice == "X" else "X"
        st.session_state.turn = "player" if choice == "X" else "ai"
        st.session_state.game_started = True

        # If AI starts first
        if st.session_state.turn == "ai":
            ai_move()
            st.session_state.turn = "player"

        st.rerun()

# ------------------- Game Board UI -------------------
if st.session_state.game_started:
    st.markdown("### Game Board")

    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            if st.session_state.board[i][j] == " ":
                if st.session_state.turn == "player":
                    if cols[j].button(" ", key=f"{i}-{j}"):
                        make_move(i, j)
                else:
                    cols[j].button(" ", key=f"{i}-{j}", disabled=True)
            else:
                cols[j].button(st.session_state.board[i][j], key=f"{i}-{j}", disabled=True)

    # Game status
    if st.session_state.message:
        st.success(st.session_state.message)

    # Reset button
    if st.button("🔁 Restart Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
