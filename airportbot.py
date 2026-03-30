import streamlit as st
import google.generativeai as genai

# ---------------- UI ----------------
st.set_page_config(page_title="Airport Bot", page_icon="✈️")
st.title("✈️ Airport Ground Operations Chatbot")

st.markdown("Ask me anything about airport procedures ✈️")

# Sidebar for API key
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if not api_key:
    st.warning("⚠️ Please enter your API key to continue")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# ---------------- Chat Input ----------------
user_input = st.text_input("Your Question:")

# ---------------- Airport Filter ----------------
def is_airport_related(query):
    keywords = [
        "airport", "flight", "boarding", "security",
        "check-in", "baggage", "luggage", "terminal",
        "gate", "immigration", "customs"
    ]
    return any(word in query.lower() for word in keywords)

# ---------------- Response Logic ----------------
if user_input:

    if not is_airport_related(user_input):
        st.error("❌ I can only answer airport-related queries.")
    
    else:
        try:
            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""
            You are an expert Airport Operations Assistant.

            Give clear, step-by-step answers about airport procedures.

            Question: {user_input}
            """

            response = model.generate_content(prompt)

            if response and hasattr(response, "text"):
                st.success(response.text)
            else:
                st.warning("⚠️ No response generated. Try again.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")