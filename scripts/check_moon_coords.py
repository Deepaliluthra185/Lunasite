from PIL import Image

im = Image.open('textures/moon_color.jpg')
w, h = im.size
print(f"Image size: {w}x{h}")

# The near side (Mare Serenitatis, Tranquillitatis, Imbrium, Oceanus Procellarum) has large dark basaltic maria.
# The far side (lunar highlands) is mostly bright cratered terrain with very few maria (except Mare Moscoviense).
# Let's compute average brightness of left half, center half, right half:
# Far side vs Near side
quarter = w // 4
left = im.crop((0, 0, quarter, h)).convert('L')
center = im.crop((quarter, 0, 3*quarter, h)).convert('L')
right = im.crop((3*quarter, 0, w, h)).convert('L')

import numpy as np
print("Mean brightness (0=dark, 255=bright):")
print(f"Left quarter (u: 0.0 - 0.25):   {np.mean(left):.1f}")
print(f"Center half (u: 0.25 - 0.75):   {np.mean(center):.1f}")
print(f"Right quarter (u: 0.75 - 1.0):  {np.mean(right):.1f}")

# Sample specific locations:
# If center (u=0.5, v=0.5) is Prime Meridian (lat 0, lon 0):
# Mare Tranquillitatis is around lat 8N, lon 31E -> u ≈ 0.5 + 31/360 = 0.586, v ≈ 0.5 + 8/180 = 0.544 (y from bottom)
# In image coords: x ≈ 0.586 * w, y ≈ (1 - 0.544) * h = 0.456 * h
# Oceanus Procellarum is West (lon -40 to -60) -> u ≈ 0.5 - 50/360 = 0.361
px_tranquillitatis = im.getpixel((int(0.586 * w), int(0.456 * h)))
px_procellarum = im.getpixel((int(0.361 * w), int(0.456 * h)))
px_far_side = im.getpixel((int(0.05 * w), int(0.5 * h)))

print(f"Pixel at Tranquillitatis (u=0.586): {px_tranquillitatis}")
print(f"Pixel at Procellarum (u=0.361):    {px_procellarum}")
print(f"Pixel at Far Side (u=0.05):        {px_far_side}")

