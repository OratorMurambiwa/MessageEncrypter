import os
import io
import json
import random
import tempfile
import zipfile
import streamlit as st
from pydub import AudioSegment
from mutagen import File as MutagenFile

# ---------- STREAMLIT UI SETUP ----------
st.set_page_config(page_title="Message Encryptor & Decryptor", layout="centered")

st.markdown(
    """
    <style>
        html, body, [class*="css"] {
            background-color: #000000 !important;
            color: #00FF41 !important;
            font-family: 'Courier New', monospace !important;
        }
        .stApp {
            background-color: #000000 !important;
            color: #00FF41 !important;
        }
        h1, h2, h3, h4, h5 {
            color: #00FF41 !important;
            text-shadow: 0 0 10px #00FF41;
        }
        .stTextInput>div>div>input, .stTextArea textarea, .stNumberInput input {
            background-color: #001900 !important;
            color: #00FF41 !important;
            border: 1px solid #00FF41 !important;
        }
        .stButton>button {
            background-color: #001900 !important;
            color: #00FF41 !important;
            border: 1px solid #00FF41 !important;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #00FF41 !important;
            color: #000000 !important;
            box-shadow: 0 0 10px #00FF41;
        }
        .stDownloadButton>button {
            background-color: #001900 !important;
            color: #00FF41 !important;
            border: 1px solid #00FF41 !important;
        }
        .stDownloadButton>button:hover {
            background-color: #00FF41 !important;
            color: #000 !important;
        }
        .stRadio>div>label, .stSlider label {
            color: #00FF41 !important;
        }
        audio {
            filter: drop-shadow(0 0 4px #00FF41);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Message Encryptor & Decryptor")

# ---------- CORE FUNCTIONS ----------
def detect_format(file_path):
    audio_file = MutagenFile(file_path)
    if not audio_file or not audio_file.mime:
        return None
    mime = audio_file.mime[0]
    if "wav" in mime:
        return "wav"
    elif "mp3" in mime:
        return "mp3"
    elif "mp4" in mime or "m4a" in mime or "aac" in mime:
        return "mp4"
    return None

def chunk_audio(sound, chunk_ms):
    return [sound[i:i+chunk_ms] for i in range(0, len(sound), chunk_ms)]

def segment_shuffle(sound, key, chunk_ms=500):
    chunks = chunk_audio(sound, chunk_ms)
    order = list(range(len(chunks)))
    random.seed(key)
    random.shuffle(order)
    shuffled = [chunks[i] for i in order]
    meta = {"order": order, "chunk_ms": chunk_ms, "n_chunks": len(chunks)}
    return sum(shuffled), meta

def segment_unshuffle(sound, meta):
    chunk_ms = meta["chunk_ms"]
    n_chunks = meta["n_chunks"]
    order = meta["order"]
    chunks = [sound[i:i+chunk_ms] for i in range(0, chunk_ms*n_chunks, chunk_ms)]
    if len(chunks) < len(order):
        order = order[:len(chunks)]
    inverse_order = [0] * len(order)
    for i, o in enumerate(order):
        inverse_order[o] = i
    unshuffled = [chunks[i] for i in inverse_order]
    return sum(unshuffled)

# ---------- MODE SELECTION ----------
mode_type = st.radio(
    "Choose Function:",
    ["Text Encryption/Decryption", "Audio Encryption/Decryption"],
    horizontal=True
)

# ---------- TEXT ----------
if mode_type == "Text Encryption/Decryption":
    st.subheader("Text Encryption/Decryption")
    characterset = "abcdefghijklmnopqrstuvwxyz0123456789!?/,.:;+=-<>@#$%^&*"
    num_char = len(characterset)
    mode = st.radio("Select Mode:", ("Encrypt", "Decrypt"), horizontal=True)
    message = st.text_area("Enter your message here:", height=150)
    key = st.number_input("Enter the key (integer):", min_value=1, step=1)

    def encrypt_message(message, key):
        result = ""
        for i in message:
            if i == " ":
                result += " "
            else:
                index = characterset.find(i.lower())
                if index != -1:
                    result += characterset[(index + key) % num_char]
        return result

    def decrypt_message(message, key):
        result = ""
        for i in message:
            if i == " ":
                result += " "
            else:
                index = characterset.find(i.lower())
                if index != -1:
                    result += characterset[(index - key) % num_char]
        return result

    if st.button("RUN ENCRYPTION/DECRYPTION"):
        if not message:
            st.warning("Please enter a message.")
        else:
            res = encrypt_message(message, key) if mode == "Encrypt" else decrypt_message(message, key)
            st.success("Process complete!")
            st.text_area("Result:", value=res, height=150)
            st.code(res, language="text")

# ---------- AUDIO ----------
else:
    st.subheader("Audio Encryption/Decryption")
    mode = st.radio("Select Mode:", ("Encrypt", "Decrypt"), horizontal=True)
    uploaded_file = st.file_uploader("Upload an audio file:", type=["wav", "mp3", "m4a"])
    key = st.number_input("Enter the key (integer):", min_value=1, step=1, key="audio_key")
    chunk_ms = st.slider("Chunk size (ms):", min_value=200, max_value=2000, value=800, step=100)

    if uploaded_file:
        st.audio(uploaded_file)

        if mode == "Encrypt" and st.button("START ENCRYPTION"):
            tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]).name
            with open(tmp_path, "wb") as f:
                f.write(uploaded_file.read())

            fmt = detect_format(tmp_path) or "wav"
            sound = AudioSegment.from_file(tmp_path, format=fmt)

            encrypted_sound, meta = segment_shuffle(sound, key, chunk_ms)
            out_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            encrypted_sound.export(out_wav, format="wav")
            out_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            AudioSegment.from_wav(out_wav).export(out_mp3, format="mp3")

            meta_path = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
            with open(meta_path, "w") as f:
                json.dump(meta, f)

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                zipf.write(out_mp3, arcname="encrypted_audio.mp3")
                zipf.write(meta_path, arcname="encryption_meta.json")
            zip_buffer.seek(0)

            st.success("Audio encrypted successfully!")
            st.audio(out_mp3)
            st.download_button(
                label="Download Encrypted Package (.zip)",
                data=zip_buffer,
                file_name="encrypted_package.zip",
                mime="application/zip"
            )

        elif mode == "Decrypt":
            meta_file = st.file_uploader("Upload encryption meta (.json):", type=["json"])
            if meta_file and st.button("START DECRYPTION"):
                try:
                    meta = json.load(meta_file)
                except:
                    st.error("Invalid JSON meta file.")
                    st.stop()

                tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]).name
                with open(tmp_path, "wb") as f:
                    f.write(uploaded_file.read())

                fmt = detect_format(tmp_path) or "wav"
                sound = AudioSegment.from_file(tmp_path, format=fmt)
                decrypted_sound = segment_unshuffle(sound, meta)
                out_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
                decrypted_sound.export(out_wav, format="wav")
                out_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                AudioSegment.from_wav(out_wav).export(out_mp3, format="mp3")

                st.success("Audio decrypted successfully!")
                st.audio(out_mp3)
                st.download_button("Download Decrypted Audio (MP3)", open(out_mp3, "rb"), file_name="decrypted_audio.mp3")
