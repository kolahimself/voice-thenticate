"""
This script implements a user interface for voice authentication using SpeechBrain.
It allows users to enroll their voice and then verify their identity with their voice.

**Author:** James Ojoawo (github.com/kolahimself)
"""

import streamlit as st
import tempfile
import pyrebase
from streamlit_mic_recorder import mic_recorder
from st_audiorec import st_audiorec
from speechbrain.inference.speaker import SpeakerRecognition
import time

# **App Configuration**
def set_page_config():
    """
    Sets the page title and custom CSS for the Streamlit app.
    """
    st.set_page_config(
        page_title="Voice Authentication Demo"
    )

    # Custom CSS (optional)
    st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
                unsafe_allow_html=True)


def display_initial_app_info():
    """
    Displays the initial title, information, and formatting for the app.
    """
    # Display the title and information
    st.title("voice-thenticate")
    st.markdown(
        'A demonstration of speaker verification using [SpeechBrain](https://speechbrain.github.io/).'
        ' View project source code on [GitHub](https://github.com/kolahimself/voice-thenticate).'
    )
    st.write("\n")  # Space for better readability


def init_firebase_storage() -> pyrebase.pyrebase.Storage:
    """
    Initializes a Firebase app and returns the storage object.

    Returns:
        pyrebase.storage.Storage: The initialized Firebase storage object.
    """
    config = {
        'apiKey': "AIzaSyA6tzaUZN8hVdDa75nioEDoXWiP-Gl8FVQ",
        'authDomain': "voice-thenticate.firebaseapp.com",
        'projectId': "voice-thenticate",
        "databaseURL": "https://voice-thenticate.firebaseio.com",
        'storageBucket': "voice-thenticate.appspot.com",
        'messagingSenderId': "583252692015",
        'appId': "1:583252692015:web:9615861360f2bcc69a8ada",
        'measurementId': "G-KR9Z6EHF56",
        'serviceAccount': 'spice_cache/sitecha18afc6tnsv.json'
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    return storage
    

def fetch_firebase_data(storage) -> list:
    """
    Retrieves a list of file names within the storage folder.

    Args:
        storage (pyrebase.storage.Storage): The initialized Firebase storage object.

    Returns:
        list: A list of file names within the specified folder, or an empty list if no files are found.
    """    
    try:
        files = storage.list_files()
        file_names = [file.name.split('.')[0] for file in files]  # Extract filename without extension
        return file_names
        
    except Exception as e:
        print(f"Error fetching data from Firebase: {e}")
        return []  # Return an empty list on error
        

def display_initial_ui(reg_usernames: list, firebase_storage) -> str:
    """
    Initial authentication page, retrieves the username of the user.
    Users can either sign in or sign up

    Args:
        reg_usernames: List containing all registered voices
    """
    # Initial page state ("initial", "sign_in", or "sign_up")
    if "page" not in st.session_state:
        st.session_state.page = 0

    def switch_to_sign_in_page(): st.session_state.page = 1
    def switch_to_sign_up_page(): st.session_state.page = 2
    # if "page" not in st.session_state:
    #     st.session_state.page = 0

    # def nextpage(): st.session_state.page += 1
    # def restart(): st.session_state.page = 0

    # placeholder = st.empty()
    # st.button("Next",on_click=nextpage,disabled=(st.session_state.page > 3))

    # if st.session_state.page == 0:
    #     # Replace the placeholder with some text:
    #     placeholder.text(f"Hello, this is page {st.session_state.page}")

    # elif st.session_state.page == 1:
    #     # Replace the text with a chart:
    #     placeholder.line_chart({"data": [1, 5, 2, 6]})

    # elif st.session_state.page == 2:
    #     # Replace the chart with several elements:
    #     with placeholder.container():
    #         st.write("This is one element")
    #         st.write("This is another")
    #         st.metric("Page:", value=st.session_state.page)

    # elif st.session_state.page == 3:
    #     placeholder.markdown(r"$f(x) = \exp{\left(x^🐈\right)}$")

    # else:
    #     with placeholder:
    #         st.write("This is the end")
    #         st.button("Restart",on_click=restart)
    display_initial_app_info()
    
    # placeholders = [st.empty() for _ in range(2)]
    placeholder = st.empty()

    if st.session_state.page == 4:
        username = placeholder.text_input(label="Username", key='A1')
        col_left, col_right = st.columns(2)
        with col_left:
            sign_in_button = st.button(
                label="Sign In",
                key="A2",
                type="primary",
                use_container_width=True
            )    
        with col_right:
            sign_up_button = st.button(
                label="Sign Up",
                key="A3",
                type="primary",
                use_container_width=True
            )
        if sign_in_button:
            switch_to_sign_in_page()
            # sign_in(auth_reqs)
        elif sign_up_button:
            switch_to_sign_up_page()

    elif st.session_state.page == 1:
        st.write(st.session_state.page)
        placeholder.empty()

    elif st.session_state.page == 2:
        st.write(st.session_state.page)
        placeholder.empty()
    # # Entry text field
    # username = placeholders[0].text_input(label="Username", key='A1')
        
    # with placeholders[1]:
    #     col_left, col_right = st.columns(2)
        
    #     with col_left:
    #         sign_in_button = st.button(
    #             label="Sign In",
    #             key="A2",
    #             type="primary",
    #             use_container_width=True
    #         )
    
    #     with col_right:
    #         sign_up_button = st.button(
    #             label="Sign Up",
    #             key="A3",
    #             type="primary",
    #             use_container_width=True
    #         )

    # # Store authentication/verificaiton requirements
    # auth_reqs = {
    #     'username': username,
    #     'registered_usernames': reg_usernames,
    #     'placeholders': placeholders,
    #     'firebase_storage': firebase_storage,
    # }
    
    # if sign_in_button:
    #     sign_in(auth_reqs)
    
    # elif sign_up_button:
    #     sign_up(auth_reqs)


def sign_in(auth_reqs: dict):
    """
    Performs the sign-in processes, then directly moves to voice verification
    """
    # Unpack requirements
    username = auth_reqs['username']
    reg_usernames = auth_reqs['registered_usernames']
    placeholders = auth_reqs['placeholders']
    firebase_storage = auth_reqs['firebase_storage']
    
    if username:
        if username not in reg_usernames:
            st.error(f"Username '{username}' is not found. Please check for existing accounts or create a new one.")

        else:
            # Clear existing layout elements
            for placeholder in placeholders:
                time.sleep(0.001)
                placeholder.empty()

            # Section for recording user's voice for verification
            st.subheader("Verify Your Voice ID")

            # Download user audio from firebase for verification
            st.write('Downloading...')
            audio_a = download_audio(username, firebase_storage)
            st.write('success!')

            mic_recorder(
                start_prompt="Start recording ⏺️",
                stop_prompt="Stop recording ⏹️",
                just_once=False,  
                use_container_width=False,
                format="wav",
                key="B"
            )

            # Section for verifying user's voice with SpeechBrain
            st.subheader("Verification Result")

            if st.session_state.B_output is not None:
                # Download user audio from firebase for verification
                audio_a = download_audio(username, firebase_storage)
                
                # Verification outcome
                verify(audio_a, st.session_state.B_output["bytes"])
            
    else:
        # Handle cases where no username is entered
        st.warning("Please enter a username to continue.")

def sign_up(auth_reqs: dict):
    pass

def download_audio(username, firebase_storage):
    """
    Downloads users' audio from firebase 
    """
    path_cloud = str(username) + ".wav"
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        # Download Firebase audio to the temporary file
        firebase_storage.child(path_cloud).download(filename=temp_file.name, path=temp_file.name)
        wav_path = temp_file.name  # Store the temporary path

    return wav_path


def is_wav_file(audio):
    """
    Checks if the provided audio is a WAV file based on its extension.

    Args:
        audio: The audio data (bytes or path) to be checked.

    Returns:
        bool: True if the audio is a WAV file, False otherwise.
    """
    if isinstance(audio, str):
        return audio.lower().endswith(".wav")
    else:
        return False


def save_audio_as_wav(audio_bytes, filename):
    """
    Saves the provided audio bytes as a temporary WAV file.

    Args:
        audio_bytes (bytes): Raw audio data in bytes format.
        filename (str): Desired filename for the temporary WAV file.

    Returns:
        str: Path to the saved temporary WAV file.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(audio_bytes)
        return temp_file.name


def voice_thenticate():
    """
    Displays the user interface for voice authentication demonstration.

    This function builds the Streamlit layout for voice enrollment and verification.
    """
    # Section for recording initial user (owner) voice
    st.subheader("Set Up Your Voice ID")

    mic_recorder(
        start_prompt="Start recording ⏺️",
        stop_prompt="Stop recording ⏹️",
        just_once=False,  
        use_container_width=False,
        format="wav",
        key="A"
    )


def verify(audio_a, audio_b) -> None:
    """
    Performs speaker verification between the two input audio recordings.

    Args:
        audio_a: Either bytes representing the enrolled user's voice sample
                or the path to a WAV file containing the sample.
        audio_b: Either bytes representing the user's voice for verification
                or the path to a WAV file containing the user's voice.
    """
    # Check if audio_a is a WAV file path
    if is_wav_file(audio_a):
        wav_path_a = audio_a
    else:
        # Save audio_a as temporary WAV if it's bytes
        wav_path_a = save_audio_as_wav(audio_a, "audio_a.wav")

    # Check if audio_b is a WAV file path
    if is_wav_file(audio_b):
        wav_path_b = audio_b
    else:
        # Save audio_b as temporary WAV if it's bytes
        wav_path_b = save_audio_as_wav(audio_b, "audio_b.wav")

    # Speech Verification
    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir="pretrained_models/spkrec-ecapa-voxceleb"
    )
    score, prediction = verification.verify_files(wav_path_a, wav_path_b)

    # Convert tensor prediction to boolean for conditional logic
    prediction_bool = prediction.item() == 1  # True if prediction is tensor([True])
        
    if prediction_bool:
        st.success("✅ Voice verified successfully!")
        st.snow()
    else:
        st.error("❌ Voice verification failed. Please try again.")


if __name__ == "__main__":
    # Call page configuration function
    set_page_config()  
    
    # Connect to firebase and get reference to storage
    storage = init_firebase_storage()

    # Retrieve registered usernames
    registered_usernames = fetch_firebase_data(storage)

    # Display initial user interface
    display_initial_ui(registered_usernames, storage)
