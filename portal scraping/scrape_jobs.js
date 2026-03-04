const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrape() {
    console.log("Launching browser...");
    const browser = await puppeteer.launch({ 
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    await page.setViewport({ width: 1440, height: 900 });

    try {
        console.log("Navigating to Microsoft Careers India PM jobs...");
        await page.goto("https://jobs.careers.microsoft.com/global/en/search?q=product+manager&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true&lc=India", { waitUntil: 'networkidle2' });
        await page.waitForTimeout(4000);

        // Extract job links without clicking, just to find where they are
        const jobs = await page.evaluate(() => {
            const links = Array.from(document.querySelectorAll('a'));
            return links
                .filter(a => a.innerText.toLowerCase().includes('product manager'))
                .map(a => ({ text: a.innerText, href: a.href }))
                .filter(a => a.href.includes('/job/'));
        });

        console.log(`Found ${jobs.length} potential PM links on Microsoft.`);
        
        if (jobs.length > 0) {
            console.log(`Targeting top job: ${jobs[0].text}`);
            // Navigate directly to the JD page to be safe, simulating a right-click open in new tab
            const jdPage = await browser.newPage();
            await jdPage.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
            console.log(`Loading JD URL: ${jobs[0].href}`);
            await jdPage.goto(jobs[0].href, { waitUntil: 'networkidle2' });
            await jdPage.waitForTimeout(3000);
            
            // Extract all text from body
            const bodyText = await jdPage.evaluate(() => document.body.innerText);
            
            const result = [{
                company: "Microsoft",
                website: "https://careers.microsoft.com",
                role: jobs[0].text.split('\n')[0].trim() || "Product Manager",
                url: jobs[0].href,
                location: "India",
                jd: bodyText.substring(0, 4000), // grab first 4k chars
                override: "false"
            }];
            
            fs.writeFileSync('/Users/satvikjain/Downloads/PM/Target_Companies_Data_Microsoft.json', JSON.stringify(result, null, 2));
            console.log(`✅ Saved Microsoft JD to Target_Companies_Data_Microsoft.json`);
            await jdPage.close();
        }

        console.log("\nNavigating to Amazon Jobs India PM...");
        await page.goto("https://www.amazon.jobs/en/search?base_query=product+manager&loc_query=India&job_type=Full-Time&category%5B%5D=product-management", { waitUntil: 'networkidle2' });
        await page.waitForTimeout(4000);

        const amznJobs = await page.evaluate(() => {
            const currentJobs = [];
            document.querySelectorAll('.job-tile').forEach(tile => {
                const link = tile.querySelector('a.job-link');
                const loc = tile.querySelector('.location-and-id');
                if(link) {
                    currentJobs.push({
                        title: link.innerText,
                        href: link.href,
                        location: loc ? loc.innerText : 'India'
                    });
                }
            });
            return currentJobs;
        });

        console.log(`Found ${amznJobs.length} PM jobs on Amazon.`);
        if(amznJobs.length > 0) {
            console.log(`Targeting top job: ${amznJobs[0].title}`);
            const jdPage = await browser.newPage();
            await jdPage.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
            await jdPage.goto(amznJobs[0].href, { waitUntil: 'networkidle2' });
            await jdPage.waitForTimeout(3000);

            const bodyText = await jdPage.evaluate(() => document.body.innerText);
            const result = [{
                company: "Amazon",
                website: "https://amazon.jobs",
                role: amznJobs[0].title.trim(),
                url: amznJobs[0].href,
                location: amznJobs[0].location.trim(),
                jd: bodyText.substring(0, 4000),
                override: "false"
            }];
            
            fs.writeFileSync('/Users/satvikjain/Downloads/PM/Target_Companies_Data_Amazon.json', JSON.stringify(result, null, 2));
            console.log(`✅ Saved Amazon JD to Target_Companies_Data_Amazon.json`);
            await jdPage.close();
        }

    } catch (e) {
        console.error("Error during scraping:", e);
    } finally {
        await browser.close();
    }
}

scrape();
