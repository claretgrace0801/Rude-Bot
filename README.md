# Rude-Bot
A discord text to speech bot.
It insults you sometimes.

Requirements (you can run `pip install -r requirements.txt` to install everything):
Run on Python3 (for the following, use appropriate version of pip)
- discord API and voice support: `pip install discord.py` and `pip install discord.py[voice]`
- gTTS (google's text to speech library): `pip install gTTS`
- `pip install python-dotenv`
- ffmpeg. This is required to play sounds. `sudo apt install ffmpeg`. If you're on windows, follow these instructions to download ffmpeg:
  - https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2020-10-22-12-33/ffmpeg-N-99692-gde59826703-win64-gpl.zip
  - Download the zip from this link and extract its contents.
  - Now change the line `vc.play(discord.FFmpegPCMAudio("./playing.mp3"))` to `vc.play(discord.FFmpegPCMAudio(executable="<path to ffmpeg extraction>/ffmpeg/bin/ffmpeg.exe", source="./playing.mp3"))`
  
Instructions for hosting:
- There will be a `.env` (hiddden) file in Rude-bot. Paste your discord bot token there `DISCORD_TOKEN=your_token`
- Now install all the requirements.
- and then finally `python3 bot.py`
