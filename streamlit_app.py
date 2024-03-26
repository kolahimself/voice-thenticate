"""
This script implements a user interface for voice authentication using SpeechBrain.
It allows users to enroll their voice and then verify their identity with their voice.

**Author:** James Ojoawo (github.com/kolahimself)
"""

import streamlit as st
from streamlit_mic_recorder import mic_recorder
from speechbrain.inference.speaker import SpeakerRecognition
import tempfile


# **App Configuration**
st.set_page_config(
    page_title="Voice Authentication Demo"
)

# **Custom CSS**
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)


def voice_thenticate():
    """
    Displays the user interface for voice authentication demonstration.

    This function builds the Streamlit layout for voice enrollment and verification.
    """

    # Display the title and info
    st.title("voice-thenticate")
    st.markdown(
        'A demonstration of speaker verification using [SpeechBrain](https://speechbrain.github.io/).'
        ' View project source code on [GitHub](https://github.com/kolahimself/voice-thenticate).'
    )
    st.write("\n")  # Add a space for better readability

    # Section for recording initial user (owner) voice
    st.subheader("Set Up Your Voice ID")

    # def callback_a():
    #     """Plays back recorded audio associated with a given key from Streamlit session state.
    #     """
    #     if st.session_state.A_output:
    #         # Access "bytes" key within data
    #         audio_bytes_a = st.session_state.A_output["bytes"]
    #         st.audio(audio_bytes_a)

    mic_recorder(
        start_prompt="Start recording ⏺️",
        stop_prompt="Stop recording ⏹️",
        just_once=False,  # Allow multiple recordings if needed
        use_container_width=False,
        format="wav",
        key="A"
    )

    # Section for recording user's voice for verification
    st.subheader("Unlock with Your Voice")

    # def callback_b():
    #     """Plays back recorded audio associated with a given key from Streamlit session state.
    #     """
    #     if st.session_state.B_output:
    #         # Access "bytes" key within data
    #         audio_bytes_b = st.session_state.B_output["bytes"]
    #         st.audio(audio_bytes_b)

    mic_recorder(
        start_prompt="Start recording ⏺️",
        stop_prompt="Stop recording ⏹️",
        just_once=False,  # Allow multiple recordings if needed
        use_container_width=False,
        format="wav",
        key="B"
    )
    if st.session_state.A_output is not None :
        st.write(str(st.session_state.A_output["id"]))

    if st.session_state.A_output is not None and st.session_state.B_output is not None:
        st.write(str(st.session_state.A_output["id"]))
        st.write(str(st.session_state.B_output["id"]))

    # Section for verifying user's voice with SpeechBrain
    st.subheader("Verify Your Voice")

    # "Verify" button with hover text
    if st.session_state.A_output is not None and st.session_state.B_output is not None:
        st.button(
            label="Verify",
            key="C",
            help="Match your voice sample to your enrolled voice ID",
            on_click=verify(st.session_state.A_output["bytes"], st.session_state.B_output["bytes"]),
            type="primary"
        )


def verify(audio_a, audio_b) -> None:
    """
    Performs speaker verification between the two input audio recordings.

    Args:
        audio_a: Bytes representing the enrolled user's voice sample.
        audio_b: Bytes representing the user's voice for verification.
    """
    
    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir="pretrained_models/spkrec-ecapa-voxceleb"
    )
        
    # with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file_a:
    #     temp_file_a.write(audio_a)
            
    # with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file_b:
    #     temp_file_b.write(audio_b)
    # with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file_a, tempfile.NamedTemporaryFile(suffix=".wav") as temp_file_b:
    #     temp_file_a.write(audio_a)
    #     temp_file_b.write(audio_b)
    def save_audio_as_wav(audio_bytes, filename):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            return temp_file.name

    wav_path_a = save_audio_as_wav(audio_a, "audio_a.wav")
    wav_path_b = save_audio_as_wav(audio_b, "audio_b.wav")
    score, prediction = verification.verify_files(wav_path_a, wav_path_b)
    

    # Convert tensor prediction to boolean for conditional logic
    prediction_bool = prediction.item() == 1  # True if prediction is [True]
        
    if prediction_bool:
        st.success("Voice verified successfully!")
    else:
        st.error("Voice verification failed. Please try again.")


if __name__ == "__main__":
    # Call main function
    voice_thenticate()
