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
# 📜 Background GIFs for Each Level
# ------------------------------
backgrounds = [
    "https://i.gifer.com/origin/3d/3d98f1ae8e1aa1d86c6d8e062c6b6f2f.gif",  # Level 1
    "https://i.gifer.com/origin/9b/9b6f8bda9266b0e5bb0c8a8472e3b5d2.gif",  # Level 2
    "https://i.gifer.com/origin/7c/7c9c1e1f8e60cdcd3cf2dfd2d0e6b6a6.gif",  # Level 3
    "https://i.gifer.com/origin/6f/6f8e3e5b1f5e2cf1a3c6e3b2d2d3f1a9.gif",  # Level 4
    "https://i.gifer.com/origin/5e/5e8e6e4b8f8b9d6a3c9f5b3c2d2e8a2d.gif",  # Level 5
    "https://i.gifer.com/origin/4d/4d7f8f6a9b9c2d1f3b6a8e7d6c5b2a1e.gif",  # Level 6
    "https://i.gifer.com/origin/3b/3b9f6e7a8b7c9d1f6e4b2c3a1d5e6f7a.gif",  # Level 7
    "https://i.gifer.com/origin/2a/2a6e7f8a9b8c7d6e5a4b3c2d1f0a9e8b.gif",  # Level 8
    "https://i.gifer.com/origin/1c/1c8f7e6a5b4c3d2e1f0a9b8c7d6e5f4a.gif",  # Level 9
    "https://i.gifer.com/origin/0b/0b7a8f6e5d4c3b2a1f0e9d8c7b6a5f4e.gif"   # Level 10
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
# Game State Initialization
# ------------------------------
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

# ------------------------------
# Apply Dynamic Background
# ------------------------------
current_level_index = st.session_state.level - 1
if current_level_index < len(backgrounds):
    set_background(backgrounds[current_level_index])
else:
    set_background(backgrounds[0])

# ------------------------------
# Game Loop
# ------------------------------
if st.session_state.level <= 10:
    num_questions = questions_per_level[st.session_state.level - 1]

    if st.session_state.question_index < num_questions:
        q = st.session_state.questions_shuffled[st.session_state.level_index + st.session_state.question_index]
        st.subheader(f"Level {st.session_state.level} — Question {st.session_state.question_index + 1}")
        st.write(q["question"])

        choice = st.radio("Choose an answer:", q["options"], key=f"q{st.session_state.level}_{st.session_state.question_index}")

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
