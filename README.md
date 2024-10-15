# Door Sensor Monitoring with ESP32 & Supabase

This project utilizes an **ESP32** microcontroller with a **reed switch door sensor** to monitor the state of a door (open or closed). The data is sent to **Supabase** for logging and is periodically deleted to avoid overuse of space. A **Discord bot** is also implemented to update a channel name with the current state of the door.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Hardware Components](#hardware-components)
- [Software Components](#software-components)
- [Setup](#setup)
  - [ESP32 Setup](#esp32-setup)
  - [Supabase Database Setup](#supabase-database-setup)
  - [Discord Bot Setup](#discord-bot-setup)
- [Log Deletion](#log-deletion)
- [License](#license)

## Project Overview
The ESP32 is connected to a reed switch that detects whether the door is open or closed. It sends this data to Supabase every 5 minutes, and the data is stored as `TRUE` (open) or `FALSE` (closed). To avoid filling up the Supabase storage, old log entries (older than 1 day) are periodically deleted.

Additionally, a Discord bot is used to update a channel's name in real-time, displaying the door's current state (open or closed). The bot can support multiple servers, each with its own unique channel.

## Features
- Monitors door status using a reed switch.
- Sends data to Supabase every 5 minutes.
- Deletes old log entries from Supabase after 1 day.
- Discord bot that updates the channel name with the current door state.
- Supports multiple Discord servers.

## Hardware Components
- **ESP32** microcontroller
- **Reed switch** (door sensor)
- Connecting wires
- Breadboard (optional)

## Software Components
- Arduino IDE for programming the ESP32
- Supabase for data storage
- Discord API for bot integration
- Python for the Discord bot

## Setup

### ESP32 Setup
1. **Connect the Reed Switch:**
   - One end of the reed switch connects to **GND** on the ESP32.
   - The other end connects to **GPIO25** on the ESP32 (or any available GPIO pin).

2. **Install Required Libraries:**
   - WiFi: Comes with the Arduino IDE for ESP32.
   - HTTPClient: Also comes with the ESP32 libraries.
   
3. **Upload the Code:**
   - Replace the placeholders for your WiFi credentials and Supabase details in the provided code.
   - Upload the modified code to your ESP32 using the Arduino IDE.

### Supabase Database Setup
1. **Create a Supabase Project:**
   - Go to [Supabase](https://supabase.com/) and create a new project.

2. **Create a Table:**
   - Use this SQL command to create the table for door sensor logs:
     ```sql
     CREATE TABLE door_sensor_data (
       id SERIAL PRIMARY KEY,
       sensor_value BOOLEAN,
       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```
   
3. **Set Up API Keys:**
   - Retrieve your Supabase `API URL` and `API Key` from the project settings. Insert them into your ESP32 and Discord bot code.

4. **Log Deletion Function:**
   - Create a function to delete logs older than 1 day using this SQL:
     ```sql
     CREATE OR REPLACE FUNCTION delete_old_logs()
     RETURNS void AS $$
     BEGIN
       DELETE FROM door_sensor_data WHERE timestamp < NOW() - INTERVAL '1 day';
     END;
     $$ LANGUAGE plpgsql;
     ```
   - Set up a cron job or use Supabase’s built-in scheduled tasks to periodically call this function.

### Discord Bot Setup
1. **Create a Discord Bot:**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new bot.
   - Add the bot to your server and give it the necessary permissions to manage channels.

2. **Install Python Dependencies:**
   - Install `discord.py` and `requests`:
     ```bash
     pip install discord.py requests
     ```

3. **Modify and Run the Bot:**
   - Replace placeholders in the provided Python code with your Discord bot token, channel IDs, and Supabase credentials.
   - Run the bot script to start monitoring your Supabase table and updating the channel name.

## Log Deletion
Logs older than 1 day are deleted to prevent overuse of Supabase storage. The deletion process runs as a scheduled task in Supabase.

