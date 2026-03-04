# Sync Platform Improvements & Post-Mortem V2

This document captures a comprehensive adverse review of the Sync Resume Customization pipeline, detailing both architectural flaws and execution failures encountered during the latest run. The focus is strictly on why existing systems broke down and how they must be redesigned for the next iteration.

---

## 1. The Rectangular Block Failure & A4 Dimension Rigidity

The current system failed to achieve a perfect "Rectangular Block" fit on a standard A4 page (210mm x 297mm). The approach of aggressively computing bullet length (`BULLET_CHAR_LIMIT`) or blindly injecting `font-size: 7pt` CSS strings proved extremely brittle. The difference between a browser's infinity-scroll height and a rigorous PDF Print Preview boundary was fundamentally misunderstood by the system engine.

### Improvement Steps (Release 2 Strategy)

- **The "5% Stretch Strategy" (⭐ BEST APPROACH):** Abandon rigid character limits. Target bullets to hit ~95% of the line and use `text-align-last: justify` with `white-space: nowrap` to mathematically stretch the last word to the margin. Use `&nbsp;` around metrics for visual micro-padding.
  - _Reason:_ Most physically robust way to guarantee the "Rectangular Block" across different rendering engines without the fragility of character counting.
- **Alternative Approaches considered:**
  1. _Fluid Typography:_ Using CSS `clamp()` to scale font size dynamically. (Rejected: Too inconsistent across OS).
  2. _Refined Char Budgets:_ Stricter V1-style counting. (Rejected: Brittle and fails on proportional fonts).
- **Embrace the Container Query:** The HTML resume MUST be constrained to a hard 8.5in or 210mm width natively in CSS, ensuring the 5% stretch logic is relative to the A4 boundary.
- **Failures in Automated Validation:** Pivot away from external `puppeteer` dependencies to internal **HTML-native validation hooks** that check for overflow during the generation loop.

## 2. Context Loss in Vector DB Chunking (ChromaDB)

The resume generation pipeline currently hallucinates or loses project context because the initial signal ingestion is flawed. When chunking text for the vector database, the context of _which_ project the signal belongs to (e.g., Walmart Spark, Qatari PM, Amex Risk) was disconnected from the granular trait (e.g., "Product Vision" or "Cross-functional Leadership").

### Improvement Steps (Release 2 Strategy)

- **Hierarchical Self-Contained Chunks (⭐ BEST APPROACH):** Ingest every signal as a Q&A pair that explicitly includes the context in the text: _"What did you do at Amex for AML Scoring? I [Action]..."_.
  - _Reason:_ Eliminates dependencies on fragile metadata retrieval and ensures the LLM always knows the "Home Project" of a bullet.
- **Alternative Approaches considered:**
  1. _Metadata Filtering:_ Relying on ChromaDB metadata tags. (Rejected: LLMs often ignore metadata).
  2. _Context Windowing:_ Pulling adjacent chunks during retrieval. (Rejected: High token cost and noise).
- **Hierarchical Metadata Tagging:** Every chunk embedded into ChromaDB MUST contain explicitly hardcoded metadata tags of its parent context for secondary filtering.

## 3. Persistent Memory vs. Docker Overhead

In an attempt to spin up ChromaDB, the system incorrectly defaulted to spinning up Docker containers and volumes rather than utilizing localized, persistent storage. This introduced unnecessary dependencies, network overhead, and complexity for a local terminal application.

### Improvement Steps (Release 2 Strategy)

- **Strictly Local Persistent Storage (⭐ BEST APPROACH):** Initialize the ChromaDB client with `chromadb.PersistentClient(path="./.chroma_db")`.
  - _Reason:_ Drastic reduction in complexity. Zero Docker overhead, zero network latency, and zero "container not started" failures.
- **Alternative Approaches considered:**
  1. _S3/Cloud Store:_ (Rejected: Overkill for local CLI).
  2. _Docker Volume persistence:_ (Rejected: Brittle and hard to manage across user environments).

## 4. Logical Bullet Point Distribution

The current automation blindly enforces a flat number of bullet points per role, which violates standard resume reading psychology and unnecessarily bloats page height. The primary/current role was treated with the same depth as a voluntary role from earlier in the career.

### Improvement Steps (Release 2 Strategy)

- **Match-Score Semantic LLM Audit (⭐ BEST APPROACH):** Replace substring matching with a secondary Claude pass to evaluate "Signal-to-JD" quality.
  - _Reason:_ Correctly handles synonyms (e.g., "GenAI" vs "LLMs") and rewards depth of experience rather than just keyword presence.
- **Temporal Weighting Algorithm:** Program the engine with an optimal upper limit (9-10 bullets total) distributed via exponential decay (Recent = 5, Previous = 3, Older = 1-2).
- **Alternative Approaches considered:**
  1. _Regex Matcher:_ (Rejected: Still too dumb for complex PM skills).
  2. _Vector Distance Score:_ (Rejected: Lacks nuance for seniority).

## 5. GitHub Pages Deployment & Branch Isolation Failures

The system attempted to push the active working directory directly to GitHub to host the resumes via GitHub Pages. The URLs generated did not resolve correctly, resulting in broken live links.

### Improvement Steps (Release 2 Strategy)

- **Branch Isolation & Action Automation (⭐ BEST APPROACH):** compiled HTML resumes must be strictly isolated into a `gh-pages` branch.
  - _Reason:_ Prevents clutter in `main` and ensures that the GitHub Pages site architecture remains clean and decoupled from the source code.
- **GitHub Actions Integration:** Use a dedicated YAML workflow to push only the `Sync/` directory to the `gh-pages` branch on every commit to `main`.

## 6. "Dumb" String Matching for Match Scores

The plan explicitly touted an "AI-powered signal engineering" platform, but the Match Score calculation (Phase 10) was executed using a rudimentary Python script doing basic substring matching (`kw.lower() in html`).

- **Improvement:** Introduce Semantic LLM matching. If the JD asks for "Generative AI" and the resume says "Gen-AI", it should correctly identify the match. The rigid substring check forced unnatural "keyword weaving" at the end of the pipeline.

## 7. Task Management (`bd` CLI) Desynchronization

The core directive insists on using the `bd` (Beads) CLI for all state synchronization.

### Improvement Steps (Release 2 Strategy)

- **Strict `bd` Mapping (⭐ BEST APPROACH):** Automation loops must fetch valid `bd` issue IDs from the current context before attempting updates.
  - _Reason:_ Prevents "Agentic Amnesia" and keeps the local state synchronized with the remote git-backed memory.
- **Sync at Session End:** Mandatory `bd sync` after every batch run to flush the debounce buffer to Git.

## 8. The "Dual-Tier" Scraper Pivot

The Epic 4 data acquisition plan pivoted heavily to a manual "Passive Capture" mode because the automated headless/headful scraping of complex UI portals (like Microsoft's Eightfold) failed due to obfuscation and dynamic rendering.

- **Improvement:** The extraction engine must be rebuilt natively into browser extensions or deeply integrated with DevTools (Network tab monitoring) rather than relying on brittle DOM-traversal scripts that instantly fail upon interface updates.

## 9. Inconsistent Confidence Gates

The architecture requires a strict `≥ 90%` Confidence Gate _before_ generating the HTML.

- **Improvement:** In execution, the engine eagerly skipped straight to generating the HTML drafts and compiling the templates before explicitly resolving the gap queues with the user. The pipeline must insert hard programmatic breakpoints that require human validation input before allowing the generation chain to proceed.
