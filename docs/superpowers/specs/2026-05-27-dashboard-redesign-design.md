# oh-my-skills Dashboard Redesign Design

## Goal

Make the dashboard easier to scan when the user has hundreds of local skills. Keep the current OpenCode-inspired identity, but change the inventory experience from a long card list into a compact management console.

## Current Problems

- The dashboard renders every skill in one vertical list, which is tiring with 300+ skills.
- The left sidebar, center list, and right editor all compete for attention.
- Skill rows have similar visual weight, so names, sources, edit status, and duplicates do not stand out enough.
- Korean UI strings are currently mojibake in parts of the app, which hurts trust and readability.

## Recommended Direction

Use an "OpenCode skin, GitHub Issues UX" design:

- Keep the cream/ink palette, monospaced type, 1px borders, 4px radius, and ASCII markers.
- Move high-frequency controls to the top of the list: search, source filter chips, duplicate/editable filters, sort, and page size.
- Replace the card-like skill list with a compact table/list hybrid.
- Keep the right-side detail/editor panel for full `SKILL.md` inspection and editing.
- Add pagination with `10`, `30`, and `50` page-size options. Default to `30`.

## Layout

Top bar:

- Brand, language toggle, theme toggle, search, refresh, new skill, creator CTA dropdown.

Summary bar:

- `Total`, `Editable`, `Read-only`, `Duplicates`, and `Sources`.

Filter bar:

- Source chips: `All`, `Codex`, `Claude`, `Agents`, `Plugin`.
- Utility chips: `Duplicates`, `Editable only`.
- Sort selector: initially `Name`.
- Page size segmented control: `10`, `30`, `50`.

Main area:

- Left: paginated skill inventory table/list.
- Right: selected skill detail and editor.

Pagination footer:

- `Showing 31-60 of 369`.
- `Prev`, page numbers, `Next`.

## Skill Row Design

Each row should be one or two lines:

- Marker: `[ ]` or `[x]` for selected.
- Name: primary visual anchor.
- Source: `codex-user`, `claude-user`, `agents-user`, `plugin-cache`, etc.
- Status badges: `[edit]`, `[ro]`, `[dup]`.
- Description: one-line truncated preview.

Rows should be dense enough for scanning but still readable. Selected rows get a soft background and `[x]` marker.

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

