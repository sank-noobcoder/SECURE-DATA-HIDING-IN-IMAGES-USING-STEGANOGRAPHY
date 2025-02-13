import streamlit as st
import base64
from stegano.lsb import hide, reveal
from cryptography.fernet import Fernet

# Function to generate a key from the password
def get_key(password):
    return base64.urlsafe_b64encode(password.ljust(32).encode())  # Ensure key is 32 bytes

# Encrypt message using the password
def encrypt_message(message, password):
    try:
        key = get_key(password)
        cipher = Fernet(key)
        return cipher.encrypt(message.encode()).decode()
    except Exception as e:
        return f"Encryption Error: {str(e)}"

# Decrypt message using the password
def decrypt_message(encrypted_message, password):
    try:
        key = get_key(password)
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_message.encode()).decode()
    except Exception as e:
        return "❌ Incorrect password or corrupted data!"

# Function to hide encrypted text inside an image
def encode_image(image, message, password):
    try:
        encrypted_message = encrypt_message(message, password)
        encoded_image = hide(image, encrypted_message)  # Hide message in image
        output_path = "encoded_image.png"
        encoded_image.save(output_path)  # Save the new image
        return output_path
    except Exception as e:
        return f"❌ Encoding Error: {str(e)}"

# Function to extract and decrypt text from an image
def decode_image(image, password):
    try:
        hidden_message = reveal(image)  # Extract hidden message
        if hidden_message is None:
            return "⚠ No hidden message found!"
        decrypted_message = decrypt_message(hidden_message, password)  # Decrypt message
        return decrypted_message
    except Exception as e:
        return f"❌ Extraction Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="🔐 Steganography App", page_icon="🔏", layout="centered")

st.sidebar.title("🔍 Choose an Option")
selected_option = st.sidebar.radio("Select", ["Encode Message", "Decode Message"])

# Encode Page
if selected_option == "Encode Message":
    st.title("🔒 Hide Secret Message in Image")
    st.markdown("Securely encrypt and hide messages in images.")

    uploaded_image = st.file_uploader("📤 Upload an Image (PNG Recommended)", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        message = st.text_area("💬 Enter the Secret Message to Hide")
        password = st.text_input("🔑 Enter Encryption Password", type="password")

        if st.button("🔏 Encode and Download Image"):
            if message and password:
                encoded_path = encode_image(uploaded_image, message, password)
                with open(encoded_path, "rb") as f:
                    st.download_button("📥 Download Encoded Image", f, file_name="encoded_image.png")
                st.success("✅ Image successfully encoded and ready for download!")
            else:
                st.error("⚠ Please enter a message and password!")

# Decode Page
elif selected_option == "Decode Message":
    st.title("🔓 Extract Hidden Message from Image")
    st.markdown("Upload an encoded image and enter the password to reveal the secret message.")

    decode_image_file = st.file_uploader("📤 Upload an Encoded Image", type=["png", "jpg", "jpeg"])

    if decode_image_file:
        decode_password = st.text_input("🔑 Enter Decryption Password", type="password")

        if st.button("🔓 Decode Message"):
            if decode_password:
                extracted_message = decode_image(decode_image_file, decode_password)
                if "Error" in extracted_message:
                    st.error(extracted_message)
                else:
                    st.success("🔍 Secret Message: " + extracted_message)
            else:
                st.error("⚠ Please enter a password!")
