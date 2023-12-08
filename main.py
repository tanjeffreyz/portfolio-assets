import json
import io
import base64
from glob import glob
from PIL import Image


OUTPUT_PATH = 'data/blur_data_urls.json'
IGNORED_DIRS = ['images/blog']
BLUR_SIZE = 8


urls = {}
for ext in ('png', 'jpg'):
    for path in glob(f'images/**/*.{ext}', recursive=True):
        path = path.replace('\\', '/')
        if any(map(lambda x: path.startswith(x), IGNORED_DIRS)):
            continue

        # Resize image to decrease response size
        img = Image.open(path).resize((BLUR_SIZE, BLUR_SIZE))
        output = io.BytesIO()
        img.save(output, format=ext)

        # Encode resized image binary data into base64
        data = output.getvalue()
        b64_string = base64.b64encode(data).decode('utf-8')
        data_url = f'data:image/jpg;base64,{b64_string}'
        urls[path] = data_url

with open(OUTPUT_PATH, 'w') as file:
    json.dump(urls, file)

print(f'[~] Finished processing {len(urls)} images')
