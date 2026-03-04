import asyncio
from playwright.async_api import async_playwright

async def dump_html():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = await context.new_page()

        print("Navigating to Microsoft...")
        await page.goto("https://jobs.careers.microsoft.com/global/en/search?q=product+manager&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true&lc=India")
        await page.wait_for_timeout(8000)
        msft_html = await page.content()
        with open("/Users/satvikjain/Downloads/PM/msft_dump.html", "w") as f:
            f.write(msft_html)

        print("Navigating to Amazon...")
        await page.goto("https://www.amazon.jobs/en/search?base_query=product+manager&loc_query=India&job_type=Full-Time&category%5B%5D=product-management")
        await page.wait_for_timeout(8000)
        amzn_html = await page.content()
        with open("/Users/satvikjain/Downloads/PM/amzn_dump.html", "w") as f:
            f.write(amzn_html)

        await browser.close()
        print("Dumps saved.")

asyncio.run(dump_html())
