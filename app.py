import streamlit as st
import random
import json

# ------------------------------
# 🎨 Dynamic Background Function
# ------------------------------
def set_background(url):
    st.markdown(f"""
    <style>
    body {{
        background: url('{url}') repeat;
        background-size: cover;
        background-attachment: fixed;
        color: white;
        font-family: 'Courier New', monospace;
    }}
    div.stButton > button {{
        background-color: #00cc66;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ------------------------------
# 🌱 Game Title & Description
# ------------------------------
st.title("🌍 NASA Sustainable Farming Guessing Game")
st.markdown("""
Agriculture is at the core of the global food supply, but faces challenges from climate change and resource use.  
This game uses **NASA open data concepts** (NDVI, rainfall, soil moisture, temperature) to simulate farming challenges.  
Your mission: Guess the correct answers, learn, and improve sustainable farming knowledge! 🌱
""")

# ------------------------------
# Background GIFs
# ------------------------------
backgrounds = [
    "https://i.gifer.com/origin/3d/3d98f1ae8e1aa1d86c6d8e062c6b6f2f.gif",
    "https://i.gifer.com/origin/9b/9b6f8bda9266b0e5bb0c8a8472e3b5d2.gif",
    "https://i.gifer.com/origin/7c/7c9c1e1f8e60cdcd3cf2dfd2d0e6b6a6.gif",
    "https://i.gifer.com/origin/6f/6f8e3e5b1f5e2cf1a3c6e3b2d2d3f1a9.gif",
]

# ------------------------------
# Load Questions
# ------------------------------
with open("questions.json", "r") as f:
    questions = json.load(f)

if "questions_shuffled" not in st.session_state:
    random.shuffle(questions)
    st.session_state.questions_shuffled = questions

# ------------------------------
# Difficulty Selection
# ------------------------------
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None

if st.session_state.difficulty is None:
    st.subheader("Select Game Difficulty")
    difficulty = st.radio("Choose difficulty level:", ["Easy", "Medium", "Hard"])
    if st.button("Start Game"):
        st.session_state.difficulty = difficulty
        st.session_state.score = 0
        st.session_state.level = 1
        st.session_state.level_index = 0
        st.session_state.question_index = 0
        st.session_state.answered = False
        st.session_state.next_question = False
        st.experimental_rerun()

# ------------------------------
# Game Logic
# ------------------------------
if st.session_state.difficulty is not None:
    if st.session_state.difficulty == "Easy":
        questions_per_level = [2, 3, 3, 4, 4, 5, 5, 5, 6, 6]
    elif st.session_state.difficulty == "Medium":
        questions_per_level = [3, 5, 6, 6, 7, 7, 8, 8, 9, 10]
    else:
        questions_per_level = [4, 6, 7, 7, 8, 8, 9, 9, 10, 12]

    # Background per level
    current_level_index = st.session_state.level - 1
    if current_level_index < len(backgrounds):
        set_background(backgrounds[current_level_index])

    # Show score
    st.write(f"**Score:** {st.session_state.score}")

    if st.session_state.level <= 10:
        num_questions = questions_per_level[st.session_state.level - 1]

        if st.session_state.question_index < num_questions:
            q = st.session_state.questions_shuffled[
                st.session_state.level_index + st.session_state.question_index
            ]
            st.subheader(f"Level {st.session_state.level} — Question {st.session_state.question_index + 1}")
            st.write(q["question"])

            choice = st.radio("Choose an answer:", q["options"], key=f"q{st.session_state.level}_{st.session_state.question_index}")

            # Submit Answer
            if not st.session_state.answered:
                if st.button("Submit Answer", key=f"submit_{st.session_state.level}_{st.session_state.question_index}"):
                    if choice == q["answer"]:
                        st.success("✅ Correct!")
                        st.session_state.score += 10
                    else:
                        st.error(f"❌ Wrong. Correct answer: {q['answer']}")
                    st.session_state.answered = True

            # Next Question button
            if st.session_state.answered:
                if st.button("Next Question"):
                    st.session_state.question_index += 1
                    st.session_state.answered = False
                    st.session_state.next_question = True

            if st.session_state.next_question:
                st.session_state.next_question = False
                st.experimental_rerun()

        else:
            st.success(f"🎯 Level {st.session_state.level} Complete!")
            st.write(f"Score: {st.session_state.score}")
            if st.button("Next Level"):
                st.session_state.level_index += questions_per_level[st.session_state.level - 1]
                st.session_state.level += 1
                st.session_state.question_index = 0
                st.experimental_rerun()

    else:
        st.success("🏆 Game Over!")
        st.write(f"Your final score: {st.session_state.score}")
        if st.button("Play Again"):
            st.session_state.clear()
            st.experimental_rerun()
