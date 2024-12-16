import streamlit as st
import asyncio  # Import asyncio

# Main function to control the app flow
def main():
    # Set the title of the app
    st.title("Social Media CRUD Operations")
    
    # Add a selectbox for platform selection
    app_selection = st.selectbox("Select a platform", ["Facebook", "YouTube", "Reddit", "Mastodon", "Discord"])
    
    if app_selection == "Facebook":
        # Facebook operations
        import facebook_app
        st.subheader("Facebook Operations")
        facebook_app.main()  # Ensure facebook_app has a defined main() function
    
    elif app_selection == "YouTube":
        # YouTube operations
        import youtube_app
        st.subheader("YouTube Operations")
        youtube_app.main()  # Ensure youtube_app has a defined main() function
    
    elif app_selection == "Reddit":
        # Reddit operations
        import app  # Assuming app.py handles Reddit operations
        st.subheader("Reddit Operations")
        app.main()  # Ensure app has a defined main() function

    elif app_selection == "Mastodon":
        # Mastodon operations
        import mastodon_app
        st.subheader("Mastodon Manager")
        mastodon_app.main()  # Ensure mastodon_app has a defined main() function
    
    elif app_selection == "Discord":
    # Discord operations
        import run
        st.subheader("Discord Operations")
    # Use asyncio.run to execute the coroutine
        asyncio.run(run.main())


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
    
