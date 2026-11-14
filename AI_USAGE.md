# AI Usage Disclosure (NASA Space Apps Challenge)

In compliance with NASA Space Apps Challenge guidelines, this document records all AI assistance utilized during the development of LunaSite.

## Tools & Models
- **AI Model**: Google DeepMind Agentic AI Assistant (Gemini 3.8 Flash)
- **Role**: Architecture design, ephemeris data pipeline engineering, SPICE/Horizons validation, and UI integration.

## Tasks & Actions Taken by AI
1. **Repository Structure Analysis**:
   - Analyzed `index.html` structure (Three.js 3D sphere, lighting, celestial trigonometry, synodic cycle calculations, DOM event loops).
2. **Ephemeris Data Pipeline (`scripts/download_kernels.py`, `scripts/generate_ephemeris.py`)**:
   - Downloaded official NASA NAIF SPICE kernels (`de440s.bsp`, `pck00010.tpc`, `naif0012.tls`, `moon_pa_de421_1900-2050.bpc`, `moon_080317.tf`).
   - Built a high-precision hourly selenographic ephemeris table generator using `spiceypy` with the `MOON_ME` (Mean Earth/Polar Axis) frame accounting for full optical and physical libration.
   - Outputted `data/ephemeris.json` (96,408 hourly records spanning 2025–2035).
3. **Rigorous Validation Against NASA JPL Horizons (`scripts/validate_ephemeris.py`, `VALIDATION.md`)**:
   - Validated ephemeris interpolation output against the live NASA JPL Horizons API for Apollo 11 (`0.67° N, 23.47° E`) at multiple timestamps.
   - Demonstrated solar azimuth accuracy within `0.001°` and solar elevation within `0.006°` (compared to up to `3.86°` error in the old analytic model).
4. **Frontend Integration**:
   - Integrated `src/ephemeris.js` into `index.html`, preserving the `sunEarth(d)` signature with automatic graceful fallback to the analytic model when offline or out-of-range.
5. **Photorealistic 3D Visuals & UI Polish**:
   - Integrated authentic NASA LROC 2K color map (`textures/moon_color.jpg`) and LOLA topographic bump map (`textures/moon_bump.jpg`) on a 128x128 segment lunar sphere with ACES Filmic Tone Mapping.
   - Built realistic multi-stage Sun with radiant core, dual-layer coronal halo, solar flare glare sprites, and physical directional lighting.
   - Constructed realistic NASA Blue Marble Earth with dual-layer cloud sphere, axial rotation, and Rayleigh atmospheric blue rim glow.
   - Added subtle lunar near-side Earthshine lighting and 3,500 multi-spectral deep space starfield.
   - Upgraded UI with modern aerospace glassmorphism styling, telemetry chips, collision-aware polar radar, and refined synodic timeline tracks.

