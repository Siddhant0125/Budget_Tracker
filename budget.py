# import streamlit as st
# from groq import Groq
# import whisper
# import os
# # from io import BytesIO

# # Fetch the API key from Streamlit Secrets
# import os
# os.environ['GROQ_API_KEY'] = st.secrets["GROQ_API_KEY"]
# # print(f"API Key: {api_key}")
# # Initialize Groq API client
# client = Groq()

# @st.cache_resource
# def load_whisper_model():
#     """
#     Loads the Whisper model.
#     Returns:
#         The loaded Whisper model.
#     """
#     print("Loading Whisper model...")
#     return whisper.load_model("base")

# whisper_model = load_whisper_model()

# def transcribe_audio(audio_file):
#     """
#     Transcribes audio using Whisper and returns the text.
#     Args:
#         audio_file (BytesIO): Uploaded audio file.
#     Returns:
#         str: Transcribed text from the audio.
#     """
#     temp_audio_path = "temp_audio.wav"
#     with open(temp_audio_path, "wb") as f:
#         f.write(audio_file.getbuffer())

#     # Transcribe the audio file
#     print(f"Transcribing audio: {temp_audio_path}")
#     result = whisper_model.transcribe(temp_audio_path, fp16=False)
#     transcription = result["text"]

#     # Clean up the temporary file
#     os.remove(temp_audio_path)
#     print("Transcription completed.")
#     return transcription



# def analyze_transcription(transcription):
#     """
#     Sends the transcription to Groq for medical analysis.
#     Args:
#         transcription (str): Text from the transcription.
#     Returns:
#         str: Groq's analysis.
#     """
#     prompt = f"""
#     The following is a conversation between a doctor and a patient:
#     {transcription}

#     Based on this conversation, provide:
#     1. A possible prognosis for the patient.
#     2. A detailed diagnosis of the condition.
#     3. Medication recommendations or treatments for the patient.
#     """
#     print("Sending transcription to Groq for analysis...")

#     response = client.chat.completions.create(model="llama3-8b-8192",
#     messages=[
#     {"role": "system", "content": "You are a medical assistant AI with expertise in prognosis, diagnosis, and medication recommendations."},
#     {"role": "user", "content": prompt}
#     ]
#     )
#     analysis = response.choices[0].message.content
#     print("Groq analysis received.")
#     return analysis

# # Streamlit App Setup
# st.title("Doctor-Patient Conversation Analysis")
# st.write("Upload an audio file to transcribe and analyze a doctor-patient conversation.")

# # File uploader for audio files
# uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "m4a"])
# if uploaded_file is not None:
#     # Step 1: Transcribe the audio
#     with st.spinner("Transcribing the audio..."):
#         transcription = transcribe_audio(uploaded_file)

#     # Display the transcription
#     st.subheader("Transcription:")
#     st.write(transcription)

#     # Step 2: Analyze the transcription
#     with st.spinner("Analyzing the transcription..."):
#         analysis = analyze_transcription(transcription)

#     # Display the medical analysis
#     st.subheader("Medical Analysis:")
#     st.write(analysis)




import streamlit as st
from groq import Groq
import whisper
import os
import json

# File to store user-specific histories
USER_HISTORY_FILE = "user_histories.json"

# Initialize the user history file if not present
if not os.path.exists(USER_HISTORY_FILE):
    with open(USER_HISTORY_FILE, "w") as file:
        json.dump({}, file)

# Load user histories from the file
def load_user_histories():
    with open(USER_HISTORY_FILE, "r") as file:
        return json.load()

# Save user histories to the file
def save_user_histories(histories):
    with open(USER_HISTORY_FILE, "w") as file:
        json.dump(histories, file)

# Simulated AI authentication function
def ai_authenticate(username, password):
    predefined_users = {
        "sid": {"password": "sid1", "role": "doctor"},
        "vin": {"password": "vin2", "role": "user"},
        "shiv": {"password": "shiv3", "role": "user"},
        "bala": {"password": "bala4", "role": "user"},
    }

    if username in predefined_users and predefined_users[username]["password"] == password:
        return {"authenticated": True, "role": predefined_users[username]["role"]}
    else:
        return {"authenticated": False, "role": None}

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

whisper_model = load_whisper_model()

def transcribe_audio(audio_file):
    temp_audio_path = "temp_audio.wav"
    with open(temp_audio_path, "wb") as f:
        f.write(audio_file.getbuffer())
    result = whisper_model.transcribe(temp_audio_path, fp16=False)
    os.remove(temp_audio_path)
    return result["text"]

def analyze_transcription(transcription):
    prompt = f"""
    The following is a conversation between a doctor and a patient:
    {transcription}

    Based on this conversation, provide:
    1. A possible prognosis for the patient.
    2. A detailed diagnosis of the condition.
    3. Medication recommendations or treatments for the patient.
    """
    return f"Analysis result for transcription: {transcription}"

# Streamlit Chat-Based Interface
st.title("Chat-Based Role Authentication with History")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.authenticated = False
    st.session_state.role = None

def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

# Initial AI prompt
if not st.session_state.chat_history:
    add_message("assistant", "Hello! Please enter your username:")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "assistant":
        st.write(f"**Assistant:** {message['content']}")
    else:
        st.write(f"**You:** {message['content']}")

# User input
user_input = st.text_input("Type your message:", key="chat_input")
if user_input:
    add_message("user", user_input)

    if not st.session_state.authenticated:
        # Authentication flow
        if len(st.session_state.chat_history) == 2:  # After first user input
            st.session_state.username = user_input
            add_message("assistant", "Got it! Now, please enter your password:")
        elif len(st.session_state.chat_history) == 4:  # After second user input
            auth_response = ai_authenticate(st.session_state.username, user_input)
            if auth_response["authenticated"]:
                st.session_state.authenticated = True
                st.session_state.role = auth_response["role"]
                add_message(
                    "assistant",
                    f"Welcome, {st.session_state.username}! You are authenticated as a {st.session_state.role}.",
                )
            else:
                add_message("assistant", "Authentication failed. Please refresh and try again.")
    else:
        # Main functionality
        if st.session_state.role == "doctor":
            if "upload_prompt" not in st.session_state:
                add_message("assistant", "You can now upload an audio file for transcription and analysis.")
                st.session_state.upload_prompt = True

            uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg", "m4a"])
            if uploaded_file is not None:
                with st.spinner("Transcribing the audio..."):
                    transcription = transcribe_audio(uploaded_file)
                add_message("assistant", f"Transcription: {transcription}")

                with st.spinner("Analyzing the transcription..."):
                    analysis = analyze_transcription(transcription)
                add_message("assistant", f"Analysis: {analysis}")

                # Save history
                user_histories = load_user_histories()
                if st.session_state.username not in user_histories:
                    user_histories[st.session_state.username] = []
                user_histories[st.session_state.username].append(
                    {"transcription": transcription, "analysis": analysis}
                )
                save_user_histories(user_histories)
        else:
            add_message("assistant", "You do not have permission to upload and analyze conversations.")

