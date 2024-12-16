import praw

# Set up Reddit API client
reddit = praw.Reddit(
    client_id="K1rhO5hjcgWr86L0kW5pjQ",
    client_secret="KVWREayY7U1_OFzkQlKz00AFW0rXQQ",
    user_agent="script:crud:v1.0 (by u/Holiday-Box3743)",
    username="Holiday-Box3743",
    password="soumya2854"
)

# Create a post with user input
def create_reddit_post(subreddit_name, title, content):
    try:
        # Make the post
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(title, selftext=content)
        print("Post created successfully!")
        return "Post created successfully!"
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

