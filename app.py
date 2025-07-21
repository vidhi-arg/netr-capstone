import streamlit as st
import os
import requests

# ---- SETUP ----

st.set_page_config(page_title="NETR - Networked Evaluator of Threat Rhetoric", layout="centered")
st.title("🕊️ NETR")
st.subheader("Networked Evaluator of Threat Rhetoric")

st.markdown(
    "NETR is an AI-powered simulator that analyzes language in political, extremist, and criminal contexts to estimate threat levels, "
    "generate chaos scores, and recommend countermeasures — aligned with **UN SDG 16: Peace, Justice, and Strong Institutions**."
)

with st.sidebar:
    st.header("How to Use")
    st.markdown(
        "- Paste a message, transcript, or scenario.\n"
        "- Choose a context: Political, Extremist, or Crime.\n"
        "- Click **Analyze** to simulate threat evaluation."
    )
    st.markdown("---")
    st.markdown("**Built by:** Vidhi Agarwal 🇮🇳  \n**Powered by:** OpenRouter")

# ---- INPUT ----

input_text = st.text_area("🔍 Paste the message or speech segment below:", height=200)

context = st.selectbox(
    "📂 Context Type:",
    options=["Select", "Political", "Extremist", "Organized Crime"]
)

analyze_button = st.button("🔎 Analyze")

# ---- OPENROUTER CONFIG ----

api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")
api_url = "https://openrouter.ai/api/v1/chat/completions"
model = "openrouter/gpt-4"  # you can switch to claude-3, mistral, etc.

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_threat_analysis(prompt):
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"⚠️ Error: {response.status_code} - {response.text}"

# ---- ANALYSIS LOGIC ----

def build_prompt(text, context_type):
    return f"""
You are NETR, a chaos-aware AI trained in geopolitical threat rhetoric.

Context: {context_type}
Input Message: {text}

Step 1: Rate the language from 0 to 10 on the following:
- Escalation
- Threat to peace
- Manipulation tactics
- Call to action or violence

Step 2: Give a 'Chaos Score' out of 100 — summarizing overall destabilization risk.

Step 3: Suggest counter-narratives or peace-building responses.

Format:
Threat Ratings:
- Escalation: X/10
- Threat to Peace: Y/10
- Manipulation: Z/10
- Call to Action: A/10

💥 Chaos Score: XX/100

🛡️ Counter-strategy:
[your answer here]
"""

# ---- OUTPUT ----

if analyze_button:
    if not input_text.strip():
        st.error("Please enter some text to analyze.")
    elif context == "Select":
        st.error("Please select a context.")
    elif not api_key:
        st.error("OpenRouter API key is missing.")
    else:
        with st.spinner("Analyzing with NETR..."):
            prompt = build_prompt(input_text, context)
            result = get_threat_analysis(prompt)
            st.markdown("---")
            st.markdown("### 📊 NETR Threat Analysis")
            st.markdown(result)
            st.markdown("---")
            st.success("Analysis complete.")

