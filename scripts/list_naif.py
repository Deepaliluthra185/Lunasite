import ssl, urllib.request, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/'
req = urllib.request.urlopen(url, context=ctx)
html = req.read().decode('utf-8')
matches = [m for m in re.findall(r'href="([^"]+)"', html) if 'de' in m]
print(matches[:20])

