import io
import streamlit as st
from streamlit_mic_recorder import mic_recorder

# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="streamlit_audio_recorder")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# # Design change st.Audio to fixed height of 45 pixels
# st.markdown('''<style>.stAudio {height: 45px;}</style>''',
#             unsafe_allow_html=True)
# # Design change hyperlink href link color
# st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
#             unsafe_allow_html=True)  # darkmode
# st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
#             unsafe_allow_html=True)  # lightmode

def voice_thenticate():
            """
            Displays GUI components for this demonstration
            """          
            # Display the title and info
            st.title("voice-thenticate")
            st.markdown('A practical application of speaker verification using '
                        '[SpeechBrain](https://speechbrain.github.io/) - '
                        'view project source code on '
                        
                        '[GitHub](https://github.com/kolahimself/voice-thenticate)')
            st.write('\n\n')

            # Section for recording initial user (owner so to say)'s voice
            st.subheader('Set Up Your Voice ID')

            speaker_audio_a = mic_recorder(
                        start_prompt="Start recording",
                        stop_prompt="Stop recording",
                        just_once=False,
                        use_container_width=False,
                        format="wav",
                        key='A')
            
            if speaker_audio_a["bytes"] is not None:
                        # display audio data as received on the Python side
                        col_playback, col_space = st.columns([0.58,0.32])
                        with col_playback:
                                    st.audio(speaker_audio_a["bytes"], format='audio/wav')

            # # Create a BytesIO object
            # audio_buffer_a = io.BytesIO(speaker_a_audio)

            # Section recording user's voice for verification
            st.subheader('Unlock with Your Voice')

            speaker_audio_b = mic_recorder(
                        start_prompt="Start recording",
                        stop_prompt="Stop recording",
                        just_once=False,
                        use_container_width=False,
                        format="wav",
                        key='B')
            
            if speaker_audio_b["bytes"] is not None:
                        # display audio data as received on the Python side
                        col_playback, col_space = st.columns([0.58,0.32])
                        with col_playback:
                                    st.audio(speaker_audio_b["bytes"], format='audio/wav')

            # Section for verifying user's voice with SpeechBrain
            st.subheader('Verify Your Voice')

            # `Verify` button
            st.Button(
                        label="Verify",
                        key='C',
                        help='Match your voice sample to your enrolled voice ID',
                        on_click=verify(speaker_audio_a[0], speaker_audio_b[0]),
                        type="primary",
            )


def verify(audio_a, audio_b):
            """
            Callable function that performs speaker recognition between the two input audio recordings.
            """
            print(1)


if __name__ == '__main__':
    # Call main function
    voice_thenticate()
