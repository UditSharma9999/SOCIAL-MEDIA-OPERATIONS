import praw

# Set up Reddit API client
reddit = praw.Reddit(
    client_id="K1rhO5hjcgWr86L0kW5pjQ",  # Your client_id
    client_secret="KVWREayY7U1_OFzkQlKz00AFW0rXQQ",  # Your client_secret
    user_agent="script:crud:v1.0 (by u/Holiday-Box3743)",  # Your user_agent
    username="Holiday-Box3743",  # Your Reddit username
    password="soumya2854"  # Your Reddit password
)

# Function to delete a Reddit post
def delete_reddit_post(post_id):
    try:
        # Fetch the post by ID
        post = reddit.submission(id=post_id)
        
        # Check if the post exists
        if not post:
            return "Invalid Post ID or the post does not exist."
        
        # Check if the authenticated user is the author
        if post.author.name != reddit.user.me().name:
            return "You can only delete posts that you have created."
        
        # Delete the post
        post.delete()
        return "Post deleted successfully!"
    
    except Exception as e:
        return f"An error occurred: {e}"


