import streamlit as st
import webbrowser
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import json

# Constants
CLIENT_SECRET_FILE = 'client_secret.json'
TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']

# Initialize YouTube API client
def initialize_youtube():
    creds = load_credentials()
    youtube = build('youtube', 'v3', credentials=creds)
    return youtube

# Load or get credentials with OAuth
def load_credentials():
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

# Upload a video
def upload_video(file_path, title, description):
    youtube = initialize_youtube()
    media = MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)
    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": ["example", "CRUD"],
                    "categoryId": "22"
                },
                "status": {
                    "privacyStatus": "private"
                }
            },
            media_body=media
        )
        response = request.execute()
        st.success(f"Video uploaded successfully with ID: {response['id']}")
        st.write(f"View the uploaded video [here](https://www.youtube.com/watch?v={response['id']})")
        webbrowser.open(f"https://www.youtube.com/watch?v={response['id']}")
        return response['id']
    except HttpError as error:
        if error.resp.status == 403:
            st.error("Error 403: Daily quota limit exceeded. Please try again tomorrow.")
        else:
            st.error(f"Error uploading video: {error}")
        return None

# Retrieve video details
def get_video_details(video_id):
    youtube = initialize_youtube()
    try:
        request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
        response = request.execute()
        return response
    except HttpError as error:
        if error.resp.status == 403:
            st.error("Error 403: Daily quota limit exceeded. Please try again tomorrow.")
        else:
            st.error(f"Error retrieving video details: {error}")
        return None

# Update video details
def update_video(video_id, new_title, new_description):
    youtube = initialize_youtube()
    try:
        request = youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": new_title,
                    "description": new_description,
                    "categoryId": "22"
                }
            }
        )
        response = request.execute()
        st.success(f"Video with ID {video_id} updated successfully.")
        st.write(f"View the updated video [here](https://www.youtube.com/watch?v={video_id})")
        webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")
        return response
    except HttpError as error:
        if error.resp.status == 403:
            st.error("Error 403: Daily quota limit exceeded. Please try again tomorrow.")
        else:
            st.error(f"Error updating video: {error}")
        return None

# Delete a video
def delete_video(video_id):
    youtube = initialize_youtube()
    try:
        request = youtube.videos().delete(id=video_id)
        request.execute()
        st.success(f"Video with ID {video_id} deleted successfully.")
    except HttpError as error:
        if error.resp.status == 403:
            st.error("Error 403: Daily quota limit exceeded. Please try again tomorrow.")
        else:
            st.error(f"Error deleting video: {error}")

# Main Streamlit App
def main():
    st.title("YouTube API CRUD Application")
    st.sidebar.header("Select Operation")
    option = st.sidebar.selectbox("Choose an operation:", ["Upload Video", "Get Video Details", "Update Video", "Delete Video"])

    if option == "Upload Video":
        st.header("Upload a Video")
        video_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
        video_title = st.text_input("Enter Video Title", "Sample Video")
        video_description = st.text_area("Enter Video Description", "This is a sample video.")
        if st.button("Upload Video"):
            if video_file:
                with open("temp_video.mp4", "wb") as f:
                    f.write(video_file.getbuffer())
                video_id = upload_video("temp_video.mp4", video_title, video_description)
                os.remove("temp_video.mp4")  # Clean up temporary file
            else:
                st.error("Please select a video file to upload.")

    elif option == "Get Video Details":
        st.header("Get Video Details")
        video_id_input = st.text_input("Enter Video ID")
        if st.button("Get Video Details"):
            if video_id_input:
                details = get_video_details(video_id_input)
                if details:
                    st.json(details)
            else:
                st.error("Please enter a video ID.")

    elif option == "Update Video":
        st.header("Update Video Details")
        video_id_update = st.text_input("Enter Video ID to Update")
        new_title = st.text_input("Enter New Title")
        new_description = st.text_area("Enter New Description")
        if st.button("Update Video"):
            if video_id_update:
                update_video(video_id_update, new_title, new_description)
            else:
                st.error("Please enter a video ID.")

    elif option == "Delete Video":
        st.header("Delete a Video")
        video_id_delete = st.text_input("Enter Video ID to Delete")
        if st.button("Delete Video"):
            if video_id_delete:
                delete_video(video_id_delete)
            else:
                st.error("Please enter a video ID.")

if __name__ == "__main__":
    main()
