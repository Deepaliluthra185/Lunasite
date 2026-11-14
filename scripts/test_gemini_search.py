import urllib.request, json, ssl, os, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

key = os.environ.get("GEMINI_API_KEY") or base64.b64decode(b"QVEuQWI4Uk42TDRBTzNjQkRLblJMaFZMdGhjQm5PN0NqUlJXcFB3bXg0VTNYSUpKWHJ3T0E=").decode()
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}'

# Test 1: Natural Language Search Prompt
search_prompt = """You are the AI mission navigator for LunaSite, a lunar landing site explorer.
Given a user's natural language search query, identify the most suitable lunar landing site.

Available Preset Sites:
- Apollo 11 (Lat: 0.67, Lon: 23.47)
- Apollo 15 (Lat: 26.13, Lon: 3.63)
- Apollo 17 (Lat: 20.19, Lon: 30.77)
- Chandrayaan-3 (Lat: -69.37, Lon: 32.32)
- Luna 25 target (Lat: -57.86, Lon: 61.36)
- IM-2 (Mons Mouton) (Lat: -84.8, Lon: 29.2)
- Blue Ghost (Mare Crisium) (Lat: 18.6, Lon: 61.8)
- Malapert massif (Lat: -85.9, Lon: 0.0)
- Shackleton rim (Lat: -89.9, Lon: 0.0)

If the query describes custom coordinates or criteria (e.g. "South pole 88S", "near Shackleton"), output the best coordinates.

Respond ONLY with valid JSON in this exact structure:
{
  "site_name": "Name of site or Custom Target",
  "lat": 0.0,
  "lon": 0.0,
  "reason": "Short 1-2 sentence explanation of why this matches the request."
}

User Query: "I need a landing spot near the south pole with direct line of sight to Earth for Artemis"
"""

data = json.dumps({'contents': [{'parts': [{'text': search_prompt}]}]}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

with urllib.request.urlopen(req, context=ctx) as r:
    res = json.loads(r.read().decode('utf-8'))
    print("Search query response:")
    print(res['candidates'][0]['content']['parts'][0]['text'])
