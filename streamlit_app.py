import streamlit as st
# from st_audiorec import st_audiorec

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
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode

def voice_thenticate():
            """
            Displays GUI components for this demonstration
            """          
            # Display the title and info
            st.title("voice-thenticate")
            st.markdown('A practical application of speaker verification using SpeechBrain'
                        '[SpeechBrain](https://speechbrain.github.io/) - '
                        'view project source code on '
                        
                        '[GitHub](https://github.com/kolahimself/voice-thenticate)')
            st.write('\n\n')


if __name__ == '__main__':
    # Call main function
    voice_thenticate()
