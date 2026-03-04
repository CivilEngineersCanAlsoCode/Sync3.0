import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_msft_amzn():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900}
        )
        page = await context.new_page()

        # ====================
        # Microsoft Scraping
        # ====================
        print("Scraping Microsoft India PM jobs...")
        await page.goto("https://jobs.careers.microsoft.com/global/en/search?q=product+manager&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true&lc=India")
        await page.wait_for_timeout(6000)

        # We will locate the first link containing "Product Manager" in a job list
        msft_links = await page.evaluate("""() => {
            return Array.from(document.querySelectorAll('a'))
                .filter(a => a.href.includes('/job/') && a.innerText.toLowerCase().includes('product manager'))
                .map(a => ({href: a.href, text: a.innerText.split('\\n')[0].trim()}));
        }""")

        if msft_links:
            target = msft_links[0]
            print(f"Found MSFT job: {target['text']}")
            
            # Using keyboard navigation to open it
            print("Simulating keyboard Enter to open JD...")
            # Focus the element safely without simulating a mouse click
            await page.locator(f"a[href='{target['href'].replace('https://jobs.careers.microsoft.com', '')}']").first.focus()
            await page.wait_for_timeout(500)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)

            # Extract body text
            body_text = await page.evaluate("() => document.body.innerText")
            result = [{
                "company": "Microsoft",
                "website": "https://careers.microsoft.com",
                "role": target['text'],
                "url": target['href'],
                "location": "India",
                "jd": body_text[:4000],
                "override": "false"
            }]
            with open('/Users/satvikjain/Downloads/PM/Target_Companies_Data_Microsoft.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("✅ Saved Microsoft JD")
        else:
            print("❌ Could not find MSFT job links.")


        # ====================
        # Amazon Scraping
        # ====================
        print("\nScraping Amazon India PM jobs...")
        await page.goto("https://www.amazon.jobs/en/search?base_query=product+manager&loc_query=India&job_type=Full-Time&category%5B%5D=product-management")
        await page.wait_for_timeout(6000)

        amzn_links = await page.evaluate("""() => {
            return Array.from(document.querySelectorAll('a'))
                .filter(a => a.href.includes('/jobs/') && a.innerText.toLowerCase().includes('product manager'))
                .map(a => ({href: a.href, text: a.innerText.split('\\n')[0].trim()}));
        }""")

        if amzn_links:
            target = amzn_links[0]
            print(f"Found AMZN job: {target['text']}")
            
            # Focus and hit Enter
            print("Simulating keyboard Enter to open JD...")
            await page.locator(f"a[href='{target['href'].replace('https://www.amazon.jobs', '')}']").first.focus()
            await page.wait_for_timeout(500)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)

            body_text = await page.evaluate("() => document.body.innerText")
            result = [{
                "company": "Amazon",
                "website": "https://amazon.jobs",
                "role": target['text'],
                "url": target['href'],
                "location": "India",
                "jd": body_text[:4000],
                "override": "false"
            }]
            with open('/Users/satvikjain/Downloads/PM/Target_Companies_Data_Amazon.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("✅ Saved Amazon JD")
        else:
            print("❌ Could not find AMZN job links.")

        await browser.close()

asyncio.run(scrape_msft_amzn())
