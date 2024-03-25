import tempfile
import streamlit as st
from st_audiorec import st_audiorec

# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="streamlit_audio_recorder")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
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

            # Call an instance of the audio recorder
            speaker_a_audio = st_audiorec()
            
            if speaker_a_audio is not None:
                        # display audio data as received on the Python side
                        col_playback, col_space = st.columns([0.58,0.32])
                        with col_playback:
                                    st.audio(speaker_a_audio, format='audio/wav')
                                    
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                        temp_file.write(wav_audio_data)
                        temp_file_path = temp_file.name
                        st.success(f"Audio saved to {temp_file_path}")

            # Section for verifying user's voice
            st.subheader('Verify Your Voice')


if __name__ == '__main__':
    # Call main function
    voice_thenticate()
