import requests
from PIL import Image
from io import StringIO
import PIL
import numpy as np
from resizeimage import resizeimage
import glob, os
import pyodbc
import datetime
from PIL import ImageFont
from PIL import ImageDraw
import cv2
import datetime
import textwrap
import time

# Server details

for fb_post in (fb_posts):
    created_time = fb_post[4]
    likes = fb_post[5]
    shares = fb_post[6]
    comments = fb_post[7]
    link_to_post = fb_post[8]
    message = fb_post[10]
    jpg_url = fb_post[12]

    print (link_to_post)

    likes = round(likes)
    shares = round(shares)
    comments = round(comments)

    created_time_cut = datetime.datetime.strptime(str(created_time), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    created_time_cut_two = datetime.datetime.strptime(str(created_time), '%Y-%m-%d %H:%M:%S').strftime('%d %B %Y')

    # Download images

    r = requests.get(jpg_url, allow_redirects=True)
    image_save = open('tbs_image.jpg', 'wb').write(r.content)

    # Resize image

    size = 680, 400
    try:
        for infile in glob.glob("tbs_image.jpg"):

            file, ext = os.path.splitext(infile)
            im = Image.open(infile)
            im.thumbnail(size)
            im.save("tbs_image" + ".jpg", "JPEG")

            template = Image.open('template_use.jpg')
            fb_image = Image.open('tbs_image.jpg')

            image_copy = template.copy()
            position = (40, 70)
            image_copy.paste(fb_image, position)
            image_copy.save('fb_post_'+created_time_cut+'.jpg')

            roboto = ImageFont.truetype("Roboto-Light.ttf", 11)
            roboto_small = ImageFont.truetype("Roboto-Light.ttf", 10)
            calibri = ImageFont.truetype("Calibri_Bold.ttf", 12)
            img = Image.open('fb_post_'+str(created_time_cut)+'.jpg')
            draw = ImageDraw.Draw(img)
            draw.text((40, 515), str(likes)+" Likes", fill="#365899",font = roboto)
            draw = ImageDraw.Draw(img)
            draw.text((130, 515), str(shares)+" Shares", fill="#365899",font = roboto)
            draw = ImageDraw.Draw(img)
            draw.text((220, 515), str(comments)+" Comments", fill="#365899",font = roboto)
            draw = ImageDraw.Draw(img)
            draw.text((167, 13), str(created_time_cut_two), (0, 0, 0), font=roboto_small)
            draw = ImageDraw.Draw(img)

            img.save('fb_post_' + str(created_time_cut) + '.jpg')
            y = 30
            novo = textwrap.wrap(message, width=85)
            for mesage_wrapped in novo:
                draw.text((50, y), mesage_wrapped, (0, 0, 0), font=roboto)
                draw = ImageDraw.Draw(img)
                y = y + 10
                img.save('fb_post_'+ str(created_time_cut)+'.jpg')
                time.sleep(1)

    except Exception as errr:
        print (errr)
        pass
