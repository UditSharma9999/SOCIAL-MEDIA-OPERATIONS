import os
import streamlit as st
from mastodon import Mastodon
from PIL import Image
import mimetypes

# Mastodon API credentials
INSTANCE_URL = "https://mastodon.social"  # Replace with your Mastodon instance URL
ACCESS_TOKEN = "UFkcYDkg3dSdmDq4ZQpFlF7ypLyhWpyrgpTMzCDY5Eg"  # Replace with your access token

# Initialize the Mastodon client
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=INSTANCE_URL
)

# CRUD Operations

def create_toot(content, media=None):
    """Create a new toot (post)."""
    if media:
        # Determine the MIME type of the media file
        mime_type, _ = mimetypes.guess_type(media.name)
        
        if not mime_type:
            raise ValueError("Unable to determine MIME type of the media file.")
        
        # Upload media (image/video)
        media_id = mastodon.media_post(media, mime_type=mime_type)
        
        # Post the toot with the media
        toot = mastodon.status_post(content, media_ids=[media_id])
    else:
        # Post the toot without media
        toot = mastodon.status_post(content)
    
    return toot

def read_toots():
    """Read recent toots from your account."""
    toots = mastodon.timeline_home(limit=10)  # Fetch the 10 most recent toots
    return toots

def update_toot(toot_id, new_content):
    """Mastodon doesn't support editing toots, but you can delete and repost."""
    mastodon.status_delete(toot_id)
    updated_toot = create_toot(new_content)
    return updated_toot

def delete_toot(toot_id):
    """Delete a toot."""
    mastodon.status_delete(toot_id)
    return True

# Streamlit UI
def main():
    st.title("Mastodon CRUD Operations with Streamlit")
    
    # Sidebar menu
    menu = st.sidebar.radio("Menu", ["Create", "Read", "Update", "Delete"])
    
    if menu == "Create":
        st.subheader("Create a New Toot (Text/Image/Video)")
        content = st.text_area("Enter toot content")
        media_type = st.selectbox("Select media type", ["None", "Image", "Video"])
        
        media = None
        if media_type == "Image":
            media = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
        elif media_type == "Video":
            media = st.file_uploader("Upload a video", type=["mp4", "mov"])
        
        if st.button("Post Toot"):
            if content or media:
                toot = create_toot(content, media)
                st.success(f"Toot created successfully! ID: {toot['id']}")
            else:
                st.warning("Content or media must be provided.")
    
    elif menu == "Read":
        st.subheader("Read Recent Toots")
        toots = read_toots()
        if toots:
            for toot in toots:
                st.markdown(f"**{toot['account']['display_name']}**: {toot['content']}")
                st.write(f"Toot ID: {toot['id']}")
                st.markdown("---")
        else:
            st.info("No toots available.")

    elif menu == "Update":
        st.subheader("Update a Toot (Delete & Repost)")
        toots = read_toots()
        toot_ids = [toot['id'] for toot in toots]
        selected_toot = st.selectbox("Select a toot to update", toot_ids)
        new_content = st.text_area("Enter new content for the toot")
        if st.button("Update Toot"):
            if new_content:
                updated_toot = update_toot(selected_toot, new_content)
                st.success(f"Toot updated successfully! New Toot ID: {updated_toot['id']}")
            else:
                st.warning("New content must be provided.")

    
    elif menu == "Delete":
        st.subheader("Delete a Toot")
        toots = read_toots()
        toot_ids = [toot['id'] for toot in toots]
        selected_toot = st.selectbox("Select a toot to delete", toot_ids)
        if st.button("Delete Toot"):
            delete_toot(selected_toot)
            st.success(f"Toot with ID {selected_toot} deleted successfully!")
    
    
# Run the app
if __name__ == "__main__":
    main()
