# import streamlit as st
# import asyncio  # Import asyncio

# # Main function to control the app flow
# def main():
#     # Set the title of the app
#     st.title("Social Media CRUD Operations")
    
#     # Add a selectbox for platform selection
#     app_selection = st.selectbox("Select a platform", ["Facebook", "YouTube", "Reddit", "Mastodon", "Discord"])
    
#     if app_selection == "Facebook":
#         # Facebook operations
#         import facebook_app
#         st.subheader("Facebook Operations")
#         facebook_app.main()  # Ensure facebook_app has a defined main() function
    
#     elif app_selection == "YouTube":
#         # YouTube operations
#         import youtube_app
#         st.subheader("YouTube Operations")
#         youtube_app.main()  # Ensure youtube_app has a defined main() function
    
#     elif app_selection == "Reddit":
#         # Reddit operations
#         import app  # Assuming app.py handles Reddit operations
#         st.subheader("Reddit Operations")
#         app.main()  # Ensure app has a defined main() function

#     elif app_selection == "Mastodon":
#         # Mastodon operations
#         import mastodon_app
#         st.subheader("Mastodon Manager")
#         mastodon_app.main()  # Ensure mastodon_app has a defined main() function
    
#     elif app_selection == "Discord":
#     # Discord operations
#         import run
#         st.subheader("Discord Operations")
#     # Use asyncio.run to execute the coroutine
#         asyncio.run(run.main())


# # Run the main function when the script is executed
# main()
    










# import streamlit as st
# import asyncio  # Import asyncio
# import run
# import os

# from run import client  # Import the Discord client directly from run.py
# import discord

# BOT_TOKEN =  os.getenv('BOT_TOKEN')
# async def start_discord():
#     """Start the Discord bot."""
#     await client.start(BOT_TOKEN)

# # Main function to control the app flow
# def main():
#     # Set the title of the app
#     st.title("Social Media CRUD Operations")
    
#     # Add a selectbox for platform selection
#     app_selection = st.selectbox("Select a platform", ["Facebook", "YouTube", "Reddit", "Mastodon", "Discord"], key="platform_selectbox")
    
#     if app_selection == "Facebook":
#         # Facebook operations
#         import facebook_app
#         st.subheader("Facebook Operations")
#         facebook_app.main()  # Ensure facebook_app has a defined main() function
    
#     elif app_selection == "YouTube":
#         # YouTube operations
#         import youtube_app
#         st.subheader("YouTube Operations")
#         youtube_app.main()  # Ensure youtube_app has a defined main() function
    
#     elif app_selection == "Reddit":
#         # Reddit operations
#         import app  # Assuming app.py handles Reddit operations
#         st.subheader("Reddit Operations")
#         app.main()  # Ensure app has a defined main() function

#     elif app_selection == "Mastodon":
#         # Mastodon operations
#         import mastodon_app
#         st.subheader("Mastodon Manager")
#         mastodon_app.main()  # Ensure mastodon_app has a defined main() function
    
#     elif app_selection == "Discord":
#         # run.main()
#         # asyncio.run(start_discord())
#         # asyncio.run(run.main())

#         pass

        


# # Run the main function when the script is executed
# if __name__ == "__main__":
#     main()
    








#  ===========================================


import discord
import asyncio
import streamlit as st
import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
TARGET_CHANNEL = None

async def create_message(channel, content):
    """Creates a message in the Discord channel."""
    await channel.send(content)
    print("Message created successfully!")

async def read_messages(channel, limit):
    """Reads messages from the Discord channel."""
    messages = await channel.history(limit=limit).flatten()
    print(f"\nLast {limit} messages:")
    for msg in messages:
        print(f"{msg.author}: {msg.content}")

async def update_message(channel, message_id, new_content):
    """Updates a bot-sent message by ID."""
    try:
        msg = await channel.fetch_message(message_id)
        if msg.author == client.user:
            await msg.edit(content=new_content)
            print("Message updated successfully!")
        else:
            print("You can only update messages sent by the bot.")
    except discord.NotFound:
        print("Message not found.")

async def delete_message(channel, message_id):
    """Deletes a bot-sent message by ID."""
    try:
        msg = await channel.fetch_message(message_id)
        if msg.author == client.user:
            await msg.delete()
            print("Message deleted successfully!")
        else:
            print("You can only delete messages sent by the bot.")
    except discord.NotFound:
        print("Message not found.")

@client.event
async def on_ready():
    global TARGET_CHANNEL
    st.title("Discord Bot Control Panel")
    st.write(f"Logged in as {client.user}")

    guild_name = st.text_input("Enter the name of the guild/server:")
    channel_name = st.text_input("Enter the name of the channel:")

    if guild_name and channel_name:
        guild = discord.utils.get(client.guilds, name=guild_name)
        if guild:
            TARGET_CHANNEL = discord.utils.get(guild.channels, name=channel_name)
            if TARGET_CHANNEL:
                st.success(f"Target channel set to #{TARGET_CHANNEL.name}.")
                run_command()
            else:
                st.error("Channel not found.")
                await client.close()
        else:
            st.error("Guild/Server not found.")
            await client.close()

def run_command():
    """Display the command options and handle user input."""
    if TARGET_CHANNEL:
        operation = st.selectbox("Choose an operation:", ["Create Message", "Read Messages", "Update Message", "Delete Message"])

        if operation == "Create Message":
            content = st.text_area("Enter the message content:")
            if st.button("Create"):
                asyncio.run_coroutine_threadsafe(create_message(TARGET_CHANNEL, content), client.loop)

        elif operation == "Read Messages":
            limit = st.number_input("Enter the number of messages to fetch:", min_value=1, step=1)
            if st.button("Read"):
                asyncio.run_coroutine_threadsafe(read_messages(TARGET_CHANNEL, limit), client.loop)

        elif operation == "Update Message":
            message_id = st.text_area("Enter the message ID to update:")
            new_content = st.text_area("Enter the new content:")
            if st.button("Update"):
                message_id = int(message_id)
                asyncio.run_coroutine_threadsafe(update_message(TARGET_CHANNEL, message_id, new_content), client.loop)

        elif operation == "Delete Message":
            message_id = st.text_area("Enter the message ID to delete:")
            if st.button("Delete"):
                message_id = int(message_id)
                asyncio.run_coroutine_threadsafe(delete_message(TARGET_CHANNEL, message_id), client.loop)

async def discord_main():
    """Start the Discord bot."""
    await client.start(BOT_TOKEN)

def social_media_operations():
    """Handles the app's main flow for different platforms."""
    st.title("Social Media CRUD Operations")
    
    app_selection = st.selectbox("Select a platform", ["Facebook", "YouTube", "Reddit", "Mastodon", "Discord"])

    if app_selection == "Facebook":
        # Facebook operations
        import facebook_app
        st.subheader("Facebook Operations")
        facebook_app.main()

    elif app_selection == "YouTube":
        # YouTube operations
        import youtube_app
        st.subheader("YouTube Operations")
        youtube_app.main()

    elif app_selection == "Reddit":
        # Reddit operations
        import app  # Assuming app.py handles Reddit operations
        st.subheader("Reddit Operations")
        app.main()

    elif app_selection == "Mastodon":
        # Mastodon operations
        import mastodon_app
        st.subheader("Mastodon Manager")
        mastodon_app.main()

    elif app_selection == "Discord":
        st.subheader("Discord Operations")
        st.sidebar.title("Bot Control")
        st.write("Starting bot...")
        asyncio.run(discord_main())

if __name__ == "__main__":
    social_media_operations()
