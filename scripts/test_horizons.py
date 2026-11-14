import ssl, urllib.request, urllib.parse, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

params = {
    'format': 'text',
    'COMMAND': "'10'",
    'EPHEM_TYPE': "'OBSERVER'",
    'CENTER': "'coord@301'",
    'COORD_TYPE': "'GEODETIC'",
    'SITE_COORD': "'23.47,0.67,0'",
    'START_TIME': "'2025-07-20 20:00'",
    'STOP_TIME': "'2025-07-20 21:00'",
    'STEP_SIZE': "'1 h'",
    'QUANTITIES': "'4'"
}

url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(params)
req = urllib.request.urlopen(url, context=ctx)
text = req.read().decode('utf-8')

soe = text.find('$$SOE')
eoe = text.find('$$EOE')
if soe != -1 and eoe != -1:
    print("HORIZONS OUTPUT for Sun:")
    print(text[soe:eoe+5])
else:
    print("OUTPUT (full):", text[:1500])
