import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

def generate_poem(theme, temperature=0.9):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a poetic assistant who writes beautiful, emotional, and imaginative poetry."},
            {"role": "user", "content": f"Write a poem about: {theme}"}
        ],
        "temperature": temperature,
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

def simulate_streaming(text, delay=0.05):
    chunk_size = 20
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]
        time.sleep(delay)

st.set_page_config(page_title="AI Poetry Generator", layout="wide", page_icon="🖋️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&family=Playfair+Display&display=swap');

body {
    background: #f9f7f7;
    font-family: 'Poppins', sans-serif;
    margin: 0;
}

.main {
    background: transparent;
    max-width: 700px;
    margin: 60px auto;
    padding: 50px 40px 60px;
    border-radius: 25px;
    box-shadow: none;
    text-align: center;
}

.title {
    font-family: 'Playfair Display', serif;
    font-weight: 600;
    font-size: 3.5rem;
    color: #5e3a99;
    margin-bottom: 12px;
    text-shadow: 0 0 6px rgba(94, 58, 153, 0.25);
}

.subtitle {
    font-size: 1.2rem;
    font-weight: 300;
    color: #7b67b9;
    margin-bottom: 40px;
}

/* Remove the outer white block and borders around the input container */
div[data-baseweb="input"] {
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
    padding: 0 !important;
}

/* Style the input text box like ChatGPT minimal style */
input[type="text"] {
    background: transparent !important;
    border: 1.5px solid #c3c3c3;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 1.1rem;
    outline: none;
    width: 100%;
    transition: border-color 0.2s ease;
}

/* On focus: purple subtle border */
input[type="text"]:focus {
    border-color: #9166ff;
    background-color: #fff;
}

/* Remove form background/padding */
form {
    background: transparent !important;
    padding: 0 !important;
    margin: 0 auto !important;
    box-shadow: none !important;
}

.stButton>button {
    background-color: #9166ff;
    color: white;
    font-size: 16px;
    border-radius: 10px;
    padding: 10px 25px;
    margin-top: 10px;
    transition: background-color 0.3s ease;
    cursor: pointer;
    border: none;
}

.stButton>button:hover {
    background-color: #7c4dff;
}

.poem-box {
    background: #f4eafd;
    border-left: 8px solid #9166ff;
    padding: 30px 35px;
    margin-top: 0;
    border-radius: 25px;
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #4a2c87;
    white-space: pre-wrap;
    line-height: 1.6;
    box-shadow: 0 6px 20px rgba(145, 102, 255, 0.25);
    max-width: 580px;
    margin-left: auto;
    margin-right: auto;
}

@media (max-width: 480px) {
    .main {
        padding: 30px 20px 40px;
    }
    .title {
        font-size: 2.8rem;
    }
    .poem-box {
        font-size: 1.1rem;
        max-width: 90%;
    }
}
</style>
""", unsafe_allow_html=True)

st.sidebar.header("🎨 Customize Your Poem")
temperature = st.sidebar.slider("Creativity Level (Temperature)", 0.0, 1.0, 0.9, 0.05)

st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="title">🖋️ AI Poetry Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter a theme and watch the AI craft beautiful poetry for you.</div>', unsafe_allow_html=True)

with st.form("poem_form"):
    theme = st.text_input("", placeholder="Type a theme like 'Rainy Nights'...", label_visibility="collapsed")
    submitted = st.form_submit_button("✨ Generate Poem")

poem_placeholder = st.empty()

if submitted:
    if theme.strip():
        with st.spinner("Crafting your poem..."):
            poem_text = generate_poem(theme, temperature)
        displayed_text = ""
        for chunk in simulate_streaming(poem_text):
            displayed_text += chunk
            poem_placeholder.markdown(f'<div class="poem-box">{displayed_text}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a theme to generate a poem.")

st.markdown("</div>", unsafe_allow_html=True)

