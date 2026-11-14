import ssl, urllib.request, urllib.parse, spiceypy as spice, numpy as np

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

params = {
    'format': 'text',
    'COMMAND': "'399'",
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
print("HORIZONS OUTPUT for Earth:")
print(text[soe:eoe+5])

spice.furnsh('kernels/naif0012.tls')
spice.furnsh('kernels/pck00010.tpc')
spice.furnsh('kernels/moon_080317.tf')
spice.furnsh('kernels/moon_pa_de421_1900-2050.bpc')
spice.furnsh('kernels/de440s.bsp')

et = spice.str2et('2025-07-20T20:00:00')
earth_pos, _ = spice.spkpos('EARTH', et, 'MOON_ME', 'LT+S', 'MOON')
_, earth_lon, earth_lat = spice.reclat(earth_pos)
elat, elon = np.degrees(earth_lat), np.degrees(earth_lon)

lat, lon = 0.67, 23.47

def altaz(lat, lon, tgt_lat, tgt_lon):
    D2R = np.pi / 180.0
    R2D = 180.0 / np.pi
    p = lat * D2R
    dl = (tgt_lon - lon) * D2R
    t = tgt_lat * D2R
    se = np.sin(p)*np.sin(t) + np.cos(p)*np.cos(t)*np.cos(dl)
    el = np.arcsin(np.clip(se, -1.0, 1.0)) * R2D
    y = np.cos(t)*np.sin(dl)
    x = np.cos(p)*np.sin(t) - np.sin(p)*np.cos(t)*np.cos(dl)
    az = ((np.arctan2(y, x)*R2D) + 360.0) % 360.0
    return el, az

el_sub, az_sub = altaz(lat, lon, elat, elon)

r_moon = 1737.4
obs_pos_me = np.array([
    r_moon * np.cos(lat*np.pi/180) * np.cos(lon*np.pi/180),
    r_moon * np.cos(lat*np.pi/180) * np.sin(lon*np.pi/180),
    r_moon * np.sin(lat*np.pi/180)
])
earth_vec = earth_pos - obs_pos_me
up = obs_pos_me / np.linalg.norm(obs_pos_me)
north = np.array([-np.sin(lat*np.pi/180)*np.cos(lon*np.pi/180),
                  -np.sin(lat*np.pi/180)*np.sin(lon*np.pi/180),
                  np.cos(lat*np.pi/180)])
east = np.cross(north, up)
e_unit = earth_vec / np.linalg.norm(earth_vec)
el_topo = np.arcsin(np.dot(e_unit, up)) * 180 / np.pi
az_topo = (np.arctan2(np.dot(e_unit, east), np.dot(e_unit, north)) * 180 / np.pi + 360) % 360

print(f"SPICE MOON_ME subearth: elat={elat:.4f}°, elon={elon:.4f}°")
print(f"Computed from subearth: Az={az_sub:.4f}°, El={el_sub:.4f}°")
print(f"Topocentric 3D vector:  Az={az_topo:.4f}°, El={el_topo:.4f}°")

