import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://svs.gsfc.nasa.gov/4720/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        html = r.read().decode('utf-8')
        links = re.findall(r'href="([^"]+\.(?:jpg|png|tif))"', html)
        print("SVS 4720 image links:")
        for l in links[:15]:
            print(" ", l)
except Exception as e:
    print("SVS error:", e)

# Test SolarSystemScope
for url in ['https://www.solarsystemscope.com/textures/download/2k_moon.jpg']:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as r:
            print(f'{url}: {r.info().get("Content-Length")} bytes, status {r.status}')
    except Exception as e:
        print(f'{url}: error {e}')

