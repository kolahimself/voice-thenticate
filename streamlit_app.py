import io
import streamlit as st
from streamlit_mic_recorder import mic_recorder


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

    speaker_audio_a = mic_recorder(
        start_prompt="Start recording",
        stop_prompt="Stop recording",
        just_once=False,  # Allow multiple recordings if needed
        use_container_width=False,
        format="wav",
        key="A",
    )

    if speaker_audio_a is not None:
        # Display audio data for playback
        col_playback, col_space = st.columns([0.58, 0.32])
        with col_playback:
            st.audio(speaker_audio_a["bytes"], format="audio/wav")

    # Section for recording user's voice for verification
    st.subheader("Unlock with Your Voice")

    speaker_audio_b = mic_recorder(
        start_prompt="Start recording",
        stop_prompt="Stop recording",
        just_once=False,  # Allow multiple recordings if needed
        use_container_width=False,
        format="wav",
        key="B",
    )

    if speaker_audio_b is not None:
        # Display audio data for playback
        col_playback, col_space = st.columns([0.58, 0.32])
        with col_playback:
            st.audio(speaker_audio_b["bytes"], format="audio/wav")

    # Section for verifying user's voice with SpeechBrain
    st.subheader("Verify Your Voice")

    # "Verify" button with hover text
    if st.button(
        label="Verify",
        key="C",
        help="Match your voice sample to your enrolled voice ID",
        on_click=verify(speaker_audio_a["bytes"], speaker_audio_b["bytes"]),
        type="primary",
    ):
        # Handle successful button click (replace with verification logic)
        st.success("Voice verified successfully!")  # Placeholder for verification result


def verify(audio_a: bytes, audio_b: bytes) -> None:
    """
    Performs speaker recognition between the two input audio recordings.

    This function should be implemented to use SpeechBrain for voice verification
    between the enrolled audio (`audio_a`) and the verification audio (`audio_b`).
    It currently just prints a placeholder message.

    Args:
        audio_a: Bytes representing the enrolled user's voice sample.
        audio_b: Bytes representing the user's voice for verification.

    Returns:
        None
    """

    print("Performing speaker verification...")  # Placeholder message
    # Implement SpeechBrain logic for verification here


if __name__ == "__main__":
    # Call main function
    voice_thenticate()
