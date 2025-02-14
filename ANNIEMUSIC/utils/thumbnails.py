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


def create_circular_thumbnail(img, size, glow_color=(0, 255, 0)):
    img = img.resize((size, size))
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    circular_img = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
    circular_img.putalpha(mask)

    glow = Image.new("RGBA", (size + 40, size + 40), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for i in range(20):
        glow_draw.ellipse(
            (i, i, size + 40 - i, size + 40 - i), outline=glow_color + (10,), width=2
        )

    final_img = Image.new("RGBA", (size + 40, size + 40), (0, 0, 0, 0))
    final_img.paste(glow, (0, 0), glow)
    final_img.paste(circular_img, (20, 20), circular_img)
    return final_img


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_cool.png"):
        return f"cache/{videoid}_cool.png"

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

    # Create gradient background
    background = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    gradient = Image.new("L", (1, 720), color=0xFF)
    for x in range(1280):
        gradient.putpixel((0, x), int(255 * (1 - x / 1280)))
    gradient = gradient.resize((1280, 720))
    background.paste((50, 50, 150), (0, 0), gradient)

    draw = ImageDraw.Draw(background)
    title_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font3.ttf", 45)
    info_font = ImageFont.truetype("ANNIEMUSIC/assets/thumb/font2.ttf", 30)

    # Add Circular Thumbnail with Glow
    circular_thumbnail = create_circular_thumbnail(youtube, 400)
    background.paste(circular_thumbnail, (50, 150), circular_thumbnail)

    # Draw Text
    draw.text((500, 180), title, fill=(255, 255, 255), font=title_font)
    draw.text((500, 250), f"{channel}  |  {views[:23]}", (200, 200, 200), font=info_font)
    draw.text((500, 300), f"Duration: {duration}", (200, 200, 200), font=info_font)

    # Add a Curved Progress Bar
    draw.arc((500, 400, 1000, 500), start=0, end=216, fill="green", width=5)
    draw.text((500, 520), "00:00", (255, 255, 255), font=info_font)
    draw.text((950, 520), duration, (255, 255, 255), font=info_font)

    # Add floating music symbols
    draw.text((100, 600), "♪ ♫ ♬", fill=(255, 255, 255, 120), font=info_font)

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except:
        pass
    background.save(f"cache/{videoid}_cool.png")
    return f"cache/{videoid}_cool.png"
