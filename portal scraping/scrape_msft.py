import requests

# Microsoft Careers API
url = "https://gcsservices.careers.microsoft.com/search/api/v1/search"
params = {
    "q": "product manager",
    "lc": "India",
    "l": "en_us",
    "pg": "1",
    "pgSz": "20",
    "o": "Relevance",
    "flt": "true"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}
resp = requests.get(url, params=params, headers=headers)
if resp.status_code == 200:
    data = resp.json()
    jobs = data.get("operationResult", {}).get("result", {}).get("jobs", [])
    print(f"✅ Microsoft: Found {len(jobs)} PM jobs in India")
    for j in jobs[:5]:
        loc = j.get('properties',{}).get('primaryLocation', 'Unknown')
        print(f"  - {j.get('title')} ({loc}) [ID: {j.get('jobId')}]")
else:
    print(f"❌ Microsoft API failed: {resp.status_code}")
    print(resp.text[:200])
