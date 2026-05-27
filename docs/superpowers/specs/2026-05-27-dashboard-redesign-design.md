# oh-my-skills Dashboard Redesign Design

## Goal

Make the dashboard easier to scan when the user has hundreds of local skills. Keep the current OpenCode-inspired identity, but change the inventory experience from a long card list into a compact management console.

## Current Problems

- The dashboard renders every skill in one vertical list, which is tiring with 300+ skills.
- The left sidebar, center list, and right editor all compete for attention.
- Skill rows have similar visual weight, so names, sources, edit status, and duplicates do not stand out enough.
- Korean UI strings are currently mojibake in parts of the app, which hurts trust and readability.

## Recommended Direction

Revision after visual review: keep the original three-pane dashboard layout because it is easier to understand at a glance. Add pagination and improve typography without replacing the dashboard with a table-heavy console.

Use an "original dashboard layout, readable inventory UX" design:

- Keep the cream/ink palette, 1px borders, 4px radius, and ASCII markers.
- Use a readable system UI font stack for most interface text. Keep monospace only for the ASCII mark, inline markers, code paths, and editors.
- Keep the left sidebar, center skill list, and right-side editor placement.
- Add page size controls and pagination to the center skill list.
- Keep the right-side detail/editor panel for full `SKILL.md` inspection and editing.
- Add pagination with `10`, `30`, and `50` page-size options. Default to `30`.

## Layout

Top bar:

- Brand, language toggle, theme toggle, search, refresh, new skill, creator CTA dropdown.

Summary bar:

- `Total`, `Editable`, `Read-only`, `Duplicates`, and `Sources`.

List controls:

- Page size segmented control: `10`, `30`, `50`.
- Pagination controls: `Prev`, compact page numbers, `Next`.
- Range text: `Showing 31-60 of 369`.

Main area:

- Left: inventory metrics, source filters, editable targets, and creator CTA.
- Center: paginated skill list.
- Right: selected skill detail and editor.

Pagination footer:

- `Showing 31-60 of 369`.
- `Prev`, page numbers, `Next`.

## Skill Row Design

Each row should preserve the original card-like list style:

- Marker: `[ ]` or `[x]` for selected.
- Name: primary visual anchor.
- Source: `codex-user`, `claude-user`, `agents-user`, `plugin-cache`, etc.
- Description: truncated preview.

Rows should stay familiar, not become a table. Selected rows get a soft background and `[x]` marker.

## Mobile Behavior

On narrow screens, the table becomes a compact stacked row:

- First line: marker and name.
- Second line: source and status badges.
- Third line: one-line description.

Pagination remains visible below the list with a simplified `Prev`, current page, `Next` control.

## Data And State

Client-side state should add:

- `pageSize`, default `30`.
- `currentPage`, reset to `1` when search, source filters, duplicate filter, editable filter, or page size changes.
- `showDuplicatesOnly`.
- `showEditableOnly`.
- `sortKey`, initially `name`.

Duplicate status can be derived from `report.duplicate_names`. Editable status can be derived from `report.editable_targets` by source.

## Error Handling

- If the current page becomes invalid after filtering, clamp it to the last available page.
- If no skills match filters, show a clear empty state in the list pane.
- Existing unsaved-change confirmation remains before selecting a new skill.

## Testing

- Run existing Python tests.
- Verify `/api/state` still returns the full inventory.
- Manually test search, source filters, duplicate filter, editable filter, page-size switching, pagination, selecting a skill, saving, archiving, language toggle, theme toggle, and mobile layout.
