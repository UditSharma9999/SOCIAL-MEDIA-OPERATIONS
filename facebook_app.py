import streamlit as st
import requests

# Replace with your actual access token and page ID
ACCESS_TOKEN = 'EAAHsPMV7w1UBO7JNxgRdhMWqJK9ZAmaKbjYdfnUS3zk4KMGP1AZBmIL7NezqZARN5kHD06gjOhn3j2rSSgXU8hyOssagAYOnVmY17FE101hq0ikbOSiUu29VdE0pzWZBEACn8i402ZBZC5kAeA7ZAYwS6GHn5zR57YLfKbFJ2qgJlZAXPgVpRRe18buo4gvHXCghW5MOl8sy'
PAGE_ID = '493274720537567'

BASE_URL = f"https://graph.facebook.com/v17.0/{PAGE_ID}"

# Streamlit UI for creating a post
def create_post():
    st.write("Choose the type of post you want to create:")
    post_type = st.selectbox("Post Type", ["Text Post", "Post with Image", "Post with Video"])

    if post_type == "Text Post":
        message = st.text_input("Enter the message you want to post:")
        if st.button("Create Text Post"):
            if message:
                url = f"{BASE_URL}/feed"
                params = {'message': message, 'access_token': ACCESS_TOKEN}
                try:
                    response = requests.post(url, params=params, timeout=30)
                    response.raise_for_status()
                    st.success("Text Post Created Successfully!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error: {e}")
    
    elif post_type == "Post with Image":
        image_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "gif"])
        caption = st.text_input("Enter a caption for the image:")
        if st.button("Create Image Post"):
            if image_file:
                url = f"{BASE_URL}/photos"
                params = {'caption': caption, 'access_token': ACCESS_TOKEN}
                try:
                    # Upload image to Facebook
                    files = {'source': image_file}
                    response = requests.post(url, params=params, files=files, timeout=30)
                    response.raise_for_status()
                    st.success("Image Post Created Successfully!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error: {e}")
    
    elif post_type == "Post with Video":
        video_file = st.file_uploader("Choose a video", type=["mp4", "mov", "avi", "mkv"])
        description = st.text_input("Enter a description for the video:")
        if st.button("Create Video Post"):
            if video_file:
                url = f"{BASE_URL}/videos"
                params = {'description': description, 'access_token': ACCESS_TOKEN}
                try:
                    # Upload video to Facebook
                    files = {'source': video_file}
                    response = requests.post(url, params=params, files=files, timeout=30)
                    response.raise_for_status()
                    st.success("Video Post Created Successfully!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error: {e}")
    
    else:
        st.error("Invalid post type selected.")

# Streamlit UI for reading posts
def read_posts():
    url = f"{BASE_URL}/posts"
    params = {'access_token': ACCESS_TOKEN}
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        st.write("Read Posts:")
        posts = response.json().get('data', [])
        for post in posts:
            st.write(post)
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

# Streamlit UI for updating a post
def update_post():
    post_id = st.text_input("Enter the Post ID you want to update:")
    new_message = st.text_input("Enter the new message:")
    if st.button("Update Post"):
        if post_id and new_message:
            url = f"https://graph.facebook.com/{post_id}"
            params = {
                'message': new_message,
                'access_token': ACCESS_TOKEN
            }
            try:
                response = requests.post(url, params=params, timeout=30)
                response.raise_for_status()
                st.success("Post Updated Successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
        else:
            st.error("Post ID and new message are required.")

# Streamlit UI for deleting a post
def delete_post():
    post_id = st.text_input("Enter the Post ID you want to delete:")
    if st.button("Delete Post"):
        if post_id:
            url = f"https://graph.facebook.com/{post_id}"
            params = {'access_token': ACCESS_TOKEN}
            try:
                response = requests.delete(url, params=params, timeout=30)
                response.raise_for_status()
                st.success("Post Deleted Successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
        else:
            st.error("Post ID is required.")

# Main Streamlit UI
def main():
    st.title("Facebook Post Management App")
    
    menu = ["Create a Post", "Read Posts", "Update a Post", "Delete a Post", "Exit"]
    choice = st.sidebar.selectbox("Choose an operation", menu)
    
    if choice == "Create a Post":
        create_post()
    elif choice == "Read Posts":
        read_posts()
    elif choice == "Update a Post":
        update_post()
    elif choice == "Delete a Post":
        delete_post()
    elif choice == "Exit":
        st.write("Exiting the program.")

# Run the app
if __name__ == "__main__":
    main()
