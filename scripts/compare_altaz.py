import spiceypy as spice
import numpy as np

spice.furnsh('kernels/naif0012.tls')
spice.furnsh('kernels/pck00010.tpc')
spice.furnsh('kernels/moon_080317.tf')
spice.furnsh('kernels/moon_pa_de421_1900-2050.bpc')
spice.furnsh('kernels/de440s.bsp')

et = spice.str2et('2025-07-20T20:00:00')

# Frame MOON_ME
sun_pos, _ = spice.spkpos('SUN', et, 'MOON_ME', 'LT+S', 'MOON')
_, sun_lon, sun_lat = spice.reclat(sun_pos)
slat, slon = np.degrees(sun_lat), np.degrees(sun_lon)

# Observer: Apollo 11
lat, lon = 0.67, 23.47

def altaz(lat, lon, slat, slon):
    D2R = np.pi / 180.0
    R2D = 180.0 / np.pi
    p = lat * D2R
    dl = (slon - lon) * D2R
    t = slat * D2R
    se = np.sin(p)*np.sin(t) + np.cos(p)*np.cos(t)*np.cos(dl)
    el = np.arcsin(np.clip(se, -1.0, 1.0)) * R2D
    y = np.cos(t)*np.sin(dl)
    x = np.cos(p)*np.sin(t) - np.sin(p)*np.cos(t)*np.cos(dl)
    az = ((np.arctan2(y, x)*R2D) + 360.0) % 360.0
    return el, az

el, az = altaz(lat, lon, slat, slon)

print(f"SPICE MOON_ME subsolar: slat={slat:.4f}°, slon={slon:.4f}°")
print(f"Computed from subsolar: Az={az:.4f}°, El={el:.4f}°")
print(f"Horizons reported:      Az=273.5178°, El=-59.7872°")

# Also, SPICE topocentric directly at Apollo 11 site:
# Apollo 11 topocentric frame: surface normal, East, North
r_moon = 1737.4
obs_pos_me = np.array([
    r_moon * np.cos(lat*np.pi/180) * np.cos(lon*np.pi/180),
    r_moon * np.cos(lat*np.pi/180) * np.sin(lon*np.pi/180),
    r_moon * np.sin(lat*np.pi/180)
])

# Vector from Apollo 11 to Sun in MOON_ME
sun_vec = sun_pos - obs_pos_me
# Up vector (unit normal)
up = obs_pos_me / np.linalg.norm(obs_pos_me)
# North vector (tangent along meridian)
north = np.array([-np.sin(lat*np.pi/180)*np.cos(lon*np.pi/180),
                  -np.sin(lat*np.pi/180)*np.sin(lon*np.pi/180),
                  np.cos(lat*np.pi/180)])
# East vector = North x Up ? In right-handed system: Up x North = East? No: East = Up x North (if North is +y, Up is +z, East is -x?)
# Let's check: at lat=0, lon=0: Up=(1,0,0), North=(0,0,1). East should be (0,1,0). Up x North = (0,-1,0). So East = North x Up!
east = np.cross(north, up)

s_unit = sun_vec / np.linalg.norm(sun_vec)
el_topo = np.arcsin(np.dot(s_unit, up)) * 180 / np.pi
az_x = np.dot(s_unit, north)
az_y = np.dot(s_unit, east)
az_topo = (np.arctan2(az_y, az_x) * 180 / np.pi + 360) % 360

print(f"Topocentric 3D vector:  Az={az_topo:.4f}°, El={el_topo:.4f}°")

