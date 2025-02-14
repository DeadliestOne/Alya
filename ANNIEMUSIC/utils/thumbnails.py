import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from ANNIEMUSIC import app
from config import YOUTUBE_IMG_URL  # Ensure this exists in your config

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))

def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

def create_glow(img, blur_radius=20, glow_color=(0, 255, 0)):
    glow = img.copy().convert("RGBA")
    alpha = glow.split()[3]
    glow = ImageOps.colorize(alpha, black="black", white=glow_color)
    glow = glow.filter(ImageFilter.GaussianBlur(blur_radius))
    return glow

async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_v6.png"):
        return f"cache/{videoid}_v6.png"

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
    background = image2.filter(filter=ImageFilter.BoxBlur(20))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.6)
    draw = ImageDraw.Draw(background)
    arial = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 30)
    title_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font3.ttf", 45)
    
    # Create gradient border with glow effect
    thumbnail_size = 400
    img_with_border = create_glow(image1, blur_radius=15, glow_color=(0, 255, 127))
    border_image = Image.new("RGBA", (thumbnail_size + 40, thumbnail_size + 40), (0, 0, 0, 0))
    border_image.paste(img_with_border, (20, 20), img_with_border)
    background.paste(border_image, (100, 160), border_image)
    
    # Add title and info
    text_x_position = 565
    title1 = truncate(title)
    draw.text((text_x_position, 180), title1[0], fill=(255, 255, 255), font=title_font)
    draw.text((text_x_position, 230), title1[1], fill=(255, 255, 255), font=title_font)
    draw.text((text_x_position, 320), f"{channel}  |  {views[:23]}", (255, 255, 255), font=arial)

    # Progress bar
    line_length = 580  
    red_length = int(line_length * 0.6)
    white_length = line_length - red_length
    start_point_red = (text_x_position, 380)
    end_point_red = (text_x_position + red_length, 380)
    draw.line([start_point_red, end_point_red], fill="red", width=9)
    start_point_white = (text_x_position + red_length, 380)
    end_point_white = (text_x_position + line_length, 380)
    draw.line([start_point_white, end_point_white], fill="white", width=8)

    # Now Playing animation
    now_playing_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font.ttf", 25)
    draw.rectangle([text_x_position, 450, text_x_position + 150, 485], fill=(255, 0, 0, 180))
    draw.text((text_x_position + 10, 455), "Now Playing", fill=(255, 255, 255), font=now_playing_font)

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except:
        pass
    background.save(f"cache/{videoid}_v6.png")
    return f"cache/{videoid}_v6.png"
