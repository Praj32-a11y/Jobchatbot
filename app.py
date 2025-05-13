from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define allowed keywords (can expand based on need)
allowed_keywords = [
    "resume", "cv", "interview", "job", "cover letter",
    "job search", "apply", "linkedin", "mock interview",
    "career", "skills", "experience", "recruiter", "hiring"
]

# Initialize Gemini model with job-specific instruction
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite",
    system_instruction="You are a helpful career coach that only provides advice on job seeking, resume improvement, and interview preparation."
)
chat = model.start_chat(history=[])

# Function to validate if input is job-related
def is_job_related(text):
    return any(keyword.lower() in text.lower() for keyword in allowed_keywords)

# Function to get Gemini response
def get_gemini_response(question):
    if not is_job_related(question):
        return ["I'm here to help with job preparation, resumes, and interviews. Please ask a relevant question."]
    response = chat.send_message(question, stream=True)
    return response

# Streamlit UI
st.set_page_config(page_title="Chatbot")
st.header("Job Preparation Mentor")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")

    response = get_gemini_response(input)
    if isinstance(response, list):  # For static responses
        for text in response:
            st.write(text)
            st.session_state['chat_history'].append(("Bot", text))
    else:
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
