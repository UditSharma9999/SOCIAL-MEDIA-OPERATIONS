import praw

# Set up Reddit API client
reddit = praw.Reddit(
    client_id="K1rhO5hjcgWr86L0kW5pjQ",
    client_secret="KVWREayY7U1_OFzkQlKz00AFW0rXQQ",
    user_agent="script:crud:v1.0 (by u/Holiday-Box3743)",
    username="Holiday-Box3743",
    password="soumya2854"
)

# Function to update a Reddit post
def update_reddit_post(post_id, new_content):
    try:
        # Fetch the post by ID
        post = reddit.submission(id=post_id)
        
        # Check if the post exists and if the authenticated user is the author
        if not post:
            print("Invalid Post ID or the post does not exist.")
            return "Invalid Post ID or the post does not exist."
        
        if post.author.name != reddit.user.me().name:
            print("You can only edit posts that you have created.")
            return "You can only edit posts that you have created."
        
        # Update the post content
        post.edit(new_content)
        print("Post updated successfully!")
        return "Post updated successfully!"
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

