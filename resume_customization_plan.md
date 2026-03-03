# Resume Customization Process — End-to-End Plan

**Inputs available:**

- `Satvik-Jain-Resume.pdf` — base resume (experience, education, skills)
- `Resume Brain/` — deep project details for CGB (Qatar), Walmart (GenAI RCA), Use Case Hub (0→1)
- `Resume Best Practices 2026.docx` — ATS rules, formatting, keyword strategies
- `Satvik_Jain_Resume.tex` — brandable LaTeX template with color placeholders
- **Trigger input** (per application): Company Name + Role Name + Job Description text

---

## 8-Phase Step-by-Step Process

---

### Phase 1 — Ingest & Understand All Inputs

**Goal:** Load all sources so every downstream step has full context.

**Steps:**

1. Read `Satvik-Jain-Resume.pdf` to extract base facts (roles, dates, metrics, titles)
2. Read all `Resume Brain/*.md` files for deep project detail on each story
3. Read `Resume Best Practices 2026.docx` for formatting + ATS rules to apply throughout
4. Accept user input: **Company Name**, **Role Name**, **Job Description (full text)**

**Output:** Structured knowledge map of:

- Satvik's experience stories (with metrics)
- Best practice rules to enforce
- JD text to analyze

---

### Phase 2 — Reverse-Engineer the Job Description

**Goal:** Extract what the company is actually looking for, beyond surface keywords.

**Steps:**

1. Parse JD for **explicit keywords** (tools, skills, titles mentioned)
2. Extract **implicit competencies** (e.g. "cross-functional" = stakeholder mgmt, "0→1" = ideation to launch)
3. Map **requirement priority** — what's in the first paragraph is most important, what's optional is last
4. Identify **cultural signals** (e.g. "move fast" = startup agility, "data-driven" = metrics culture)
5. Produce a **JD Scorecard** with 3 columns:
   - Requirement (from JD)
   - Importance (Must / Strong / Nice-to-have)
   - Satvik Evidence Source (PDF / Resume Brain / Unknown)

> **Rule:** Any requirement tagged "Must" with source "Unknown" triggers a user interview question in Phase 3.

---

### Phase 3 — Gap Analysis + User Confirmation Interview

**Goal:** Validate AI interpretation of Satvik's experience before writing anything. Never assume.

**Sub-steps:**

#### 3a. Draft Understanding Summaries

For each **Must/Strong** JD requirement, write a 2-paragraph understanding:

- **Para 1:** "From your resume/Resume Brain, here's what I found that matches this requirement: [specific instance + metric + context]"
- **Para 2:** "My interpretation is [X]. Is this accurate? Is there anything I'm missing or misrepresenting?"

**Example:**

> _JD says: "Led 0→1 product development". From Resume Brain (Use Case Hub), I found that you conceptualized, framed, and drove end-to-end execution of the Use Case Hub from scratch — including the Listen→Learn→Act framework, AI entity logic, and reporting template architecture — deployed to 1500+ clients in 3 months. You noted "VP aligned but idea + execution was mine." My interpretation: this is a strong 0→1 example where you had full ownership. Is that accurate? Was there anything else about your ownership/constraints I should know before writing this?_

#### 3b. Flag Missing Evidence

For JD requirements with **no evidence found**, ask directly:

- "The JD mentions [X]. I couldn't find a clear example of this in your resume or Resume Brain. Have you done this in any role? If yes, give me 2–3 sentences and I'll turn it into a bullet."

#### 3c. Collect Confirmations

Wait for user to respond to all questions. Update the JD Scorecard with confirmed/corrected evidence.

> ⚠️ **Do not proceed to Phase 4 until all Must/Strong requirements are confirmed by the user.**

---

### Phase 4 — Bullet Rewriting (Story Selection + Tailoring)

**Goal:** Rewrite each experience bullet to match the JD's language, priorities, and metrics.

**Steps:**

1. For each role in the resume, **select the 3–5 bullets** that best match the JD Scorecard
2. **Rewrite using Resume Best Practices 2026 rules:**
   - Start with a strong action verb aligned to JD language (e.g. JD says "scaled" → use "Scaled", not "Built")
   - Lead with impact metric, follow with method: `"Reduced X by Y% by doing Z"`
   - Mirror JD keywords verbatim where truthful (ATS optimization)
   - Remove bullets that don't match any JD requirement
3. **Add new bullets** from Resume Brain if they match Must/Strong requirements not covered by PDF resume
4. Apply **STAR light format** internally: Situation implicit, Task implicit, Action explicit, Result first

**Bullet formula:**

```
[Strong Verb] + [What] + [How/With what] → [Metric impact]
```

**Example transformation:**

- Before: _"Built Gen-AI Assistant for Walmart Spark Driver Support using unsupervised ML"_
- JD asks for: _"Scale AI solutions for enterprise clients with measurable ROI"_
- After: _"Generated $1.2M ARR opportunity by building a GenAI-powered RCA engine for Walmart's driver support ecosystem, cutting time-to-insight by 85% using unsupervised ML clustering across 100K+ contact center calls"_

---

### Phase 5 — Resume Structure & ATS Formatting

**Goal:** Apply Resume Best Practices 2026 formatting to the final content.

**Checklist (non-negotiable):**

- [ ] Single-column layout (ATS-safe — avoids multi-column parsing errors)
- [ ] File format: LaTeX → PDF for human review; export to DOCX for ATS submissions
- [ ] Fonts: FiraMono / TG Heros (already in template) — ATS-safe sans-serif
- [ ] Margins: 0.5–1 inch all sides (already in template)
- [ ] Bullet symbols: Standard `•` only (no `▶`, `◆`, custom glyphs)
- [ ] No tables, text boxes, headers/footers that contain content (ATS breaks on these)
- [ ] Reverse-chronological order (most recent role first)
- [ ] 1 page if <5 yrs experience; 2 pages is acceptable for Satvik (4 yrs)
- [ ] Resume headline: `Product Manager | AI · B2C · Design · 0→1` (customizable per company)
- [ ] Section order: Experience → Projects/Achievements → Education → Skills
- [ ] Keywords from JD appear in Experience bullets (not just Skills section)
- [ ] No generic summaries — if summary added, it must mention company name or domain directly

---

### Phase 5.5 — ✋ Format Selection Gate (USER INPUT REQUIRED)

**Goal:** Choose the output format _before any coding begins_. The choice determines the entire rendering pipeline.

**Ask the user:**

> _"Which format do you want for this resume?"_
>
> - **Option 1 — HTML + CSS** → Single `.html` + `.css` file. Export to PDF via browser print. Best visual control, easiest brand color application with CSS variables. ATS-safe only if single-column.
> - **Option 2 — .docx via Python** → Agent generates a `.py` script using `python-docx` that outputs a `.docx`. Most ATS-compatible format (Word is universally parsed by ATS systems). Minimal visual styling but maximum ATS safety.
> - **Option 3 — .tex (LaTeX)** → Uses existing `Satvik_Jain_Resume.tex` template. Agent writes the `.tex` source; user compiles via Overleaf or `pdflatex`. Best typography, supports brand `\definecolor`.

**Format tradeoff:**

|                | HTML + CSS            | .docx (Python)     | .tex (LaTeX)        |
| -------------- | --------------------- | ------------------ | ------------------- |
| ATS safe       | ⚠️ single-col only    | ✅ Best            | ✅ Good             |
| Brand colors   | ✅ CSS vars           | ❌ None            | ✅ `\definecolor`   |
| Visual quality | ✅ High               | ⚠️ Basic           | ✅ Highest          |
| Editability    | ✅ Easy               | ✅ Easy            | ⚠️ Needs LaTeX      |
| Agent output   | `.html` + `.css`      | `.py` + `.docx`    | `.tex`              |
| Compile step   | Browser → Print → PDF | `python script.py` | Overleaf / pdflatex |

> ⚠️ **Do not begin coding until user selects a format.**

---

### Phase 6 — Brand Color Customization

**Goal:** Apply company branding using the chosen format's color system.

**Option 1 (HTML + CSS):**

```css
:root {
  --brand-primary: #XXXXXX; /* name, section headings */
  --brand-secondary: #XXXXXX; /* dates, locations */
  --brand-accent: #XXXXXX; /* skill labels */
}
```

**Option 2 (.docx):** Skip colors — use neutral black/grey for ATS safety.

**Option 3 (.tex):**

```latex
\definecolor{brand-primary}{HTML}{XXXXXX}
\definecolor{brand-secondary}{HTML}{XXXXXX}
\definecolor{brand-accent}{HTML}{XXXXXX}
```

Look up hex values in `resume_branding_cheatsheet.csv`. Visual-check before export.

> **Rule:** ATS portal submissions → neutral grey/black. Brand colors only for human/recruiter/referral.

---

### Phase 7 — Final Review & Output Package

**Goal:** Produce the complete application-ready package.

**Deliverables (by format):**

- HTML: `Satvik_Jain_[Company]_[Role].html` + branded `.css` + browser-printed `.pdf`
- .docx: `Satvik_Jain_[Company]_[Role].docx` (ATS submission) + generator `.py` script
- LaTeX: `Satvik_Jain_[Company]_[Role].tex` + compiled branded `.pdf` + neutral ATS `.pdf`

**Final checklist:**

- [ ] No spelling errors
- [ ] All metrics confirmed in Phase 3
- [ ] JD keywords appear naturally in bullets
- [ ] Contact info is current
- [ ] File name: `FirstName_LastName_Company_PM.[ext]`

---

## Dependency Graph

```
Phase 1: Ingest Inputs
    └── Phase 2: JD Reverse-Engineering
            └── Phase 3: Gap Analysis + User Interviews
                    └── [USER GATE ✋ — Confirm understanding]
                            ├── Phase 4: Bullet Rewriting
                            │       └── Phase 5: ATS Formatting
                            │               └── [USER GATE ✋ — Format Selection]
                            │                       └── Phase 5.5: Pick HTML/docx/tex
                            │                               └── Phase 6: Brand Colors
                            │                                       └── Phase 7: Final Output
                            └── [If gaps found] → Loop back to Phase 3
```

---

## bd Task Structure (per job application)

```
Epic: Resume Customization — [Company] [Role]
│
├── TASK-A: Ingest inputs (PDF + Brain + JD)                [P1]
├── TASK-B: JD Reverse-Engineering + Scorecard              [P1]  blocked by: A
├── TASK-C: Draft Phase 3 understanding summaries           [P1]  blocked by: B
├── TASK-D: [USER GATE] Confirm understanding + fill gaps   [P0]  blocked by: C
├── TASK-E: Bullet rewriting (Phase 4)                      [P1]  blocked by: D
├── TASK-F: ATS formatting pass (Phase 5)                   [P1]  blocked by: E
├── TASK-F5: [USER GATE] Format selection (HTML/docx/tex)   [P0]  blocked by: F  ← NEW
├── TASK-G: Brand color + format rendering (Phase 6)        [P2]  blocked by: F5
└── TASK-H: Final output package (Phase 7)                  [P1]  blocked by: G
```

**bd CLI scaffold:**

```bash
bd create "Epic: Resume — [Company] [Role]" -t epic -p 0
bd create "TASK-A: Ingest inputs" -t task -p 1
bd create "TASK-B: JD reverse-engineering" -t task -p 1
bd create "TASK-C: Draft Phase 3 understanding summaries" -t task -p 1
bd create "TASK-D: USER GATE — confirm understanding" -t task -p 0
bd create "TASK-E: Bullet rewriting" -t task -p 1
bd create "TASK-F: ATS formatting pass" -t task -p 1
bd create "TASK-F5: USER GATE — format selection (HTML/docx/tex)" -t task -p 0
bd create "TASK-G: Brand color + format rendering" -t task -p 2
bd create "TASK-H: Final output package" -t task -p 1
# Chain: A→B→C→D→E→F→F5→G→H
```

---

## Key Rules (Non-Negotiable)

| Rule                                                   | Why                                             |
| ------------------------------------------------------ | ----------------------------------------------- |
| **Never write a bullet without user confirmation**     | Prevents misrepresentation                      |
| **Mirror JD language verbatim in bullets**             | ATS keyword match                               |
| **Lead bullets with metric impact, not action**        | Recruiter spends 6 sec on resume                |
| **Max 3–5 bullets per role**                           | Scannability; quality > quantity                |
| **Use Resume Brain as detail source, not PDF**         | PDF is compressed; Brain has full story         |
| **Ask format before any coding begins**                | HTML/docx/tex require completely different code |
| **Brand colors only for human/referral; grey for ATS** | ATS doesn't care about color                    |
| **Always confirm interpretation before writing**       | Avoids tone/context distortion                  |

**Goal:** Apply company-specific branding to the LaTeX resume to signal brand alignment visually.

**Steps:**

1. Look up company in `resume_branding_cheatsheet.csv`
2. If not listed, extract primary hex color from company's official website or brand guidelines
3. Replace 3 `\definecolor` lines at top of `Satvik_Jain_Resume.tex`:
   ```latex
   \definecolor{brand-primary}{HTML}{XXXXXX}    % Section headings, name, rules
   \definecolor{brand-secondary}{HTML}{XXXXXX}  % Dates, locations
   \definecolor{brand-accent}{HTML}{XXXXXX}     % Skill labels
   ```
4. Compile: `pdflatex Satvik_Jain_Resume.tex`
5. Visual check: Ensure colors are readable, not too bright/light, print-safe

> **Rule:** For ATS submissions → submit PDF with neutral grey colors. For human/recruiter submissions (email, referral, portfolio) → use brand colors.

---

### Phase 7 — Final Review & Output Package

**Goal:** Produce the complete application-ready package.

**Deliverables:**

1. `Satvik_Jain_[Company]_[Role].tex` — branded LaTeX source
2. `Satvik_Jain_[Company]_[Role].pdf` — branded PDF (for human/referral submission)
3. `Satvik_Jain_[Company]_[Role]_ATS.pdf` — neutral grey PDF (for ATS portals)
4. **Cover letter outline** (optional, generated from confirmed Phase 3 understanding)

**Final checklist before sending:**

- [ ] No spelling errors or grammar issues
- [ ] All metrics are accurate and confirmed in Phase 3
- [ ] JD keywords appear naturally in bullets (not stuffed)
- [ ] Contact info is current
- [ ] File names are professional: `FirstName_LastName_Company_PM.pdf`

---

## Dependency Graph

```
Phase 1: Ingest Inputs
    └── Phase 2: JD Reverse-Engineering
            └── Phase 3: Gap Analysis + User Interviews
                    └── [USER CONFIRMATION GATE ✋]
                            ├── Phase 4: Bullet Rewriting
                            │       └── Phase 5: ATS Formatting
                            │               └── Phase 6: Brand Colors
                            │                       └── Phase 7: Final Output Package
                            └── [If gaps found] → Loop back to Phase 3
```

---

## bd Task Structure (per job application)

```
Epic: Resume Customization — [Company] [Role]
│
├── TASK-A: Ingest inputs (PDF + Brain + JD)                [P1]
│       └── Blockers: none
│
├── TASK-B: JD Reverse-Engineering + Scorecard              [P1]
│       └── Blockers: TASK-A
│
├── TASK-C: Draft Phase 3 understanding summaries           [P1]
│       └── Blockers: TASK-B
│
├── TASK-D: [USER GATE] Confirm understanding + fill gaps   [P0]
│       └── Blockers: TASK-C
│       └── Type: human-review
│
├── TASK-E: Bullet rewriting (Phase 4)                      [P1]
│       └── Blockers: TASK-D
│
├── TASK-F: ATS formatting pass (Phase 5)                   [P1]
│       └── Blockers: TASK-E
│
├── TASK-G: Brand color customization (Phase 6)             [P2]
│       └── Blockers: TASK-F (parallel ok with F)
│
└── TASK-H: Final output package + review (Phase 7)         [P1]
        └── Blockers: TASK-E, TASK-F, TASK-G
```

**bd CLI commands to scaffold per application:**

```bash
bd create "Epic: Resume — [Company] [Role]" -t epic -p 0
bd create "TASK-A: Ingest inputs" -t task -p 1
bd create "TASK-B: JD reverse-engineering" -t task -p 1
bd create "TASK-C: Draft Phase 3 understanding summaries" -t task -p 1
bd create "TASK-D: USER GATE — confirm understanding" -t task -p 0
bd create "TASK-E: Bullet rewriting" -t task -p 1
bd create "TASK-F: ATS formatting pass" -t task -p 1
bd create "TASK-G: Brand color customization" -t task -p 2
bd create "TASK-H: Final output package" -t task -p 1
# Then add deps: bd dep add TASK-B TASK-A, etc.
```

---

## Key Rules (Non-Negotiable)

| Rule                                                            | Why                                                   |
| --------------------------------------------------------------- | ----------------------------------------------------- |
| **Never write a bullet without user confirmation of the facts** | Prevents misrepresentation                            |
| **Mirror JD language verbatim in bullets**                      | ATS keyword match                                     |
| **Lead bullets with metric impact, not action**                 | Recruiter spends 6 sec on resume — metric catches eye |
| **Max 3–5 bullets per role**                                    | Scannability; quality over quantity                   |
| **Use Resume Brain as the detail source, not the PDF**          | PDF is compressed; Brain has full story               |
| **Brand colors only for human/referral; grey for ATS**          | ATS doesn't care about color; human does              |
| **Always confirm interpretation before writing**                | Avoids tone/context distortion                        |
