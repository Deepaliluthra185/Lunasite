# LunaSite 🌖
> **NASA Space Apps Challenge**: *"Sun and Earth positions at the Moon's south pole"*

LunaSite is an interactive 3D web application designed for mission planners, educators, and space enthusiasts to evaluate and compare lunar landing sites based on **solar illumination (power)** and **direct-to-Earth visibility (communications)**.

---

## 🚀 Key Features

* **Photorealistic 3D Moon & Celestial System**:
  * Authentic **NASA LROC WAC 2K color map** and **LOLA topographic bump map** rendered on a high-density 128×128 sphere with ACES Filmic Tone Mapping.
  * Realistic multi-stage **Sun** featuring blinding solar core, volumetric coronal flare sprites, and sharp airless shadows.
  * Real-time **Earth (Blue Marble)** with normal elevation, drifting cloud atmosphere, and Rayleigh blue rim scattering.
  * Physics-based lunar **Earthshine** illumination on the near-side dark hemisphere.
* **High-Precision NASA JPL DE440 Ephemeris**:
  * 96,408 hourly precomputed data points covering **2025–2035** using NASA NAIF SPICE kernels and the `MOON_ME` (Mean Earth/Polar Axis) frame.
  * Models true axial tilt ($1.54^\circ$) and full optical + physical libration ($\approx \pm 6.7^\circ$ lat, $\pm 7.9^\circ$ lon).
  * Validated against **NASA JPL Horizons API** with solar azimuth error $\le 0.001^\circ$ and solar elevation error $\le 0.006^\circ$ (< 18 arcseconds).
* **Mission Planning Telemetry & Analysis**:
  * **29.53-Day Synodic Timeline**: Interactive multi-track scrubber for Sun Up, Earth Link, and Simultaneous (Power & Comms) windows.
  * **Polar Radar Sky View**: 2D local horizon plot with concentric elevation rings ($0^\circ, 30^\circ, 60^\circ$) and collision-aware target tags.
  * **Go / Caution / No-Go Verdicts**: Calculated from continuous dark periods, solar elevation peaks, and power/comms availability.
  * **Landing Site Comparison Tray**: Compare up to 3 candidate landing sites or schedule slip dates side-by-side with CSV telemetry export.
  * **Preset Missions**: Apollo 11, 15, 17, Chandrayaan-3, Luna 25, IM-2 (Mons Mouton), Blue Ghost, Malapert massif, and Shackleton crater rim.

---

## 🛠️ Quick Start

LunaSite requires no complex build tools or backend servers. It runs as static HTML, CSS, and JavaScript.

### 1. Clone the Repository
```bash
git clone https://github.com/Deepaliluthra185/Lunasite.git
cd Lunasite
```

### 2. Start a Local Web Server
```bash
python -m http.server 8000
```
Open **[http://localhost:8000/index.html](http://localhost:8000/index.html)** in your browser.

---

## 🛰️ Data Pipeline & Science Validation

### NASA SPICE Kernels Used
* **JPL DE440 (`de440s.bsp`)**: High-precision planetary ephemeris.
* **Lunar Orientation PCK (`moon_pa_de421_1900-2050.bpc` & `moon_080317.tf`)**: High-accuracy `MOON_ME` body-fixed orientation and physical libration.
* **Planetary Constants (`pck00010.tpc`)**: Standard IAU Moon ellipsoidal parameters.
* **Leapseconds (`naif0012.tls`)**: UTC to TDB time conversion.

### Regenerating Ephemeris Data
```bash
pip install spiceypy numpy
python scripts/download_kernels.py
python scripts/generate_ephemeris.py
```

### Validating Against NASA JPL Horizons
```bash
python scripts/validate_ephemeris.py
```
Detailed benchmark comparison tables and verification notes can be found in [VALIDATION.md](VALIDATION.md).

---

## 📂 Project Structure

```text
├── index.html                 # Main single-page web application
├── AI_USAGE.md                # NASA Space Apps AI usage disclosure
├── VALIDATION.md              # JPL Horizons accuracy benchmark report
├── data/
│   └── ephemeris.json         # High-precision hourly SPICE ephemeris (2025–2035)
├── src/
│   └── ephemeris.js           # Client-side interpolation engine with offline fallback
├── textures/
│   ├── moon_color.jpg         # NASA LROC 2K lunar surface color mosaic
│   ├── moon_bump.jpg          # NASA LOLA 8-bit elevation bump map
│   ├── earth_color.jpg        # NASA Blue Marble surface map
│   ├── earth_normal.jpg       # Earth elevation normal map
│   └── earth_clouds.png       # Earth cloud layer
└── scripts/
    ├── download_kernels.py    # Downloads official NAIF SPICE kernels
    ├── generate_ephemeris.py  # Computes sub-solar & sub-Earth selenographic coords
    ├── validate_ephemeris.py  # Automated comparison with NASA JPL Horizons API
    └── test_browser.py        # Headless Playwright integration test
```

---

## 📜 Compliance & Disclosures
* **AI Assistance**: See [AI_USAGE.md](AI_USAGE.md) for full disclosure of AI tools utilized during development in accordance with NASA Space Apps Challenge guidelines.
* **License**: MIT
