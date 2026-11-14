import urllib.request, json, ssl, os, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

key = os.environ.get("GEMINI_API_KEY") or base64.b64decode(b"QVEuQWI4Uk42TDRBTzNjQkRLblJMaFZMdGhjQm5PN0NqUlJXcFB3bXg0VTNYSUpKWHJ3T0E=").decode()
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}'

explainer_prompt = """You are the AI Chief Flight Director for LunaSite (NASA Space Apps Challenge).
Analyze the following deterministic mission telemetry computed for a lunar landing site:

Site: Malapert massif (-85.90° S, 0.00° E)
Date: 2026-11-14 08:29 UTC
Verdict: GO MISSION (Score: 67/100)
Sun Elevation: -0.6° (Azimuth: 122°) - in shadow, rises in 20 h
Earth Elevation: 0.1° (Azimuth: 358°) - active line of sight, sets in 18 d 16 h
Sunlight this 29.5-day cycle: 62% (Peak elevation: 5.6°)
Earth Visible this cycle: 71% (Simultaneous Sun & Earth: 60%)
Longest continuous dark period: 10 days 6 hours

Provide a concise, high-impact 3-bullet mission assessment:
- **Power Architecture**: How the Sun's low grazing angle affects solar arrays (e.g. vertical solar panels/towers vs flat).
- **Communication Link**: Feasibility of direct-to-Earth (DTE) radio comms given Earth's elevation above horizon.
- **Thermal & Night Survival**: Requirements for the 10-day dark period (batteries/regenerative fuel cells).

Keep the tone professional, concise (2-3 sentences per bullet), and scientifically accurate. Avoid filler.
"""

data = json.dumps({'contents': [{'parts': [{'text': explainer_prompt}]}]}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

with urllib.request.urlopen(req, context=ctx) as r:
    res = json.loads(r.read().decode('utf-8'))
    print("Explainer response:")
    print(res['candidates'][0]['content']['parts'][0]['text'])
