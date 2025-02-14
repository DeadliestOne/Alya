import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from ANNIEMUSIC import app
from config import YOUTUBE_IMG_URL  # Ensure you have this in your config

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

def create_square_thumbnail(img, size):
    img = img.resize((size, size))
    return img

def add_glowing_border(image, size, glow_color=(255, 0, 0), border_width=10, glow_intensity=15):
    border_size = size + 2 * border_width
    glow_image = Image.new("RGBA", (border_size, border_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_image)

    # Draw the square border
    draw.rectangle(
        [border_width, border_width, border_size - border_width, border_size - border_width],
        outline=glow_color, width=border_width
    )

    # Add glow effect by applying blur multiple times
    for _ in range(glow_intensity):
        glow_image = glow_image.filter(ImageFilter.GaussianBlur(2))
    
    # Paste the original image on top of the glowing border
    final_image = Image.new("RGBA", (border_size, border_size), (0, 0, 0, 0))
    final_image.paste(glow_image, (0, 0), glow_image)
    final_image.paste(image, (border_width, border_width), image)

    return final_image

async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_v5.png"):
        return f"cache/{videoid}_v5.png"

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
    background = image2.filter(ImageFilter.BoxBlur(20))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.6)
    draw = ImageDraw.Draw(background)
    arial = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 30)
    font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font.ttf", 30)
    title_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font3.ttf", 45)

    square_thumbnail = create_square_thumbnail(youtube, 400)
    
    # Add glowing border around the square thumbnail
    square_with_glow = add_glowing_border(square_thumbnail, 400, glow_color=(255, 0, 0), border_width=15, glow_intensity=10)
    square_position = (120, 160)
    background.paste(square_with_glow, square_position, square_with_glow)

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
    circle_radius = 10 
    draw.ellipse([end_point_red[0] - circle_radius, end_point_red[1] - circle_radius,
                  end_point_red[0] + circle_radius, end_point_red[1] + circle_radius], fill="red")

    draw.text((text_x_position, 400), "00:00", (255, 255, 255), font=arial)
    draw.text((1080, 400), duration, (255, 255, 255), font=arial)

    play_icons = Image.open("ANNIEMUSIC/assets/thumb/play_icons.png")
    play_icons = play_icons.resize((580, 62))
    background.paste(play_icons, (text_x_position, 450), play_icons)

    # Add watermark at the bottom
    watermark_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font.ttf", 25)
    draw.text((1050, 680), "@MitshBot", fill=(255, 255, 255, 150), font=watermark_font)

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except:
        pass
    background.save(f"cache/{videoid}_v5.png")
    return f"cache/{videoid}_v5.png"
