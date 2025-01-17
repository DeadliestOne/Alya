import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables from .env file
load_dotenv()

API_ID = int(getenv("API_ID" , 26416419))
API_HASH = getenv("API_HASH" , "c109c77f5823c847b1aeb7fbd4990cc4")
BOT_TOKEN = getenv("BOT_TOKEN" , "7763722459:AAF1p7FxZX094Uh6E7WAZepNFK1mzZSFXY0")
# Specify where to get the following credentials
OWNER_USERNAME = getenv("OWNER_USERNAME", "Uncountableaura")
BOT_USERNAME = getenv("BOT_USERNAME", "AlyaxMusicBot")
BOT_NAME = getenv("BOT_NAME", "˹𝐀ɴɴɪᴇ ✘ 𝙼ᴜsɪᴄ˼ ♪")
ASSUSERNAME = getenv("ASSUSERNAME", "AlyaAssos")
EVALOP = list(map(int, getenv("EVALOP", "6797202080").split()))
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://rio:rio345@cluster0.p7rya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOGGER_ID = int(getenv("LOGGER_ID", -1002477649312))
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))

GPT_API = getenv("GPT_API", None )
DEEP_API = getenv("DEEP_API", None)
OWNER_ID = int(getenv("OWNER_ID", 6748827895))

# Heroku deployment settings - Refer to Heroku documentation on how to obtain these
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/doraemon890/ANNIE-X-MUSIC")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN", None)

# Support and contact information - Provide your own support channels
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/ThunderboltFantasy")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/BeAkatsuki")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "11500"))

# Server limits and configurations - These can be set based on your server configurations
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "3000"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "2500"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))

# External service credentials - Obtain these from Spotify
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")

# Telegram file size limits - Set these according to your requirements
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# Pyrogram session strings - You need to generate these yourself
STRING1 = getenv("STRING_SESSION", "BQGTFSMAqsr_sMqbk7ixXvEBP11nI8oUVeGKZA-e89RZGanRdX4aeHL1cICLs8QSfsb8j-UvMsbRVTTmNCH4xitAlnU45WqEvJP6tuZy62n6uW-3lOvL0KG0nr2OQYvdi81aRIa9MZ9zE14MBTRjDaRqdTCayuJYd6MIcp-pQlZIT0x6X2sNJXuVsGPY8p3MTIOgxbHGozL34rLsyw6U4YzHyUgCD0XBt-c0AeW3NRKz9z1B1fZWgoa3cfNJskI6rsmvrdoRb1nlqa_VP2rDiPIo1c7NJbqdEEFuC44GsjbnNOU7X4t**edtkE2Ks-A8FVGCoAR-9kq9CUyl-A8e6_pXeTsPtQAAAAHXrklAAA") 
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


# Bot introduction messages - These can be customized as per your preference
AYU = [
    "💞", "🦋", "🔍", "🧪", "🦋", "⚡️", "🔥", "🦋", "🎩", "🌈", "🍷", "🥂", "🦋", "🥃", "🥤", "🕊️",
    "🦋", "🦋", "🕊️", "🦋", "🕊️", "🦋", "🦋", "🦋", "🪄", "💌", "🦋", "🦋", "🧨"
]

AYUV = [ "<b>нєу</b> {0}, 💗\n\n๏ ᴛʜɪs ɪs {1} !\n\n➻ {1} ɪs ʏᴏᴜʀ ᴘᴇʀsᴏɴᴀʟ ᴍᴜsɪᴄ ᴄᴏᴍᴘᴀɴɪᴏɴ, ʜᴇʀᴇ ᴛᴏ ʙʀɪɴɢ ʜᴀʀᴍᴏɴʏ ᴛᴏ ʏᴏᴜʀ ᴅᴀʏ. EɴJᴏʏ sᴇᴀᴍʟᴇss ᴍᴜsɪᴄ ᴘʟᴀʏʙᴀᴄᴋ, ᴄᴜʀᴀᴛᴇᴅ ᴘʟᴀʏʟɪsᴛs, ᴀɴᴅ ᴇғғᴏʀᴛʟᴇss ᴄᴏɴᴛʀᴏʟ, ᴀʟʟ ᴀᴛ ʏᴏᴜʀ ғɪɴɢᴇʀᴛɪᴘs. Lᴇᴛ {1} ᴇʟᴇᴠᴀᴛᴇ ʏᴏᴜʀ ʟɪsᴛᴇɴɪɴɢ ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴡɪᴛʜ ᴇᴀsᴇ ᴀɴᴅ sᴛʏʟᴇ.\n\n<b><u>Sᴜᴘᴘᴏʀᴛᴇᴅ Pʟᴀᴛғᴏʀᴍs :</b></u> ʏᴏᴜᴛᴜʙᴇ, sᴘᴏᴛɪғʏ, ʀᴇssᴏ, ᴀᴘᴘʟᴇ ᴍᴜsɪᴄ ᴀɴᴅ sᴏᴜɴᴅᴄʟᴏᴜᴅ.\n──────────────────\n<b>๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs🦋.</b> "  ,
]

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/583bts.jpg"
)
PING_VID_URL = getenv(
    "PING_VID_URL", "https://telegra.ph/file/4be43ed2aa6872337e9a8.mp4"
)
PLAYLIST_IMG_URL = "https://files.catbox.moe/lo8fl3.jpg"
STATS_VID_URL = "https://files.catbox.moe/aodut1.mp4"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/fjpc10.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/fjpc10.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/ift7s0.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/ift7s0.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/ift7s0.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/lo8fl3.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/fjpc10.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/ift7s0.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
)
