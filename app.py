import streamlit as st
import random
import json

# 🌱 Game Title
st.title("🌍 NASA Sustainable Farming Guessing Game")

# 🎮 Animated Pixel Background
st.markdown("""
<style>
body {
    background: url('https://i.gifer.com/origin/3d/3d98f1ae8e1aa1d86c6d8e062c6b6f2f.gif') repeat;
    background-size: cover;
    color: white;
    font-family: 'Courier New', monospace;
}
div.stButton > button {
    background-color: #00cc66;
    color: white;
    font-weight: bold;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# 📜 Game description
st.markdown("""
Agriculture is at the core of the global food supply, but faces challenges from climate change and resource use.  
This game uses **NASA open data concepts** (NDVI, rainfall, soil moisture, temperature) to simulate farming challenges.  
Your mission: Guess the correct answers, learn, and improve sustainable farming knowledge! 🌱
""")

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

# Shuffle questions once
if "questions_shuffled" not in st.session_state:
    random.shuffle(questions)
    st.session_state.questions_shuffled = questions

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "level_index" not in st.session_state:
    st.session_state.level_index = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "submit_clicked" not in st.session_state:
    st.session_state.submit_clicked = False

questions_per_level = [3, 5, 6, 6, 7, 7, 8, 8, 9, 10]

# Game loop
if st.session_state.level <= 10:
    num_questions = questions_per_level[st.session_state.level - 1]

    if st.session_state.question_index < num_questions:
        q = st.session_state.questions_shuffled[st.session_state.level_index + st.session_state.question_index]
        st.subheader(f"Level {st.session_state.level} — Question {st.session_state.question_index + 1}")

        st.write(q["question"])
        choice = st.radio("Choose an answer:", q["options"], key=f"q{st.session_state.level}_{st.session_state.question_index})

        if st.button("Submit Answer"):
            st.session_state.submit_clicked = True

        if st.session_state.submit_clicked:
            if choice == q["answer"]:
                st.success("✅ Correct!")
                st.session_state.score += 10
            else:
                st.error(f"❌ Wrong. Correct answer: {q['answer']}")

            st.session_state.question_index += 1
            st.session_state.submit_clicked = False
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
        st.session_state.score = 0
        st.session_state.level = 1
        st.session_state.level_index = 0
        st.session_state.question_index = 0
        random.shuffle(questions)
        st.session_state.questions_shuffled = questions
        st.experimental_rerun()
