import urllib.request, json, ssl, os, base64

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

key = os.environ.get("GEMINI_API_KEY") or base64.b64decode(b"QVEuQWI4Uk42TDRBTzNjQkRLblJMaFZMdGhjQm5PN0NqUlJXcFB3bXg0VTNYSUpKWHJ3T0E=").decode()
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}'

comparison_prompt = """You are the AI Mission Analyst for LunaSite.
Provide a concise side-by-side trade study comparison between the following candidates:

Candidate 1: Malapert massif (-85.90° S, 0.00° E)
- Score: 67/100 (GO)
- Sunlight this cycle: 62% (Peak: 5.6°)
- Earth link this cycle: 71% (Both active: 60%)

Candidate 2: Shackleton rim (-89.90° S, 0.00° E)
- Score: 78/100 (GO)
- Sunlight this cycle: 86% (Peak: 2.1°)
- Earth link this cycle: 55% (Both active: 50%)

Provide:
1. **Core Trade-off**: Direct comparison of power vs communications.
2. **Operational Recommendation**: Which site to choose based on mission priorities (e.g., maximum power vs continuous DTE telemetry).
Keep it under 150 words.
"""

data = json.dumps({'contents': [{'parts': [{'text': comparison_prompt}]}]}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

with urllib.request.urlopen(req, context=ctx) as r:
    res = json.loads(r.read().decode('utf-8'))
    print("Comparison response:")
    print(res['candidates'][0]['content']['parts'][0]['text'])
