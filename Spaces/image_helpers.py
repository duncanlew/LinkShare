import requests
import http.client, urllib
from PIL import Image
from io import BytesIO

def get_page_text(url):
    headers = {'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    n = requests.get(url, headers=headers)
    return n.text

def get_image_size(url):
    try:
        data = requests.get(url).content
        im = Image.open(BytesIO(data))
        return im.size
    except OSError as e:
        print(e)
        return 0,0
