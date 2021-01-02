# Rude-Bot
A rude discord text to speech bot.
It insults you sometimes.

Requirements:
Run on Python3 (for the following, use appropriate version of pip)
- discord API and voice support: `pip install discord.py` and `pip install discord.py[voice]`
- pyttsx3 (text to speech library): `pip install pyttsx3` and if on windows: `pip install pywin32` this is required to run pyttsx3 on windows
- `pip install python-dotenv`
- ffmpeg (this is a big one). This is required to play sounds. Follow the instructions to download ffmpeg:
  - https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2020-10-22-12-33/ffmpeg-N-99692-gde59826703-win64-gpl.zip
  - Download the zip from this link and extract the contents into the main Rude-Bot folder.
  - Now the path to ffmpeg.exe should look like `whatever/Rude-Bot/ffmpeg/bin/ffmpeg.exe`
  - (Optional) You install ffmpeg in any location you want but then you have to change its path in `bot.py`
  
Instructions for hosting:
- There will be a `.env` (hiddden) file in Rude-bot. Paste your discord bot token there `DISCORD_TOKEN=your_token`
- Now install all the requirements.
- and then finally `python3 bot.py`
