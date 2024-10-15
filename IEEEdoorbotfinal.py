import discord
import asyncio
import requests

# Discord bot token (replace with your bot's token)
TOKEN = ''

# Dictionary of server (guild) IDs and corresponding channel IDs
# Format: {guild_id: channel_id}
CHANNEL_IDS = {
    7516629999983921291: 1285685300000000260,  # Replace with actual server (guild) and channel IDs
    1284315000000015635: 1284315000000015639 # Add as many as needed
}

# Supabase configuration
SUPABASE_URL = ""
SUPABASE_KEY = ""

# Supabase REST API table URL
TABLE_URL = f"{SUPABASE_URL}/rest/v1/door_sensor"

# Headers for Supabase API requests
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Create a Discord client with default intents
client = discord.Client(intents=discord.Intents.default())

async def update_channel_name(guild_id, channel_id):
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    
    if channel is None:
        print(f"Channel not found for guild {guild_id}!")
        return

    last_state = None

    while not client.is_closed():
        try:
            # Make a GET request to Supabase to retrieve the latest sensor data
            response = requests.get(TABLE_URL, headers=HEADERS, params={"order": "timestamp.desc", "limit": 1})

            if response.status_code == 200:
                data = response.json()
                if not data:
                    print("No data found in Supabase table.")
                    continue
                
                # Get the most recent sensor value from the Supabase response
                sensor_value = data[0].get('is_open', None)

                if sensor_value is None:
                    print("Sensor value is missing from the response.")
                    continue

                # Determine if the door is open or closed
                door_status = "Door is Open" if sensor_value == True else "Door is Closed"

                # Update the channel name only if the state has changed
                if last_state != door_status:
                    last_state = door_status
                    await channel.edit(name=f"{door_status}")
                    print(f"Channel name updated to: {door_status} for guild {guild_id}")

            else:
                print(f"Failed to retrieve data from Supabase: {response.status_code}, {response.text}")

            # Wait for 60 seconds before checking again
            await asyncio.sleep(60)

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)

@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')
    # For each guild (server), start a task to update its designated channel
    for guild_id, channel_id in CHANNEL_IDS.items():
        client.loop.create_task(update_channel_name(guild_id, channel_id))

# Run the bot
client.run(TOKEN)
