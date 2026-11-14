import spiceypy as spice
import numpy as np
import datetime

# Load kernels
spice.furnsh('kernels/naif0012.tls')
spice.furnsh('kernels/pck00010.tpc')
spice.furnsh('kernels/moon_080317.tf')
spice.furnsh('kernels/moon_pa_de421_1900-2050.bpc')
spice.furnsh('kernels/de440s.bsp')

# Test date: Apollo 11 landing time (1969 is outside de440s which starts 1980, so let's test 2025-07-20 20:17:40 UTC)
utc_str = '2025-07-20T20:17:40'
et = spice.str2et(utc_str)

# Calculate sub-solar point and sub-Earth point on the Moon
# Frame: IAU_MOON (Mean Earth / Polar Axis) or MOON_ME
frame = 'MOON_ME' # or 'IAU_MOON'

# Position of Sun relative to Moon center in lunar body-fixed frame
sun_pos, _ = spice.spkpos('SUN', et, frame, 'LT+S', 'MOON')
sun_r, sun_lon, sun_lat = spice.reclat(sun_pos)

# Position of Earth relative to Moon center in lunar body-fixed frame
earth_pos, _ = spice.spkpos('EARTH', et, frame, 'LT+S', 'MOON')
earth_r, earth_lon, earth_lat = spice.reclat(earth_pos)

print(f"Date: {utc_str}")
print(f"MOON_ME:")
print(f"Sun  lat: {np.degrees(sun_lat):.4f}°, lon: {np.degrees(sun_lon):.4f}°")
print(f"Earth lat: {np.degrees(earth_lat):.4f}°, lon: {np.degrees(earth_lon):.4f}°")

# Also test IAU_MOON to see difference
sun_pos_iau, _ = spice.spkpos('SUN', et, 'IAU_MOON', 'LT+S', 'MOON')
_, sun_lon_iau, sun_lat_iau = spice.reclat(sun_pos_iau)
earth_pos_iau, _ = spice.spkpos('EARTH', et, 'IAU_MOON', 'LT+S', 'MOON')
_, earth_lon_iau, earth_lat_iau = spice.reclat(earth_pos_iau)

print(f"IAU_MOON:")
print(f"Sun  lat: {np.degrees(sun_lat_iau):.4f}°, lon: {np.degrees(sun_lon_iau):.4f}°")
print(f"Earth lat: {np.degrees(earth_lat_iau):.4f}°, lon: {np.degrees(earth_lon_iau):.4f}°")

spice.kclear()
