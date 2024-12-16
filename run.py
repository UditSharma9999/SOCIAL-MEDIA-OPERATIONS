import discord
import asyncio
import streamlit as st
import dotenv
import os
dotenv.load_dotenv();


BOT_TOKEN =  os.getenv('BOT_TOKEN')
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
                asyncio.run(create_message(TARGET_CHANNEL, content))

        elif operation == "Read Messages":
            limit = st.number_input("Enter the number of messages to fetch:", min_value=1, step=1)
            if st.button("Read"):
                asyncio.run_coroutine_threadsafe(read_messages(TARGET_CHANNEL, limit), client.loop)
                # asyncio.run(read_messages(TARGET_CHANNEL, limit))

        elif operation == "Update Message":
            message_id = st.text_area("Enter the message ID to update:")
            new_content = st.text_area("Enter the new content:")
            if st.button("Update"):
                id = int(message_id)
                # asyncio.run(update_message(TARGET_CHANNEL, message_id, new_content))
                asyncio.run_coroutine_threadsafe(update_message(TARGET_CHANNEL, id, new_content), client.loop)

        elif operation == "Delete Message":
            message_id = st.text_area("Enter the message ID to delete:")
            if st.button("Delete"):
                id = int(message_id)
                # asyncio.run(delete_message(TARGET_CHANNEL, message_id))
                asyncio.run_coroutine_threadsafe(delete_message(TARGET_CHANNEL, id), client.loop)

async def main():
    """Start the Discord bot."""
    await client.start(BOT_TOKEN)


if __name__ == "__main__":
    st.sidebar.title("Bot Control")
    st.write("Starting bot...")
    asyncio.run(main())
