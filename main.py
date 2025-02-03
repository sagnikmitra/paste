import streamlit as st
import requests
from datetime import datetime

# GitHub Configuration
GITHUB_TOKEN = "your_github_personal_access_token"  # Replace with your token
GITHUB_REPO = "your_username/your_repo_name"  # Replace with your repo
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents"

# Helper function to upload file to GitHub
def upload_to_github(file_content, file_name, file_type):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if file_type == "text":
        file_path = f"uploads/text_{now}.txt"
    else:
        file_path = f"uploads/{file_name.split('/')[-1]}"
    
    encoded_content = file_content if file_type == "text" else file_content.read().decode("latin1")
    response = requests.put(
        f"{GITHUB_API_URL}/{file_path}",
        json={
            "message": f"Add {file_name}",
            "content": encoded_content.encode("utf-8").decode("latin1"),
        },
        headers={"Authorization": f"token {GITHUB_TOKEN}"},
    )
    if response.status_code == 201:
        return f"File '{file_name}' successfully uploaded!"
    else:
        return f"Error: {response.status_code}, {response.json().get('message')}"

# Streamlit UI
st.title("Upload Text, Picture, or Document")

st.write("You can upload text, images, or documents. The files will be saved to the designated GitHub repository.")

# Input for Text
text_input = st.text_area("Enter Text (Optional):")

# File Upload
file_input = st.file_uploader("Upload a File (Optional)", type=["png", "jpg", "jpeg", "pdf", "docx", "txt"])

if st.button("Submit"):
    if text_input:
        result = upload_to_github(text_input, "text_input", "text")
        st.success(result)
    elif file_input:
        result = upload_to_github(file_input, file_input.name, "file")
        st.success(result)
    else:
        st.warning("Please provide either text or a file for upload.")
