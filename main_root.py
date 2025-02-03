import streamlit as st
import os

# Title of the App
st.title("Simple Paste App")

# Instructions
st.write("Choose whether to paste text or upload a document, and it will be saved in the app's root directory.")

# Radio Button for User Choice
choice = st.radio("What would you like to do?", ("Paste Text", "Upload a Document"))

# Handling Text Input
if choice == "Paste Text":
    text_input = st.text_area("Enter your text here:")
    if st.button("Save Text"):
        if text_input.strip():
            # Save the text input as a file
            file_name = "pasted_text.txt"
            with open(file_name, "w") as f:
                f.write(text_input)
            st.success(f"Your text has been saved to '{file_name}' in the app's root directory!")
        else:
            st.warning("Text input is empty. Please write something to save.")

# Handling File Upload
elif choice == "Upload a Document":
    uploaded_file = st.file_uploader("Choose a file to upload", type=["png", "jpg", "jpeg", "pdf", "txt", "docx"])
    if uploaded_file is not None:
        # Save the uploaded file
        file_path = os.path.join(os.getcwd(), uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' has been uploaded and saved to the app's root directory!")
