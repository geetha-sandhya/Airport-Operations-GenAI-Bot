import streamlit as st
import google.generativeai as genai

# ---------------- UI ----------------
st.set_page_config(page_title="Airport Bot", page_icon="✈️")
st.title("✈️ Airport Ground Operations Bot")

# Sidebar for API key
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# Configure API
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please enter your API key to continue")

# ---------------- Chat Input ----------------
user_input = st.text_input("Ask about airport procedures:")

# ---------------- Logic ----------------
if user_input and api_key:
    
    # Restrict to airport-related questions
    prompt = f"""
    You are an Airport Operations Assistant.

    Answer ONLY questions related to:
    - Airport procedures
    - Boarding
    - Security check
    - Check-in
    - Baggage

    If the question is unrelated, say:
    "I can only answer airport-related queries."

    Question: {user_input}
    """

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        st.success(response.text)

    except Exception as e:
        st.error("Error generating response. Please check API key or try again.")