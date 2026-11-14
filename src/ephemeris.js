/**
 * src/ephemeris.js
 * High-precision Lunar Ephemeris loader and interpolator.
 * 
 * Uses precomputed JPL DE440 + MOON_ME SPICE kernels (data/ephemeris.json)
 * with graceful fallback to the analytic model if offline or out of range.
 */

(function (root) {
  const SYNODIC = 29.530588; // days
  let ephemerisData = null;
  let isLoaded = false;
  let loadListeners = [];

  function interpAngle(a0, a1, frac) {
    let diff = a1 - a0;
    if (diff > 180.0) diff -= 360.0;
    else if (diff < -180.0) diff += 360.0;
    let res = a0 + frac * diff;
    if (res > 180.0) res -= 360.0;
    else if (res < -180.0) res += 360.0;
    return res;
  }

  function analyticSunEarth(d) {
    const days = (d.getTime() - Date.UTC(2000, 0, 6, 18, 14)) / 864e5;
    const f = ((days / SYNODIC) % 1 + 1) % 1;
    let slon = 180 - 360 * f;
    slon = ((slon + 540) % 360) - 180;
    const slat = 1.54 * Math.sin(2 * Math.PI * days / 346.62); // approx. solar declination
    const elon = 7.9 * Math.sin(2 * Math.PI * days / 27.5546); // optical libration in lon
    const elat = 6.7 * Math.sin(2 * Math.PI * days / 27.2122); // libration in lat
    return {
      sun: { lat: slat, lon: slon },
      earth: { lat: elat, lon: elon },
      source: "Analytic approximation"
    };
  }

  function sunEarth(d) {
    if (isLoaded && ephemerisData && ephemerisData.data) {
      const t_ms = d.getTime();
      const idx_f = (t_ms - ephemerisData.t0) / ephemerisData.step_ms;
      if (idx_f >= 0 && idx_f < ephemerisData.count - 1) {
        const i0 = Math.floor(idx_f);
        const i1 = i0 + 1;
        const frac = idx_f - i0;
        const p0 = ephemerisData.data[i0];
        const p1 = ephemerisData.data[i1];

        const slat = p0[0] + frac * (p1[0] - p0[0]);
        const slon = interpAngle(p0[1], p1[1], frac);
        const elat = p0[2] + frac * (p1[2] - p0[2]);
        const elon = interpAngle(p0[3], p1[3], frac);

        return {
          sun: { lat: slat, lon: slon },
          earth: { lat: elat, lon: elon },
          source: "JPL DE440 / SPICE (MOON_ME)"
        };
      }
    }
    return analyticSunEarth(d);
  }

  function loadEphemeris(jsonPath = "data/ephemeris.json") {
    fetch(jsonPath)
      .then(resp => {
        if (!resp.ok) throw new Error("HTTP " + resp.status);
        return resp.json();
      })
      .then(data => {
        ephemerisData = data;
        isLoaded = true;
        console.log(`[LunaSite] High-precision ephemeris loaded (${data.count} points, ${data.t0_iso} to 2035).`);
        loadListeners.forEach(fn => fn(true, data));
      })
      .catch(err => {
        console.warn("[LunaSite] Could not load ephemeris.json, using analytic fallback:", err.message);
        loadListeners.forEach(fn => fn(false, err));
      });
  }

  function onEphemerisLoaded(cb) {
    if (isLoaded) {
      cb(true, ephemerisData);
    } else {
      loadListeners.push(cb);
    }
  }

  // Export functions to global or root
  root.sunEarth = sunEarth;
  root.analyticSunEarth = analyticSunEarth;
  root.loadEphemeris = loadEphemeris;
  root.onEphemerisLoaded = onEphemerisLoaded;
  root.isEphemerisLoaded = () => isLoaded;

})(typeof window !== "undefined" ? window : global);

