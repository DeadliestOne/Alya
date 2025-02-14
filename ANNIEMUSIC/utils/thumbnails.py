import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from ANNIEMUSIC import app
from config import YOUTUBE_IMG_URL

# Utility function to resize the image
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

# Utility function to truncate long text
def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

# Function to create a square thumbnail without blur or glow
def create_square_thumbnail(img, size):
    img = img.resize((size, size), Image.LANCZOS)  # Resize to the exact square size
    square_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    square_img.paste(img, (0, 0))
    return square_img

# Main function to generate the thumbnail
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

    youtube = Image.open(f"cache/thumb{videoid}.png")
    image1 = changeImageSize(1280, 720, youtube)
    image2 = image1.convert("RGBA")
    background = image2.filter(ImageFilter.GaussianBlur(15))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.6)
    draw = ImageDraw.Draw(background)

    # "Now Playing" with red vertical bar
    now_playing_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 35)
    draw.text((50, 50), "|", fill="red", font=now_playing_font)
    draw.text((80, 50), "Mitsuha Now Playing", fill=(255, 255, 255), font=now_playing_font)

    arial = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 30)
    font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font.ttf", 30)
    title_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font3.ttf", 45)

    # Add square thumbnail with real image (no blur or glow)
    square_thumbnail = create_square_thumbnail(youtube, 400)
    square_position = (120, 160)
    background.paste(square_thumbnail, square_position)

    # Add text
    text_x_position = 565
    title1 = truncate(title)
    draw.text((text_x_position, 180), title1[0], fill=(255, 255, 255), font=title_font)
    draw.text((text_x_position, 230), title1[1], fill=(255, 255, 255), font=title_font)
    draw.text((text_x_position, 320), f"{channel}  |  {views[:23]}", (255, 255, 255), font=arial)

    # Progress bar
    line_length = 580
    red_length = int(line_length * 0.6)
    white_length = line_length - red_length
    draw.line([(text_x_position, 380), (text_x_position + red_length, 380)], fill="red", width=9)
    draw.line([(text_x_position + red_length, 380), (text_x_position + line_length, 380)], fill="white", width=8)
    circle_radius = 10
    draw.ellipse([(text_x_position + red_length - circle_radius, 380 - circle_radius),
                  (text_x_position + red_length + circle_radius, 380 + circle_radius)], fill="red")

    draw.text((text_x_position, 400), "00:00", (255, 255, 255), font=arial)
    draw.text((1080, 400), duration, (255, 255, 255), font=arial)

    # Play icons
    play_icons = Image.open("ANNIEMUSIC/assets/thumb/play_icons.png").resize((580, 62))
    background.paste(play_icons, (text_x_position, 450), play_icons)

    # Add watermark
    watermark_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font.ttf", 25)
    draw.text((1050, 680), "@MitshBot", fill=(255, 255, 255, 150), font=watermark_font)

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except:
        pass

    background.save(f"cache/{videoid}_custom.png")
    return f"cache/{videoid}_custom.png"
