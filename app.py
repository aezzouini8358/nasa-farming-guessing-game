import streamlit as st
import random
import json

# 🌱 Game Title
st.title("🌍 NASA Sustainable Farming Guessing Game")

# 📜 Background
st.markdown("""
Agriculture is at the core of the global food supply, but faces challenges from climate change and resource use.  
This game uses **NASA open data concepts** (NDVI, rainfall, soil moisture, temperature) to simulate farming challenges.  
Your mission: Guess the correct answers, learn, and improve sustainable farming knowledge! 🌱
""")

# Load questions from JSON
with open("questions.json", "r") as f:
    questions = json.load(f)

# Shuffle questions
random.shuffle(questions)

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# Game loop
if st.session_state.q_index < len(questions):
    q = questions[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index+1}: {q['question']}")

    choice = st.radio("Choose an answer:", q["options"], key=f"q{st.session_state.q_index}")

    if st.button("Submit"):
        if choice == q["answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 10
        else:
            st.error(f"❌ Wrong. Correct answer: {q['answer']}")
        st.session_state.q_index += 1
        st.experimental_rerun()
else:
    st.success("🎉 Game Over!")
    st.write(f"Your final score: {st.session_state.score} / {len(questions)*10}")

    if st.button("Play Again"):
        st.session_state.score = 0
        st.session_state.q_index = 0
        random.shuffle(questions)
        st.experimental_rerun()
