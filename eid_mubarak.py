import streamlit as st
import time
from PIL import Image
import requests
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Eid Mubarak",
    page_icon="🌙",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        font-size: 20px;
    }
    .title {
        font-size: 50px;
        color: #2E7D32;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000000;
    }
    .message {
        font-size: 30px;
        color: #1B5E20;
        text-align: center;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# Title with animation
st.markdown('<div class="title">Eid Mubarak 🌙</div>', unsafe_allow_html=True)

# Animated message
st.markdown('<div class="message">From Nida to All of You ✨</div>', unsafe_allow_html=True)

# Decorative elements
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🌟")
with col2:
    st.markdown("### 🌙")
with col3:
    st.markdown("### ✨")

# Eid message
st.markdown("""
    ### 🕌 May this Eid bring:
    - Joy and happiness to your life
    - Peace and prosperity to your home
    - Blessings and good health to your family
    - Success and achievements in your endeavors
""")

# Decorative line
st.markdown("---")

# Animated emojis
emoji_container = st.empty()
emojis = ["🌟", "🌙", "✨", "🕌", "💫", "🎊", "🎉", "💝"]
for i in range(10):
    emoji_container.markdown(f"# {emojis[i % len(emojis)]}")
    time.sleep(0.5)

# Final message
st.markdown("""
    ### 💝 Wishing you and your family a blessed Eid filled with:
    - Love and togetherness
    - Joy and celebration
    - Peace and harmony
    - Success and prosperity
""")

# Footer
st.markdown("---")
st.markdown("### Made with ❤️ by Nida") 