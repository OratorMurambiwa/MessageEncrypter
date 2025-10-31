# Message Encryptor & Decryptor

A simple yet powerful **Streamlit web app** for encrypting and decrypting both **text and audio files**, featuring a **Matrix-inspired green-on-black hacker UI**.

This project combines basic cryptography concepts with a creative, cyberpunk-styled user interface. Users can:
- Encrypt or decrypt text using a Caesar-like cipher.
- Encrypt and decrypt audio files (`.wav`, `.mp3`, `.m4a`) by segment shuffling with a secret key.
- Download the encrypted audio and its matching metadata as a single `.zip` file.
- Enjoy a glowing neon-green hacker aesthetic built with Streamlit custom CSS.

---

## Features

-  **Text Encryption / Decryption**
  - Simple Caesar-shift logic using a custom character set.
  - Adjustable integer key.
  - Encrypted results displayed instantly.

- **Audio Encryption / Decryption**
  - Encrypts by **shuffling audio chunks** using a key-based random seed.
  - Produces encrypted `.mp3` output and a `.json` file containing the shuffle order.
  - Decrypts perfectly when the same key and `.json` file are used.
  - Uses **WAV format internally** for lossless transformation.
  - Downloads both files as a `.zip` package for convenience.

- **Hacker-Themed UI**
  - Glowing green text and buttons on a pure black background.
  - Terminal-style fonts and hover effects.
  - Feels like you’re in the Matrix while encrypting files.

---

## Tech Stack

- **Frontend:** Streamlit  
- **Audio Processing:** Pydub  
- **Metadata Detection:** Mutagen  
- **Packaging:** zipfile, tempfile  
- **Language:** Python 3.10+

---

## Setup & Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/OratorMurambiwa/MessageEncrypter.git
   cd MessageEncrypter

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run main.py

Usage
Text Encryption

Select “Text Encryption/Decryption”.

Choose Encrypt or Decrypt.

Enter your message and numeric key.

Click RUN ENCRYPTION/DECRYPTION.

Copy or view your encrypted message in the console output.

Audio Encryption

Select “Audio Encryption/Decryption”.

Upload an audio file (.wav, .mp3, .m4a).

Enter a key (integer).

Adjust the chunk size (default 800ms).

Click START ENCRYPTION.

Download the .zip file containing:

encrypted_audio.mp3

encryption_meta.json

Audio Decryption

Reupload the encrypted .mp3 file.

Upload its matching encryption_meta.json.

Enter the same key used for encryption.

Click START DECRYPTION to restore the original audio.

How It Works
Text Cipher

Each character’s index is shifted forward or backward in a predefined character set, depending on the key and mode (Encrypt/Decrypt).

Audio Cipher

The app:

Splits the audio into time chunks (e.g., 800ms each).

Randomly shuffles the order based on the key.

Saves the shuffle order in encryption_meta.json.

Decryption reverses the shuffle using that same order.

🖥️ UI Preview
<p align="center"> <img src="https://i.imgur.com/VRiPnqI.png" width="600" alt="Hacker UI Screenshot"> </p>
 Requirements

See requirements.txt

Author

Orator Murambiwa
🔗 GitHub
 • Grambling State University

License

This project is open source under the MIT License
.

“In cryptography, the only thing cooler than encryption... is decrypting your own voice.” - OpenAI