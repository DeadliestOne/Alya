import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from ANNIEMUSIC import app
from config import YOUTUBE_IMG_URL  # Ensure this is correctly set up in your config

# Utility function to resize the image
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight), Image.LANCZOS)
    return newImage

# Utility function to truncate long text
def truncate(text, max_len=30):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < max_len:
            text1 += " " + word
        elif len(text2) + len(word) < max_len:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

# Main function to generate the thumbnail with higher resolution and PNG format
async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_custom.png"):
        return f"cache/{videoid}_custom.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)
    for result in (await results.next())["result"]:
        title = result.get("title", "Unsupported Title").title()
        duration = result.get("duration", "Unknown Mins")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    youtube = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")
    image1 = changeImageSize(1920, 1080, youtube)
    image2 = image1.convert("RGBA")
    background = image2.filter(ImageFilter.GaussianBlur(10))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.7)
    draw = ImageDraw.Draw(background)

    # "Now Playing" text with red vertical bar
    now_playing_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 40)
    draw.text((50, 50), "|", fill="red", font=now_playing_font)
    draw.text((80, 50), "Mitsuha Now Playing", fill=(255, 255, 255), font=now_playing_font)

    arial = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 35)
    title_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font3.ttf", 50)
    watermark_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font.ttf", 30)

    # Add square thumbnail
    square_img = youtube.resize((500, 500), Image.LANCZOS)
    background.paste(square_img, (150, 200))

    # Add title text
    title1 = truncate(title)
    draw.text((700, 220), title1[0], fill=(255, 255, 255), font=title_font)
    draw.text((700, 280), title1[1], fill=(255, 255, 255), font=title_font)
    draw.text((700, 380), f"{channel}  |  {views}", fill=(255, 255, 255), font=arial)

    # Progress bar
    line_length = 600
    red_length = int(line_length * 0.6)
    draw.line([(700, 460), (700 + red_length, 460)], fill="red", width=10)
    draw.line([(700 + red_length, 460), (700 + line_length, 460)], fill="white", width=8)
    circle_radius = 12
    draw.ellipse([(700 + red_length - circle_radius, 460 - circle_radius),
                  (700 + red_length + circle_radius, 460 + circle_radius)], fill="red")
    draw.text((700, 500), "00:00", fill=(255, 255, 255), font=arial)
    draw.text((1250, 500), duration, fill=(255, 255, 255), font=arial)

    # Play icons
    play_icons = Image.open("ANNIEMUSIC/assets/thumb/play_icons.png").resize((600, 70))
    background.paste(play_icons, (700, 550), play_icons)

    # Add watermark
    draw.text((1400, 1000), "@MitsuhaBot", fill=(255, 255, 255), font=watermark_font)

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except:
        pass

    background.save(f"cache/{videoid}_custom.png", format="PNG")
    return f"cache/{videoid}_custom.png"
