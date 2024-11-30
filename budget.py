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

# Define users and their passwords
USER_CREDENTIALS = {
    "sid": "cin123",
    "vin": "cin234",
    "bala": "cin467",
    "shiv": "cin555"
}

# Fetch the API key from Streamlit Secrets
os.environ['GROQ_API_KEY'] = st.secrets["GROQ_API_KEY"]

# Initialize Groq API client
client = Groq()

@st.cache_resource
def load_whisper_model():
    """
    Loads the Whisper model.
    Returns:
        The loaded Whisper model.
    """
    print("Loading Whisper model...")
    return whisper.load_model("base")

whisper_model = load_whisper_model()

def transcribe_audio(audio_file):
    """
    Transcribes audio using Whisper and returns the text.
    Args:
        audio_file (BytesIO): Uploaded audio file.
    Returns:
        str: Transcribed text from the audio.
    """
    temp_audio_path = "temp_audio.wav"
    with open(temp_audio_path, "wb") as f:
        f.write(audio_file.getbuffer())

    # Transcribe the audio file
    print(f"Transcribing audio: {temp_audio_path}")
    result = whisper_model.transcribe(temp_audio_path, fp16=False)
    transcription = result["text"]

    # Clean up the temporary file
    os.remove(temp_audio_path)
    print("Transcription completed.")
    return transcription

def analyze_transcription(transcription):
    """
    Sends the transcription to Groq for medical analysis.
    Args:
        transcription (str): Text from the transcription.
    Returns:
        str: Groq's analysis.
    """
    prompt = f"""
    The following is a conversation between a doctor and a patient:
    {transcription}

    Based on this conversation, provide:
    1. A possible prognosis for the patient.
    2. A detailed diagnosis of the condition.
    3. Medication recommendations or treatments for the patient.
    """
    print("Sending transcription to Groq for analysis...")

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a medical assistant AI with expertise in prognosis, diagnosis, and medication recommendations."},
            {"role": "user", "content": prompt}
        ]
    )
    analysis = response.choices[0].message.content
    print("Groq analysis received.")
    return analysis

# Streamlit App Setup
st.title("Doctor-Patient Conversation Analysis")

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Authenticate"):
        if username_input in USER_CREDENTIALS and USER_CREDENTIALS[username_input] == password_input:
            st.session_state.authenticated = True
            st.session_state.username = username_input
            st.success(f"Hi, {username_input}! You are now authenticated.")
        else:
            st.error("Invalid username or password. Please try again.")
else:
    # Main App Logic After Authentication
    st.subheader(f"Welcome, {st.session_state.username}!")
    st.write("Upload an audio file to transcribe and analyze a doctor-patient conversation.")

    # Load user-specific histories
    user_histories = load_user_histories()
    if st.session_state.username not in user_histories:
        user_histories[st.session_state.username] = []

    # File uploader for audio files
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "m4a"])
    if uploaded_file is not None:
        # Step 1: Transcribe the audio
        with st.spinner("Transcribing the audio..."):
            transcription = transcribe_audio(uploaded_file)

        # Display the transcription
        st.subheader("Transcription:")
        st.write(transcription)

        # Step 2: Analyze the transcription
        with st.spinner("Analyzing the transcription..."):
            analysis = analyze_transcription(transcription)

        # Display the medical analysis
        st.subheader("Medical Analysis:")
        st.write(analysis)

        # Save to user-specific history
        user_histories[st.session_state.username].append({"transcription": transcription, "analysis": analysis})
        save_user_histories(user_histories)

    # Display user-specific history
    st.subheader("Your Past Analyses:")
    for i, record in enumerate(user_histories[st.session_state.username][::-1], start=1):  # Show most recent first
        st.write(f"**Analysis {i}:**")
        st.write(f"- **Transcription:** {record['transcription']}")
        st.write(f"- **Analysis:** {record['analysis']}")
        st.write("---")

    # Logout Option
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.success("You have been logged out.")
