import streamlit as st

characterset = ("abcdefghijklmnopqrstuvwxyz0123456789!?/,.:;+=-<>@#$%^&*")
num_char = len(characterset)

# Encryption function
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

# Decryption function
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

#user interface

st.set_page_config(page_title="Encryption/Decryption App", layout="centered")
st.title("Message Encryptor & Decryptor")

mode = st.radio("Select Mode:", ("Encrypt", "Decrypt"), horizontal=True)
message = st.text_area("Enter your message here:", height=150)
key = st.number_input("Enter the key (integer):", min_value=1, step=1)

#action button
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

