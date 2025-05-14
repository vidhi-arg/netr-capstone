import streamlit as st
from transformers import pipeline
import re

# Title
st.title("🧠 NETR: AI-Powered Coded Speech Detector")
st.markdown("Detects and deciphers suspicious or coded language in conversations.")

# User input
user_input = st.text_area("Enter a message to analyze:", height=200)

# Load a zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Keywords that hint at coded language
suspicious_keywords = [
    "eagle", "package", "midnight", "sunrise", "rainbow", "storm", "gift", "fireworks",
    "uncle", "party", "signal", "drop", "payload", "merch", "courier"
]

def keyword_score(text):
    matches = [word for word in suspicious_keywords if word.lower() in text.lower()]
    return len(matches)

def ai_interpretation(text):
    candidate_labels = ["criminal code", "military code", "normal message"]
    result = classifier(text, candidate_labels)
    return result

if st.button("🕵️ Analyze"):
    if not user_input.strip():
        st.warning("Please enter a message.")
    else:
        score = keyword_score(user_input)
        interpretation = ai_interpretation(user_input)

        st.subheader("🔍 AI Interpretation")
        for label, score in zip(interpretation["labels"], interpretation["scores"]):
            st.write(f"**{label.title()}**: {score:.2%}")

        st.subheader("🧪 Risk Score")
        if score == 0:
            st.success("Low Risk – No suspicious patterns found.")
        elif score <= 2:
            st.warning("Moderate Risk – A few potential code words detected.")
        else:
            st.error("High Risk – Multiple coded keywords detected.")
        
        st.markdown("✅ Analysis complete.")
