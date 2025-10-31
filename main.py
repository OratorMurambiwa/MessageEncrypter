import streamlit as st
from pydub import AudioSegment
import numpy as np
import tempfile
import io

characterset = ("abcdefghijklmnopqrstuvwxyz0123456789!?/,.:;+=-<>@#$%^&*")
num_char = len(characterset)

def encrypt_message(message, key):
    encrypted_message = ""
    for i in message:
        if i == " ":
            encrypted_message += " "
        else:
            index = characterset.find(i.lower())
            new_index = index + key
            if new_index >= num_char:
                new_index -= num_char
            encrypted_message += characterset[new_index]
    return encrypted_message

def decrypt_message(message, key):
    decrypted_message = ""
    for i in message:
        if i == " ":
            decrypted_message += " "
        else:
            index = characterset.find(i.lower())
            new_index = index - key
            if new_index < 0:
                new_index += num_char
            decrypted_message += characterset[new_index]
    return decrypted_message

st.set_page_config(page_title="Encryption/Decryption App", layout="centered")
st.title("Message Encryptor & Decryptor")

mode_type = st.sidebar.selectbox("Choose Mode", ["Text Encryption/Decryption", "Audio Encryption/Decryption"])

if mode_type == "Text Encryption/Decryption":
    st.header("Text Encryption/Decryption")
    mode = st.radio("Select Mode:", ("Encrypt", "Decrypt"), horizontal=True)
    message = st.text_area("Enter your message here:", height=150)
    key = st.number_input("Enter the key (integer):", min_value=1, step=1)
    if st.button("Run"):
        if not message:
            st.warning("Please enter a message to proceed.")
        else:
            if mode == "Encrypt":
                result = encrypt_message(message, key)
                st.success("Message Encrypted successfully!")
            else:
                result = decrypt_message(message, key)
                st.success("Message Decrypted successfully!")
        st.text_area("Result:", value=result, height=150)
        st.code(result, language="text")

elif mode_type == "Audio Encryption/Decryption":
    st.header("Audio Encryption/Decryption")
    mode = st.radio("Select Mode:", ("Encrypt", "Decrypt"), horizontal=True)
    uploaded_file = st.file_uploader("Upload an audio file:", type=["wav", "mp3", "mp4"])
    key = st.number_input("Enter the key (integer):", min_value=1, step=1, key="audio_key")
    if uploaded_file:
        st.audio(uploaded_file)
        audio_data = uploaded_file.read()
        if mode == "Encrypt" and st.button("Encrypt Audio"):
            sound = AudioSegment.from_file(io.BytesIO(audio_data))
            samples = np.array(sound.get_array_of_samples())
            encrypted = (samples ^ key).astype(samples.dtype)
            enc_audio = sound._spawn(encrypted.tobytes())
            out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            enc_audio.export(out_path, format="mp3")
            st.success("Audio encrypted successfully!")
            st.download_button("Download Encrypted Audio", open(out_path, "rb"), file_name="encrypted_audio.mp3")
        elif mode == "Decrypt" and st.button("Decrypt Audio"):
            sound = AudioSegment.from_file(io.BytesIO(audio_data))
            samples = np.array(sound.get_array_of_samples())
            decrypted = (samples ^ key).astype(samples.dtype)
            dec_audio = sound._spawn(decrypted.tobytes())
            out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            dec_audio.export(out_path, format="mp3")
            st.success("Audio decrypted successfully!")
            st.download_button("Download Decrypted Audio", open(out_path, "rb"), file_name="decrypted_audio.mp3")
