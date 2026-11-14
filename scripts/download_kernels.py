import ssl, urllib.request, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

files = [
    ('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls', 'kernels/naif0012.tls'),
    ('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc', 'kernels/pck00010.tpc'),
    ('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/moon_pa_de421_1900-2050.bpc', 'kernels/moon_pa_de421_1900-2050.bpc'),
    ('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/satellites/moon_080317.tf', 'kernels/moon_080317.tf'),
    ('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp', 'kernels/de440s.bsp')
]

os.makedirs('kernels', exist_ok=True)
for url, dest in files:
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f'{dest} already exists ({os.path.getsize(dest)} bytes)')
        continue
    print(f'Downloading {url} -> {dest} ...')
    req = urllib.request.urlopen(url, context=ctx)
    with open(dest, 'wb') as f:
        while chunk := req.read(1024 * 1024):
            f.write(chunk)
    print(f'Saved {dest} ({os.path.getsize(dest)} bytes)')

print("Kernel download complete.")

