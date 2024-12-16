import webbrowser
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
from google.auth.transport.requests import Request  # Correct import for token refresh

# Define constants for the credentials file and scopes
CLIENT_SECRET_FILE = "client_secret.json"  # Path to your credentials file
TOKEN_FILE = "token.json"  # Path to store token
SCOPES = ["https://www.googleapis.com/auth/youtube"]

# Initialize YouTube API client
def initialize_youtube():
    creds = load_credentials()
    youtube = build("youtube", "v3", credentials=creds)
    print("YouTube API client initialized.")
    return youtube

# Load or get credentials with OAuth
def load_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        print("Loading credentials from token file...")
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"Error loading credentials: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Token expired. Refreshing...")
            try:
                creds.refresh(Request())
                print("Token refreshed successfully.")
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None
        if not creds or not creds.valid:  # Start OAuth if refresh fails
            print("No valid token found. Starting OAuth flow...")
            if not os.path.exists(CLIENT_SECRET_FILE):
                raise FileNotFoundError(f"Client secret file not found: {CLIENT_SECRET_FILE}")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            print("New credentials obtained.")

        # Save new credentials to token file
        if creds:
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            print("Credentials saved to token file.")
    return creds

# Create (Upload) a video with YouTube API
def upload_video(file_path, title, description):
    youtube = initialize_youtube()
    print(f"Uploading video: {title}")
    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": ["example", "CRUD"],
                    "categoryId": "22",
                },
                "status": {
                    "privacyStatus": "private",
                },
            },
            media_body=file_path,
        )
        response = request.execute()
        print(f"Video uploaded successfully with ID: {response['id']}")
        webbrowser.open(f"https://www.youtube.com/watch?v={response['id']}")
        return response["id"]
    except HttpError as error:
        print(f"Error uploading video: {error}")
        return None

# Read (Retrieve) video details
def get_video_details(video_id):
    youtube = initialize_youtube()
    print(f"Retrieving details for video ID: {video_id}")
    try:
        request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
        response = request.execute()
        print("Video Details:")
        print(json.dumps(response, indent=4))
        return response
    except HttpError as error:
        print(f"Error getting video details: {error}")
        return None

# Update video details
def update_video(video_id, new_title, new_description):
    youtube = initialize_youtube()
    print(f"Updating video ID: {video_id} with new title and description")
    try:
        request = youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": new_title,
                    "description": new_description,
                    "categoryId": "22",
                },
            },
        )
        response = request.execute()
        print(f"Video with ID {video_id} updated successfully.")
        webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")
        return response
    except HttpError as error:
        print(f"Error updating video: {error}")
        return None

# Delete a video
def delete_video(video_id):
    youtube = initialize_youtube()
    print(f"Deleting video ID: {video_id}")
    try:
        request = youtube.videos().delete(id=video_id)
        request.execute()
        print(f"Video with ID {video_id} deleted successfully.")
    except HttpError as error:
        print(f"Error deleting video: {error}")

# Main function to demonstrate CRUD operations
def main():
    file_path = "video.mp4"  # Path to your video file
    title = "Sample Upload Video"
    description = "This is a test upload video using the YouTube API"

    print("1. Creating/Uploading the video...")
    video_id = upload_video(file_path, title, description)
    if video_id:  # Only proceed if upload was successful
        print("\n2. Retrieving video details...")
        get_video_details(video_id)

        print("\n3. Updating video details...")
        new_title = "Updated Video Title"
        new_description = "This is the updated description for the video."
        update_video(video_id, new_title, new_description)

        print("\n4. Deleting the video...")
        delete_video(video_id)

if __name__ == "__main__":
    main()
