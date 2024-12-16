import praw
import streamlit as st
from delete_post import delete_reddit_post
from update_post import update_reddit_post
from read_post import get_user_posts
from create_post import create_reddit_post

# Set up Reddit API client
reddit = praw.Reddit(
    client_id="K1rhO5hjcgWr86L0kW5pjQ",
    client_secret="KVWREayY7U1_OFzkQlKz00AFW0rXQQ",
    user_agent="script:crud:v1.0 (by u/Holiday-Box3743)",
    username="Holiday-Box3743",
    password="soumya2854"
)

# Streamlit App
def main():
    st.title("Reddit Post Management (CRUD)")

    # Create Sidebar with navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose a task", ["Create Post", "Read Posts", "Update Post", "Delete Post"])

    # Create Post
    if app_mode == "Create Post":
        st.header("Create a New Post")
        
        # User input fields for creating a post
        subreddit_name = st.text_input("Enter Subreddit Name")
        title = st.text_input("Enter Title of the Post")
        content = st.text_area("Enter Content of the Post")

        if st.button("Create Post"):
            if subreddit_name and title and content:
                # Call the create post function
                result_message = create_reddit_post(subreddit_name, title, content)
                if "successfully" in result_message.lower():
                    st.success(result_message)
                else:
                    st.error(result_message)
            else:
                st.error("Please fill in all the fields.")

    # Read Posts
    elif app_mode == "Read Posts":
        st.header("Read Your Posts")

        # Create form to handle user input for reading posts
        with st.form(key='read_form'):
            subreddit_name = st.text_input("Enter Subreddit Name (leave blank for all)")
            post_limit = st.number_input("Enter Number of Posts to Display", min_value=1, max_value=10, value=5)
            
            # Form submit button
            submit_button = st.form_submit_button(label="Show Posts")
            
            # If the form is submitted
            if submit_button:
                st.write(f"Showing posts with limit: {post_limit}")
                
                # Fetch posts
                posts_data = get_user_posts(subreddit_name=subreddit_name, post_limit=post_limit)
                
                # Debugging: Print the fetched posts data to the Streamlit app
                st.write("Fetched posts data:")
                st.write(posts_data)  # This will help confirm if data is being fetched
                
                # Display posts if data is found
                if posts_data:
                    for post in posts_data:
                        st.write(f"**Title:** {post['title']}")
                        st.write(f"**Score:** {post['score']}")
                        st.write(f"**URL:** {post['url']}")
                        st.write(f"**Content:** {post['content']}")
                        st.markdown("---")  # Separator
                else:
                    st.write("No posts found.")

    # Update Post
    elif app_mode == "Update Post":
        st.header("Update an Existing Post")
        
        # User input fields for updating a post
        post_id = st.text_input("Enter Post ID (found in URL)")
        new_content = st.text_area("Enter New Content for the Post")

        if st.button("Update Post"):
            if post_id and new_content:
                # Call the update post function
                result_message = update_reddit_post(post_id, new_content)
                if "successfully" in result_message.lower():
                    st.success(result_message)
                else:
                    st.error(result_message)
            else:
                st.error("Please fill in all the fields.")

    # Delete Post
    elif app_mode == "Delete Post":
        st.header("Delete a Post")
        
        # User input field for deleting a post
        post_id = st.text_input("Enter Post ID to Delete")

        if st.button("Delete Post"):
            if post_id:
                # Call the function to delete the post
                result_message = delete_reddit_post(post_id)
                if "successfully" in result_message.lower():
                    st.success(result_message)
                else:
                    st.error(result_message)
            else:
                st.error("Please enter a valid Post ID.")

if __name__ == "__main__":
    main()  # Ensure the main function is properly called
