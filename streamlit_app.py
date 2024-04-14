"""
This script implements a user interface for voice authentication using SpeechBrain.
It allows users to enroll their voice and then verify their identity with their voice.

**Author:** James Ojoawo (github.com/kolahimself)
"""
import tempfile
import json

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from streamlit_javascript import st_javascript

import pyrebase
from speechbrain.inference.speaker import SpeakerRecognition


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
        "databaseURL": "https://voice-thenticate-default-rtdb.firebaseio.com/",
        'storageBucket': "voice-thenticate.appspot.com",
        'messagingSenderId': "583252692015",
        'appId': "1:583252692015:web:9615861360f2bcc69a8ada",
        'measurementId': "G-KR9Z6EHF56",
        'serviceAccount': 'spice_cache/sitecha18afc6tnsv.json'
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    db = firebase.database()
    return storage, db
    

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


def user_authentication(reg_users):
    """
    Initial authentication page, retrieves the username of the user.
    Users can either sign in or sign up
    """
    display_initial_app_info()
    
    def on_sign_in_click(user, reg_users):
        if user in reg_users:
            st.session_state["user"] = user
            st.session_state.user_state = 'signing_in'
        else:
            st.session_state.user_state = None
            
    def on_signup_click(user, reg_users):
        if user not in reg_users:
            st.session_state["user"] = user
            st.session_state.user_state = 'signing_up'
        else:
            st.session_state.user_state = None
            
    def on_signout_click():
        st.session_state["user"] = None
        st.session_state.user_state = None
            
    if st.session_state.setdefault("user", None) is None:
        # Entry text field
        username = st.text_input(label="Username", key='A1')
        
        if username:
            col_left, col_right = st.columns(2)
            with col_left:
                sign_in_button = st.button(label="Sign In",
                         on_click=on_sign_in_click,
                         args=(username, reg_users),
                         key="A2",
                         type="primary",
                         use_container_width=True)
            with col_right:
                sign_up_button = st.button(label="Sign Up",
                         on_click=on_signup_click, 
                         args=(username, reg_users),
                         key="A3",
                         type="primary",
                         use_container_width=True)
                
            if sign_in_button:
                st.error(f"Username '{username}' is not found. Please check for existing accounts or create a new one.")
            elif sign_up_button:
                st.error(f"Username '{username}' already exists. Please choose a different username.")
        else: 
            # Handle cases where no username is entered
            st.warning("Please enter a username to continue.")
            
    else:
        st.button("Sign Out", on_click=on_signout_click, key='A4')
        st.success(f"Welcome {st.session_state['user']}, Your voice is your key – let's confirm it's you.")


def voice_auth_sign_in(firebase_storage, db):
    """
    Voice verification for a signed in user
    """
    # Section for recording user's voice for verification
    st.subheader("Verify Your Voice ID")
    
    mic_recorder(
        start_prompt="Start recording ⏺️",
        stop_prompt="Stop recording ⏹️",
        just_once=False,  
        use_container_width=False,
        format="wav",
        key="MC_I"
    )
    # Display recording
    if st.session_state.MC_I_output is not None:
        st.audio(data=st.session_state.MC_I_output["bytes"], format="audio/wav")
        
    # Section for verifying user's voice with SpeechBrain
    st.subheader("Verification Result")

    if st.session_state.MC_I_output is not None:        
        # Download user audio from firebase for verification
        audio_a = download_audio(username=st.session_state["user"], firebase_storage=firebase_storage)
                
        # Verification outcome
        verify(audio_a, st.session_state.MC_I_output["bytes"], mode="sign_in")
        

def voice_auth_sign_up(firebase_storage, db):
    """
    Voice verification for a new user
    """
    # Section for recording initial user (owner) voice
    st.subheader("Set Up Your Voice ID")

    mic_recorder(
        start_prompt="Start recording ⏺️",
        stop_prompt="Stop recording ⏹️",
        just_once=False,  
        use_container_width=False,
        format="wav",
        key="MIC_XC"
    )
    
    if st.session_state.MIC_XC_output is not None:
        # Display recording
        st.audio(data=st.session_state.MIC_XC_output["bytes"], format="audio/wav")

    # Section for recording user's voice for verification
    st.subheader("Verify Your Voice ID")
    
    mic_recorder(
        start_prompt="Start recording ⏺️",
        stop_prompt="Stop recording ⏹️",
        just_once=False,  
        use_container_width=False,
        format="wav",
        key="MXC_CG"
    )
    # Display recording
    if st.session_state.MXC_CG_output is not None:
        st.audio(data=st.session_state.MXC_CG_output["bytes"], format="audio/wav")

    # Section for retrieving verifying user's voice with SpeechBrain
    st.subheader("Verification Result")

    if st.session_state.MIC_XC_output is not None and st.session_state.MXC_CG_output is not None:
        # Verification outcome
        verify(st.session_state.MIC_XC_output["bytes"], st.session_state.MXC_CG_output["bytes"])

        with st.form("my_form"):
            # Section for registering user info 
            st.subheader("Complete Registration details")
            
            # Recieve info from users
            user_info = {}
            user_info["username"] = st.session_state['user']
            user_info["full_name"] = st.text_input(label="Full Name", key='UI1')
            user_info["date_of_birth"] = st.text_input(label="Date of Birth", key='UI2')
            user_info["course"] = st.text_input(label="Course Taken", key='UI3')
            user_info["email"] = st.text_input(label="Email Address", key='UI4')
            user_info["address"] = st.text_input(label="Address", key='UI5')
            

            # Save info
            submitted = st.form_submit_button(label="Submit", type="primary")
            if submitted:
                # Convert owner recording to .wav
                wav_for_upload = save_audio_as_wav(st.session_state.MIC_XC_output["bytes"])

                # Upload the owner's voice recording to firebase
                upload_audio(audio_file=wav_for_upload,
                             username=st.session_state["user"],
                             firebase_storage=firebase_storage)
                
                # Upload user info to firebase storage
                # upload_json(user_info, firebase_storage)
                db.child(str(st.session_state["user"]))
                db.child(str(st.session_state["user"])).set(user_info)
        
                # Redirect to dashboard
                redirect()


def upload_audio(audio_file, username, firebase_storage):
    """
    Upload's the recorded audio to firebase as reference for signing in
    """
    path_on_cloud = str(username) + ".wav"
    firebase_storage.child(path_on_cloud).put(audio_file)


def upload_json(user_information: dict, firebase_storage):
    """
    Uploads the user data to firebase storage
    """
    # Covert dict to json, save to tmp
    tfile = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    json.dump(user_information, tfile)
    tfile.flush()
    
    # Upload to firebase storage
    path_on_cloud = str(st.session_state["user"]) + ".json"
    firebase_storage.child(path_on_cloud).put(tfile.name)


def download_audio(username, firebase_storage):
    """
    Downloads users' audio from firebase 
    """
    audio_path = str(username) + ".wav"
    firebase_storage.child(audio_path).download(filename=audio_path, path=audio_path)

    return audio_path


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


def save_audio_as_wav(audio_bytes):
    """
    Saves the provided audio bytes as a temporary WAV file.

    Args:
        audio_bytes (bytes): Raw audio data in bytes format.
    Returns:
        str: Path to the saved temporary WAV file.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(audio_bytes)
        return temp_file.name


def verify(audio_a, audio_b, mode='sign_up'):
    """
    Performs speaker verification between the two input audio recordings. Redirects to the dashboard webpage

    Args:
        audio_a: Either bytes representing the enrolled user's voice sample
                or the path to a WAV file containing the sample.
        audio_b: Either bytes representing the user's voice for verification
                or the path to a WAV file containing the user's voice.
        mode: 'sign_up' or 'sign_in'
    """
    # Check if audio_a is a WAV file path
    if is_wav_file(audio_a):
        wav_path_a = audio_a
    else:
        # Save audio_a as temporary WAV if it's bytes
        wav_path_a = save_audio_as_wav(audio_a)

    # Check if audio_b is a WAV file path
    if is_wav_file(audio_b):
        wav_path_b = audio_b
    else:
        # Save audio_b as temporary WAV if it's bytes
        wav_path_b = save_audio_as_wav(audio_b)

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
        if mode == 'sign_in':
            redirect()
        
    else:
        st.error("❌ Voice verification failed. Please try again.")

def redirect(): 
    """
    Redirects to https://vtrenderer.github.io/
    """
    dashboard_url = f"https://vtrenderer.github.io/?username={st.session_state['user']}"
    js = f'window.open("{dashboard_url}", "_blank").then(r => window.parent.location.href);'
    st_javascript(js)


if __name__ == "__main__":
    # Call page configuration function
    set_page_config()  
    
    # Connect to firebase and get reference to storage
    storage, db = init_firebase_storage()

    # Initialize session state containing context imformation in the app   
    if 'reg_users' not in st.session_state:
        st.session_state['reg_users'] = fetch_firebase_data(storage)
        
    if 'storage' not in st.session_state:
        st.session_state['storage'] = storage
        
    if 'db' not in st.session_state:
        st.session_state['db'] = db

    if 'user_state' not in st.session_state:
        st.session_state['user_state'] = None

    # Initial user authentication
    user_authentication(st.session_state.reg_users)

    # Handle voice verification when user is signing in/up
    if st.session_state.user_state == 'signing_in':
        voice_auth_sign_in(st.session_state.storage, st.session_state.db)
    elif st.session_state.user_state == 'signing_up':
        voice_auth_sign_up(st.session_state.storage, st.session_state.db)
    else:
        pass
        
    # Update reg users
    st.session_state['reg_users'] = fetch_firebase_data(storage)
