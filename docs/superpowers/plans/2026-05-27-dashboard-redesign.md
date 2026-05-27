# Dashboard Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the oh-my-skills dashboard into a clearer paginated inventory console for 300+ local skills.

**Architecture:** Keep the existing Python API unchanged and implement the redesign client-side in the static web app. Add pagination, filtering, status derivation, and denser table/list rendering in `app.js`, then update `index.html` and `styles.css` to support the new summary, filters, and responsive layout.

**Tech Stack:** Python standard-library HTTP server, vanilla HTML/CSS/JavaScript, existing pytest suite, local browser verification.

---

### Task 1: Reshape Dashboard Markup

**Files:**
- Modify: `skill_ledger/web/index.html`

- [ ] **Step 1: Replace the left-heavy inventory layout with top summary and filters**

Update the main workspace structure so the list pane owns summary, filters, list, and pagination, while the detail pane stays on the right.

- [ ] **Step 2: Add controls needed by JavaScript**

Add elements with stable IDs for summary metrics, source chips, duplicate/editable toggles, sort select, page-size buttons, pagination range, and page buttons.

- [ ] **Step 3: Keep existing editor and new-skill dialog IDs stable**

Do not rename `skillEditor`, `saveButton`, `archiveButton`, `newDialog`, or creation form inputs because existing API actions depend on those selectors.

### Task 2: Implement Pagination And Derived Status

**Files:**
- Modify: `skill_ledger/web/app.js`

- [ ] **Step 1: Add list state**

Add `pageSize`, `currentPage`, `showDuplicatesOnly`, `showEditableOnly`, and `sortKey` to the existing state object.

- [ ] **Step 2: Add helper functions**

Implement helpers for duplicate detection, editability detection, page clamping, visible range calculation, source labels, and filtered/sorted skill retrieval.

- [ ] **Step 3: Render only the current page**

Change `renderList()` to render a paginated slice instead of all filtered skills.

- [ ] **Step 4: Add pagination controls**

Render previous/next buttons, compact page numbers, and `Showing X-Y of Z` text. Reset to page 1 whenever filters/search/page size change.

### Task 3: Fix Korean Strings And CTA Text

**Files:**
- Modify: `skill_ledger/web/index.html`
- Modify: `skill_ledger/web/app.js`

- [ ] **Step 1: Replace mojibake literals**

Replace garbled Korean strings with readable Korean labels.

- [ ] **Step 2: Normalize CTA fallback**

Keep `제작자 구독하기` as the localized CTA label and render channel links as a dropdown plus optional side/footer links only if useful.

### Task 4: Redesign Styling

**Files:**
- Modify: `skill_ledger/web/styles.css`

- [ ] **Step 1: Preserve theme tokens**

Keep cream/ink colors, monospace stack, ASCII markers, 1px hairlines, and 4px interactive radius.

- [ ] **Step 2: Add console-style inventory styling**

Style summary metrics, filter chips, compact table/list rows, status badges, pagination footer, and selected-row state.

- [ ] **Step 3: Improve responsive behavior**

On narrower screens, stack controls and convert rows into compact card-like rows without horizontal overflow.

### Task 5: Verify Behavior

**Files:**
- Test existing pytest suite
- Manually verify local GUI

- [ ] **Step 1: Run automated tests**

Run `python -m pytest`.

- [ ] **Step 2: Verify API and server**

Run the GUI server and verify `/api/state` returns the full skill count.

- [ ] **Step 3: Manual UI check**

Check search, source chips, duplicate filter, editable filter, page-size switching, pagination, selecting a skill, theme toggle, language toggle, and mobile width.

