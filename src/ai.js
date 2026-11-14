/**
 * src/ai.js
 * Google Gemini 2.5 Flash AI integration for LunaSite:
 * 1. Natural Language Landing Site Search
 * 2. Mission Telemetry Explainer & Flight Director Briefing
 * 3. Multi-Site Comparison Trade Study Summarizer
 */

(function (root) {
  const MODEL = "gemini-2.5-flash";

  function getApiKey() {
    const saved = localStorage.getItem("lunasite_gemini_key");
    if (saved && saved.trim()) return saved.trim();
    try {
      return atob("QVEuQWI4Uk42TDRBTzNjQkRLblJMaFZMdGhjQm5PN0NqUlJXcFB3bXg0VTNYSUpKWHJ3T0E=");
    } catch (e) {
      return "";
    }
  }

  function setApiKey(key) {
    if (key) localStorage.setItem("lunasite_gemini_key", key);
    else localStorage.removeItem("lunasite_gemini_key");
  }

  async function callGemini(promptText) {
    const key = getApiKey();
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${key}`;
    const payload = {
      contents: [
        {
          parts: [{ text: promptText }]
        }
      ],
      generationConfig: {
        temperature: 0.2,
        maxOutputTokens: 800
      }
    };

    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(`Gemini API error (HTTP ${resp.status}): ${errText}`);
    }

    const data = await resp.json();
    if (!data.candidates || !data.candidates[0] || !data.candidates[0].content) {
      throw new Error("Invalid or empty response from Gemini API.");
    }

    return data.candidates[0].content.parts[0].text;
  }

  /**
   * 1. Natural Language Site Search
   */
  async function searchSites(query, availableSites) {
    const siteCatalog = availableSites
      .map(s => `- ${s.n} (Lat: ${s.lat}°, Lon: ${s.lon}°, Mission: ${s.t})`)
      .join("\n");

    const prompt = `You are the AI mission navigator for LunaSite, a lunar landing site explorer for the NASA Space Apps Challenge.
Given a user's natural language search query, identify the most suitable lunar landing site.

Available Preset Sites:
${siteCatalog}

Rules:
1. If the user asks for a specific historical or current mission (e.g., "Apollo 11", "Chandrayaan", "IM-2", "Malapert", "Shackleton"), match that site.
2. If the user describes operational criteria (e.g. "South pole with good Earth visibility", "Site near 85S", "Equatorial landing"), select the best matching preset site or output specific coordinates.
3. Respond ONLY with valid JSON in this exact structure, enclosed in \`\`\`json ... \`\`\` or raw JSON:
{
  "site_name": "Name of site",
  "lat": 0.0,
  "lon": 0.0,
  "reason": "Clear 1-2 sentence explanation of why this site matches the query."
}

User Query: "${query.replace(/"/g, '\\"')}"`;

    const rawText = await callGemini(prompt);
    
    // Extract JSON block
    let jsonStr = rawText.trim();
    const match = jsonStr.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
    if (match) {
      jsonStr = match[1];
    }

    try {
      return JSON.parse(jsonStr);
    } catch (e) {
      console.warn("Failed to parse JSON from Gemini search response:", rawText);
      return {
        site_name: "Custom Search Result",
        lat: -85.9,
        lon: 0.0,
        reason: rawText.slice(0, 160)
      };
    }
  }

  /**
   * 2. Site Mission Explainer (Flight Director Briefing)
   */
  async function explainTelemetry(site, dateStr, k, a, verdictText) {
    const prompt = `You are the AI Chief Flight Director for LunaSite (NASA Space Apps Challenge).
Analyze the following deterministic mission telemetry computed for a lunar landing site:

Site: ${site.n} (${site.lat.toFixed(2)}° Lat, ${site.lon.toFixed(2)}° Lon)
Timestamp: ${dateStr} UTC
Verdict: ${verdictText} (Score: ${(a.score * 100).toFixed(0)}/100)
Sun Elevation: ${k.sun.el.toFixed(1)}° (Azimuth: ${k.sun.az.toFixed(0)}°) - ${k.sun.el > 0 ? "Illuminated" : "In shadow"}
Earth Elevation: ${k.earth.el.toFixed(1)}° (Azimuth: ${k.earth.az.toFixed(0)}°) - ${k.earth.el > 0 ? "Line of sight active" : "Below horizon"}
Sunlight this 29.5-day cycle: ${(a.sunF * 100).toFixed(0)}% (Peak elevation: ${a.peak.toFixed(1)}°)
Earth Visible this cycle: ${(a.earF * 100).toFixed(0)}% (Simultaneous Sun & Earth: ${(a.bothF * 100).toFixed(0)}%)
Longest continuous shadow window: ${a.longest} hours (${(a.longest / 24).toFixed(1)} days)

Provide a concise, high-impact 3-part operational assessment formatted in clean HTML paragraphs with <b> tags:
1. <b>Power Architecture</b>: How the solar grazing angle and peak elevation affect solar array deployment (e.g. vertical solar panels/towers vs flat arrays).
2. <b>Communication Link</b>: Direct-to-Earth (DTE) radio comms feasibility given Earth's elevation and risk of terrain masking.
3. <b>Thermal & Night Survival</b>: Energy storage requirements (regenerative fuel cells, high-density batteries) to survive the longest continuous shadow window.

Keep the response concise, authoritative, and strictly scientific (under 180 words total). Do NOT use markdown asterisks (use <b> and <p> instead).`;

    return await callGemini(prompt);
  }

  /**
   * 3. Comparison Trade Study Summarizer
   */
  async function summarizeComparison(candidates) {
    const list = candidates.map((c, i) =>
      `Option ${i + 1}: ${c.n} (Date: ${c.d})\n- Verdict: ${c.v} (Score: ${(c.score * 100).toFixed(0)}/100)\n- Sunlight: ${(c.sunF * 100).toFixed(0)}%\n- Earth Comms Link: ${(c.earF * 100).toFixed(0)}%`
    ).join("\n\n");

    const prompt = `You are the AI Mission Trade Study Analyst for LunaSite.
Synthesize the trade-offs between the following compared lunar landing site candidates:

${list}

Provide a concise trade study summary formatted in clean HTML:
<p><b>Core Trade-Off:</b> [Compare power availability vs direct-to-Earth communication link across the options].</p>
<p><b>Recommendation:</b> [Clear operational recommendation explaining which candidate is superior for power-limited landers vs communication-critical missions].</p>

Keep the total summary under 140 words. Strictly avoid markdown; use HTML tags only.`;

    return await callGemini(prompt);
  }

  // Export to global scope
  root.LunaAI = {
    searchSites,
    explainTelemetry,
    summarizeComparison,
    getApiKey,
    setApiKey
  };

})(typeof window !== "undefined" ? window : global);
