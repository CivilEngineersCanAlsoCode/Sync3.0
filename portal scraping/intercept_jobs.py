import asyncio
from playwright.async_api import async_playwright
import json

async def intercept_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = await context.new_page()

        msft_jobs = []
        amzn_jobs = []

        async def handle_response(response):
            nonlocal msft_jobs, amzn_jobs
            url = response.url
            if "gcsservices.careers.microsoft.com/search/api/v1/search" in url:
                try:
                    data = await response.json()
                    jobs = data.get("operationResult", {}).get("result", {}).get("jobs", [])
                    print(f"✅ Microsoft API intercepted: Found {len(jobs)} jobs")
                    msft_jobs = jobs
                except Exception as e:
                    print("MSFT JSON err:", e)
            elif "amazon.jobs/en/search.json" in url or "amazon.jobs/en/search" in url and "json" in response.headers.get("content-type", ""):
                try:
                    data = await response.json()
                    if "jobs" in data:
                        print(f"✅ Amazon API intercepted: Found {len(data['jobs'])} jobs")
                        amzn_jobs = data["jobs"]
                except Exception as e:
                    pass

        page.on("response", handle_response)

        print("Navigating to Microsoft...")
        await page.goto("https://jobs.careers.microsoft.com/global/en/search?q=product+manager&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true&lc=India")
        await page.wait_for_timeout(8000)

        print("\nNavigating to Amazon...")
        await page.goto("https://www.amazon.jobs/en/search?base_query=product+manager&loc_query=India&job_type=Full-Time&category%5B%5D=product-management")
        await page.wait_for_timeout(8000)

        # Process and save the grabbed jobs
        if msft_jobs:
            msft_formatted = []
            for j in msft_jobs[:5]:
                msft_formatted.append({
                    "company": "Microsoft",
                    "website": "https://careers.microsoft.com",
                    "role": j.get('title'),
                    "url": f"https://jobs.careers.microsoft.com/global/en/job/{j.get('jobId')}",
                    "location": "India",
                    "jd": j.get('description', '')[:4000],
                    "override": "false"
                })
            with open('/Users/satvikjain/Downloads/PM/Target_Companies_Data_Microsoft.json', 'w') as f:
                json.dump(msft_formatted, f, indent=2)
            print("💾 Saved MSFT Jobs to file.")

        if amzn_jobs:
            amzn_formatted = []
            for j in amzn_jobs[:5]:
                amzn_formatted.append({
                    "company": "Amazon",
                    "website": "https://www.amazon.jobs",
                    "role": j.get('title'),
                    "url": "https://www.amazon.jobs" + j.get('job_path', ''),
                    "location": j.get('city', 'India'),
                    "jd": j.get('description', '')[:4000] + "\n" + j.get('basic_qualifications', '') + "\n" + j.get('preferred_qualifications', ''),
                    "override": "false"
                })
            with open('/Users/satvikjain/Downloads/PM/Target_Companies_Data_Amazon.json', 'w') as f:
                json.dump(amzn_formatted, f, indent=2)
            print("💾 Saved AMZN Jobs to file.")

        await browser.close()

asyncio.run(intercept_jobs())
