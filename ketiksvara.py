#https://github.com/stefanrmmr/streamlit-audio-recorder
import streamlit as st
import openai
from st_audiorec import st_audiorec
from io import BytesIO
import tempfile
#%%
openai.api_key = st.secrets["API_KEYS"]["OPENAI_API_KEY"]

def save_to_temp(audio_file, filetype):
    audio_data = BytesIO(audio_file)
    with tempfile.NamedTemporaryFile(suffix=f'.{filetype}', delete=False) as temp_file:
        temp_file.write(audio_data.getvalue())
    #st.write(temp_file.name)
    return temp_file

def get_transcript(audio_temp_file):
    with open(audio_temp_file.name, "rb") as audio_file:
        #response = requests.post(api_url, files={"audio": (temp_file.name, audio_file)})
        response = openai.Audio.transcribe("whisper-1", audio_file)
        st.session_state['transcription'] = response['text']
        st.session_state['transcriptions'].append(st.session_state['transcription'])

def show_transcript():
    if st.session_state['transcription'] is not None:
        st.text_area("Teks:", st.session_state['transcription'])
        st.session_state['transcription'] = None
    if len(st.session_state['transcriptions']) > 0:
        st.text_area("Seluruh teks:", "\n\n\n".join(st.session_state['transcriptions']))
#%%
st.set_page_config(
    page_title="KetikSvara",
    page_icon="🧊",
    #layout="wide",
)
# Initialization
if 'recorded_audio' not in st.session_state:
    st.session_state['recorded_audio'] = None
if 'uploaded_audio' not in st.session_state:
    st.session_state['uploaded_audio'] = None
if 'transcription' not in st.session_state:
    st.session_state['transcription'] = None
if 'transcriptions' not in st.session_state:
    st.session_state['transcriptions'] = []
#%%
st.header('KetikSvara', divider='rainbow')

tab1, tab2, tab3 = st.tabs(["Beranda", "Rekam svara", "Unggah file"])

with tab1:
    st.subheader("Ubah svaramu menjadi teks! Diketik oleh AI.🤖")
    st.text("Dapat digunakan untuk Bahasa Indonesia, Inggris, dan 54 bahasa lainnya!🤗")
    st.text("")
    st.subheader('Silakan pilih "Rekam svara" atau "Unggah svara"')
#%%
with tab2:
    st.subheader("Rekam svara")
    st.toast('Klik Izinkan apabila pop-up muncul', icon="ℹ️")
    # recorder
    wav_audio_data = st_audiorec()

    # save to session state
    st.session_state['recorded_audio'] = wav_audio_data

    # show get transcript button if audio is not empty
    if st.session_state['recorded_audio'] is not None:
        if st.button("Ubah svara menjadi teks", type="primary"):
            temp_file = save_to_temp(st.session_state['recorded_audio'], "wav")
            get_transcript(temp_file)

    show_transcript()

#%%
with tab3:
    st.subheader("Unggah svara")
    uploaded_audio = st.file_uploader("Pilih file svara",
                                      type = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"],
                                      accept_multiple_files=False)

    if uploaded_audio is not None:
        # show audio
        bytes_data = uploaded_audio.read()
        filetype = uploaded_audio.name.split(".")[-1]
        st.audio(bytes_data, format=f'audio/{filetype}')

        # save to session state
        st.session_state['uploaded_audio'] = bytes_data

        if st.button("Ubah svara menjadi teks", type="primary"):
            temp_file = save_to_temp(st.session_state['uploaded_audio'], filetype)
            get_transcript(temp_file)
    show_transcript()

#%%

