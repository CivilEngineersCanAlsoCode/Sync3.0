import requests
import json

# Amazon Careers API
url = "https://www.amazon.jobs/en/search.json"
params = {
    "base_query": "product manager",
    "loc_query": "India",
    "job_type": "Full-Time",
    "category[]": "product-management",
    "sort": "recent"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
}
resp = requests.get(url, params=params, headers=headers)
if resp.status_code == 200:
    data = resp.json()
    jobs = data.get("jobs", [])
    print(f"✅ Amazon: Found {data.get('hits', len(jobs))} PM jobs in India")
    for j in jobs[:5]:
        print(f"  - {j.get('title')} ({j.get('city')}, {j.get('state')}) [URL: {j.get('job_path')}]")
else:
    print(f"❌ Amazon API failed: {resp.status_code}")
    print(resp.text[:200])
