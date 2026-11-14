import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://svs.gsfc.nasa.gov/4720/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as r:
    html = r.read().decode('utf-8')
    links = [l for l in re.findall(r'href="([^"]+)"', html) if any(x in l.lower() for x in ['ldem', 'topo', 'elev', 'bump', 'disp', 'norm'])]
    print("SVS 4720 elevation links:")
    for l in links[:20]:
        print(" ", l)

