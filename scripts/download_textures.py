import urllib.request, ssl, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

files = [
    ('https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/lroc_color_2k.jpg', 'textures/moon_color.jpg'),
    ('https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/ldem_3_8bit.jpg', 'textures/moon_bump.jpg'),
    ('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_atmos_2048.jpg', 'textures/earth_color.jpg'),
    ('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_normal_2048.jpg', 'textures/earth_normal.jpg'),
    ('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_clouds_1024.png', 'textures/earth_clouds.png')
]

os.makedirs('textures', exist_ok=True)

for url, dest in files:
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f'{dest} exists ({os.path.getsize(dest)} bytes)')
        continue
    print(f'Downloading {url} -> {dest} ...')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as r:
        with open(dest, 'wb') as f:
            while chunk := r.read(1024 * 1024):
                f.write(chunk)
    print(f'Saved {dest} ({os.path.getsize(dest)} bytes)')

# Also copy moon_color.jpg to moon.jpg in root for backward compatibility
if os.path.exists('textures/moon_color.jpg'):
    with open('textures/moon_color.jpg', 'rb') as fsrc, open('moon.jpg', 'wb') as fdst:
        fdst.write(fsrc.read())
    print('Copied to moon.jpg')

