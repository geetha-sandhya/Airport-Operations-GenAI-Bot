import streamlit as st
import google.generativeai as genai
from google.genai import types

# ---------------- UI ----------------
st.set_page_config(page_title="Airport Bot", layout="centered")
st.title("✈️ Airport Operations Explainer Bot 🧳")

st.write("""
This bot explains airport passenger procedures like:
Check-in, Security, Boarding, Arrival, and Baggage Claim.
""")

# ---------------- API KEY INPUT ----------------
st.sidebar.title("🔐 API Settings")

api_key = st.sidebar.text_input(
    "Enter your Google AI Studio API Key",
    type="password"
)

# Stop if no API key
if not api_key:
    st.warning("Please enter your API key in the sidebar to continue.")
    st.stop()

# Initialize Gemini client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"API Key Error: {e}")
    st.stop()

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are an Airport Ground Operations Explainer Bot.

Explain ONLY airport passenger procedures such as:
- Check-in
- Security screening
- Boarding
- Arrival process
- Baggage claim

DO NOT:
- Provide flight booking
- Give ticket status
- Suggest travel decisions

If the question is unrelated, politely refuse.
"""

# Allowed topics filter
allowed_topics = [
    "check", "security", "boarding", "airport",
    "baggage", "arrival", "departure",
    "terminal", "passenger", "immigration"
]

# ---------------- USER INPUT ----------------
user_input = st.text_input(
    "Ask about airport procedures:",
    placeholder="e.g., What happens at security check?"
)

# ---------------- BUTTON ----------------
if st.button("Explain"):

    if not user_input.strip():
        st.warning("Please enter a valid question.")

    elif not any(topic in user_input.lower() for topic in allowed_topics):
        st.info("""
❗ I can only explain airport passenger procedures like:
Check-in, Security, Boarding, Arrival & Baggage Claim.

Please ask a related question. ✈️
""")

    else:
        with st.spinner("Generating response... ✨"):
            try:
                contents = [
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(
                                text=SYSTEM_PROMPT + "\nUser: " + user_input
                            )
                        ]
                    )
                ]

                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=contents
                )

                st.success(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built using Streamlit + Google Gemini API | Hackathon Project")