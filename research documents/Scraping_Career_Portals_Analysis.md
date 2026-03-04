# Research Analysis: Scraping Job Portals (Strict No-Ban Constraints)

**Goal:** Extract PM job descriptions from Top 10 Tier companies (Google, Microsoft, Amazon, Meta, etc.) relying only on safe, invisible, or strictly keyboard-navigated automation to completely avoid IP bans.

---

## 1. Direct HTTP Parsing (`read_url_content` / cURL)

- **Approach:** Sending standard HTTP GET requests to the career search URLs without any JavaScript rendering or browser automation.
- **Result:** **Massive Success for Google.** Failed for others.
- **Analysis:** Google builds their career page with incredible SEO and accessibility in mind. They embed the actual job data directly into the raw HTML. Zero ban risk, executes in milliseconds. However, Microsoft, Amazon, Meta, Adobe, and Salesforce send back empty HTML "shells" and require heavy client-side JavaScript to load the jobs.

## 2. Browser Automation with Keyboard-Only Constraints (Playwright / Puppeteer)

- **Approach:** Launched headless Chromium. Forbade mouse clicks and forced the use of only `Tab` and `Shift+Tab` to simulate an accessibility tester or visually impaired user.
- **Result:** **Failed (Keyboard Traps).**
- **Analysis:** Blind tabbing is incredibly brittle on modern web apps. The `Tab` sequence gets infinitely stuck inside invisible accessibility helper navigation bars, Shadow DOM elements, or mandatory cookie-consent modals that trap focus.

## 3. DOM Target Focus + Keyboard Enter

- **Approach:** Refined the browser script to search the DOM for the exact `href` of the job, jump the keyboard focus directly to that element using `.focus()`, and then press `Enter`.
- **Result:** **Failed (JS Routing Events).**
- **Analysis:** Amazon and Microsoft use complex Single Page Application (SPA) routers (like React/Angular). Pressing `Enter` on an `<a>` tag often doesn't trigger the page transition because they explicitly listen for `onClick` mouse events, instead of native keyboard `Enter` events on those custom elements.

## 4. Direct Backend API Querying (Python Requests)

- **Approach:** Bypassed the UI entirely. Inspected the network traffic to find the hidden backend JSON APIs that the frontends use, and wrote Python scripts to hit them directly.
- **Result:** **Failed (Anti-Bot Defenses).**
- **Analysis:**
  - **Microsoft:** Returned a `502 Bad Gateway` error, which happens when their web-application firewall (WAF) detects a request missing proper session cookies or browser fingerprints.
  - **Amazon:** Returned `200 OK` but gave an empty `jobs: []` array. This is a classic "shadowban" response where the server pretends the request worked but gives no data because there is no valid human session.

## 5. Network Traffic Interception (Playwright Sniffing)

- **Approach:** Wrote a sophisticated script that opened the browser, let it act like a normal user to pass browser fingerprinting, and silently "sniffed" the network traffic (`page.on('response')`) to intercept the raw JSON data the page requested for itself.
- **Result:** **Failed (Advanced Bot Detection).**
- **Analysis:** Even though the Amazon API response was captured, it still returned `0` jobs. Akamai/AWS WAF detected that the Chromium instance was running in `headless=True` mode (headless browsers expose certain fingerprint flags, e.g., missing plugins, specific WebGL signatures) and quietly dropped the payload.

---

## Conclusion & Recommendations

If the primary goal is **absolute safety from bans**:

1.  **Google is a goldmine.** They don't hide their jobs behind SPAs or anti-bot walls. Basic HTML scraping works flawlessly.
2.  **"Keyboard-only" via headless automation is conceptually safe but practically broken** on enterprise career sites due to cookie modals, shadow DOMs, and custom JS event listeners that ignore native `Enter` keys.
3.  **Headless browsers are heavily fingerprinted.** The moment a headless browser connects to `amazon.jobs`, they know it is a bot and serve empty data.

**Future Architecture Recommendation:**
Rather than fighting custom career portals, the most robust approach is to either:

1.  **Use a job-board aggregator API** (like scraping Wellfound/Cutshort).
2.  **Use Search Engine APIs** (Google Custom Search targeting `site:careers.microsoft.com`).
3.  **Run with full headful browsers natively** using stealth plugins if direct portal scraping is an absolute requirement.
