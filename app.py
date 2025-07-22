import streamlit as st
import numpy as np
from PIL import Image
from utils import detect_emotion
from spotify import get_songs

# Page setup
st.set_page_config(page_title="FeelBeats - AI Music", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Override Clear photo hover color */
    button[title="Clear photo"] {
        color: #9333ea !important;
    }
    button[title="Clear photo"]:hover {
        background-color: #f3e8ff !important;
        color: #6b21a8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Camera input
img_file = st.camera_input("")

# Process image if available
if img_file:
    image = Image.open(img_file)
    
    image_np = np.array(image)
    with st.spinner("🔍 Detecting Emotion..."):
        emotion = detect_emotion(image_np)

    if emotion and emotion != "No Face Detected":
        st.markdown(f"<h3 style='text-align:center;'>Detected Emotion: <span style='color:#9333ea'>{emotion}</span></h3>", unsafe_allow_html=True)
        st.subheader("🎵 Recommended Songs:")
        songs = get_songs(emotion)
        for song in songs:
            st.markdown(
                f"<div style='background-color:#ede9fe;padding:10px;border-radius:10px;margin-bottom:10px;'>🔊 "
                f"<a href='{song['url']}' target='_blank'>{song['name']}</a></div>",
                unsafe_allow_html=True)
    else:
        st.markdown('<div style="background-color:#f3e8ff; color:#6b21a8; padding:10px; border-radius:8px; font-weight:bold; text-align:center;">⚠️ No face detected. Please try again.</div>', unsafe_allow_html=True)
