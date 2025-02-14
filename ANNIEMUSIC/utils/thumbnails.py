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

# Function to create glow effect for text
def draw_glow_text(draw, position, text, font, glow_color, text_color):
    x, y = position
    for offset in range(-3, 4):
        draw.text((x + offset, y), text, font=font, fill=glow_color)
        draw.text((x, y + offset), text, font=font, fill=glow_color)
    draw.text((x, y), text, font=font, fill=text_color)

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

    youtube = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")
    image1 = changeImageSize(1280, 720, youtube)
    image2 = image1.convert("RGBA")
    background = image2.filter(ImageFilter.GaussianBlur(15))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.6)
    draw = ImageDraw.Draw(background)

    # Now Playing with red vertical bar
    now_playing_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 35)
    draw.text((50, 50), "|", fill="red", font=now_playing_font)
    draw.text((80, 50), "Mitsuha Now Playing", fill=(255, 255, 255), font=now_playing_font)

    arial = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 30)
    title_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font3.ttf", 45)
    watermark_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font.ttf", 25)

    # Add square thumbnail
    square_img = youtube.resize((400, 400), Image.LANCZOS)
    background.paste(square_img, (120, 160))

    # Add text with glow effect
    title1 = truncate(title)
    draw_glow_text(draw, (565, 180), title1[0], title_font, (0, 0, 0), (255, 255, 255))
    draw_glow_text(draw, (565, 230), title1[1], title_font, (0, 0, 0), (255, 255, 255))
    draw.text((565, 320), f"{channel}  |  {views[:23]}", fill=(255, 255, 255), font=arial)

    # Progress bar
    line_length = 580
    red_length = int(line_length * 0.6)
    draw.line([(565, 380), (565 + red_length, 380)], fill="red", width=9)
    draw.line([(565 + red_length, 380), (565 + line_length, 380)], fill="white", width=8)
    circle_radius = 10
    draw.ellipse([(565 + red_length - circle_radius, 380 - circle_radius),
                  (565 + red_length + circle_radius, 380 + circle_radius)], fill="red")
    draw.text((565, 400), "00:00", fill=(255, 255, 255), font=arial)
    draw.text((1080, 400), duration, fill=(255, 255, 255), font=arial)

    # Play icons
    play_icons = Image.open("ANNIEMUSIC/assets/thumb/play_icons.png").resize((580, 62))
    background.paste(play_icons, (565, 450), play_icons)

    # Add watermark with glow effect
    draw_glow_text(draw, (1050, 680), "@MitshBot", watermark_font, (0, 0, 0), (255, 255, 255))

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except:
        pass

    background.save(f"cache/{videoid}_custom.png")
    return f"cache/{videoid}_custom.png"
