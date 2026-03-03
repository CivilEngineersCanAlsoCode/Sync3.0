# Resume Customization Process — End-to-End Plan

**Default output format: HTML + CSS** (printed to PDF via browser — no external tools needed)

> LaTeX files archived to `_archive/latex/`. See README there if switching back.

**Inputs per application:**

- `Input/Satvik-Jain-Resume.pdf` — base resume
- `Resume Brain/` — deep project detail (CGB/Qatar, Walmart GenAI, Use Case Hub)
- `Resume Best Practices 2026.docx` — ATS + formatting rules
- **Trigger:** Company Name + Role Name + Job Description text

---

## 7-Phase Process

### Phase 1 — Ingest All Inputs

1. Read `Satvik-Jain-Resume.pdf` (roles, dates, metrics, titles)
2. Read all `Resume Brain/*.md` for full project stories
3. Read `Resume Best Practices 2026.docx` for ATS + formatting rules
4. Accept: **Company Name**, **Role Name**, **Job Description (full text)**

---

### Phase 2 — Reverse-Engineer the JD

1. Extract **explicit keywords** (tools, skills, titles)
2. Identify **implicit competencies** (e.g. "cross-functional" = stakeholder mgmt)
3. Map **priority** — first paragraph = most important
4. Detect **cultural signals** (e.g. "move fast" = startup agility)
5. Produce **JD Scorecard**:

| Requirement | Importance           | Satvik Evidence Source       |
| ----------- | -------------------- | ---------------------------- |
| ...         | Must / Strong / Nice | PDF / Resume Brain / Unknown |

> Any "Must" + "Unknown" → triggers a user interview question in Phase 3.

---

### Phase 3 — Gap Analysis + User Confirmation Interview

**Never write without user confirmation. Never assume.**

#### 3a. Understanding Summaries

For each Must/Strong requirement, write:

- **Para 1:** "From Resume Brain/PDF, I found [specific instance + metric + context]"
- **Para 2:** "My interpretation is [X]. Is this accurate? Anything missing?"

> _Example: "JD says 0→1 product development. From Resume Brain (Use Case Hub), you conceptualized and owned end-to-end execution — Listen→Learn→Act framework, AI entity logic, 1500+ clients in 3 months. 'VP aligned, idea + execution was mine.' My reading: this is a strong 0→1 example. Is that accurate?"_

#### 3b. Flag Missing Evidence

"The JD mentions [X]. I found no clear example. Have you done this? Give 2–3 sentences and I'll write the bullet."

#### 3c. Collect Confirmations

Update JD Scorecard. **Do not proceed to Phase 4 until all Must/Strong confirmed.**

---

### Phase 4 — Bullet Rewriting

For each role, select 3–5 bullets matching JD Scorecard. Rewrite using:

- Strong action verb matching JD language
- **Lead with metric:** `"Reduced X by Y% by doing Z"`
- Mirror JD keywords verbatim (ATS)
- Draw from Resume Brain (richer than PDF)

**Formula:** `[Verb] + [What] + [How] → [Metric]`

> _Before: "Built Gen-AI Assistant for Walmart using unsupervised ML"_
> _After: "Generated $1.2M ARR by building GenAI-powered RCA engine for Walmart, cutting time-to-insight 85% via unsupervised ML clustering across 100K+ contact center calls"_

---

### Phase 5 — ATS Formatting Pass

- [ ] Single-column layout
- [ ] Standard `•` bullets only (no custom symbols)
- [ ] No tables or text boxes (ATS breaks on these)
- [ ] Reverse-chronological order
- [ ] Keywords in Experience bullets, not only Skills section
- [ ] Section order: Experience → Achievements → Education → Skills
- [ ] Max 2 pages (Satvik: 4 yrs experience)

---

### Phase 5.5 — HTML + CSS Build

**Output:** `Satvik_Jain_[Company]_[Role].html` + `Satvik_Jain_[Company]_[Role].css`
**To PDF:** Open in Chrome → Print → Save as PDF (no external tools needed)

**Structure:**

```
resume.html   — semantic single-column layout
resume.css    — all styling including CSS custom properties for brand colors
```

**CSS architecture:**

```css
/* Brand color zone — only these 3 lines change per company */
:root {
  --brand-primary: #1a1a2e; /* name, section headings, horizontal rules */
  --brand-secondary: #4a4a6a; /* dates, locations, role titles */
  --brand-accent: #7b2d8b; /* skill category labels */
}
```

**HTML rules (ATS print-safe):**

- Single `<div class="resume">` container, no multi-column CSS grid/flex
- `<h2>` for section headers, `<h3>` for company names
- `<ul>` with `<li>` for bullets (not `<p>` tags)
- Inline `<style>` block as fallback for email clients
- Print margins: `@media print { margin: 0.5in; }`

---

### Phase 6 — Brand Color Application

Look up company in `_archive/latex/resume_branding_cheatsheet.csv` (hex codes still valid for CSS).
Apply to the 3 CSS variables in `:root`. Visual-check in browser before printing.

**Rule:** ATS portal submissions → keep `--brand-*` as neutral grey/black. Brand colors for human/recruiter/referral only.

---

### Phase 7 — Final Output Package

**Deliverables:**

1. `Satvik_Jain_[Company]_[Role].html` + `.css` — branded (for visual/referral)
2. `Satvik_Jain_[Company]_[Role]_ATS.html` + `.css` — neutral grey (for ATS portals)
3. Both printed to `.pdf` via browser

**Final checklist:**

- [ ] No spelling errors
- [ ] All metrics confirmed in Phase 3
- [ ] JD keywords appear naturally in bullets
- [ ] Contact info current
- [ ] File: `FirstName_LastName_Company_PM.pdf`

---

## Dependency Graph

```
Phase 1: Ingest Inputs
    └── Phase 2: JD Reverse-Engineering
            └── Phase 3: Gap Analysis + User Interviews
                    └── [USER GATE ✋ — Confirm understanding]
                            ├── Phase 4: Bullet Rewriting
                            │       └── Phase 5: ATS Formatting
                            │               └── Phase 5.5: HTML + CSS Build
                            │                       └── Phase 6: Brand Colors (CSS vars)
                            │                               └── Phase 7: Final Output
                            └── [If gaps] → Loop back to Phase 3
```

---

## bd Task Structure

```
Epic: Resume Customization — [Company] [Role]
│
├── TASK-A: Ingest inputs                              [P1]
├── TASK-B: JD Reverse-Engineering + Scorecard         [P1]  → blocked by A
├── TASK-C: Draft understanding summaries              [P1]  → blocked by B
├── TASK-D: [USER GATE] Confirm understanding          [P0]  → blocked by C
├── TASK-E: Bullet rewriting                           [P1]  → blocked by D
├── TASK-F: ATS formatting pass                        [P1]  → blocked by E
├── TASK-F5: HTML + CSS build                          [P1]  → blocked by F
├── TASK-G: Brand color application (CSS vars)         [P2]  → blocked by F5
└── TASK-H: Final output package                       [P1]  → blocked by G
```

**bd CLI scaffold:**

```bash
bd create "Epic: Resume — [Company] [Role]" -t epic -p 0
bd create "TASK-A: Ingest inputs" -t task -p 1
bd create "TASK-B: JD reverse-engineering" -t task -p 1
bd create "TASK-C: Draft understanding summaries" -t task -p 1
bd create "TASK-D: USER GATE — confirm understanding" -t task -p 0
bd create "TASK-E: Bullet rewriting" -t task -p 1
bd create "TASK-F: ATS formatting pass" -t task -p 1
bd create "TASK-F5: HTML + CSS build" -t task -p 1
bd create "TASK-G: Brand colors via CSS vars" -t task -p 2
bd create "TASK-H: Final output package" -t task -p 1
# Chain: A→B→C→D→E→F→F5→G→H
```

---

## Key Rules

| Rule                                                | Why                                      |
| --------------------------------------------------- | ---------------------------------------- |
| **Never write a bullet without user confirmation**  | Prevents misrepresentation               |
| **Mirror JD language verbatim**                     | ATS keyword match                        |
| **Lead bullets with metric, not action**            | Recruiter spends 6 sec on resume         |
| **Max 3–5 bullets per role**                        | Scannability                             |
| **Use Resume Brain, not PDF**                       | Resume Brain has full project context    |
| **HTML + CSS is the default — no LaTeX, no Python** | No external tools, browser prints to PDF |
| **Brand colors for human; grey for ATS**            | ATS ignores color                        |
| **Always confirm interpretation before writing**    | Avoids distortion                        |
