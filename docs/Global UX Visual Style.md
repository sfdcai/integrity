4. Global UX & Visual Style

Theme: Dark, with deep navy/charcoal background and neon-style accents (green, cyan, amber).

Components: Card-based layout, soft shadows, rounded corners.

Typography: System fonts with clear hierarchy (headlines, labels, values).

Feedback: Inline validation, toasts for saves/errors, skeleton loaders.

5. Pages & UX Flows
5.1 Login Page

Simple centered card.

Fields: email, password.

Button: "Sign in".

Error message on invalid credentials.

On success, redirect to Dashboard.

5.2 Dashboard Page

Primary KPIs:

Top strip:

Total wells.

Wells by status (green/amber/red).

Wells with SAP.

Open critical tasks.

Risk Matrix Widget:

5×5 grid with coloured cells showing count of wells in each risk category.

Well Portfolio Table:

Columns: Well name, Field, Status, Highest risk, Last integrity update, Open tasks.

Traffic-light icons.

Task Panel:

Right column with list of most urgent tasks.

5.3 Wells Page (List View)

Search + Filters (status, field, type).

Table of wells with quick health indicators.

Click row → open Well Detail page.

5.4 Well Detail Page

This is the key view. Layout:

Sticky header with:

Well name.

Status pill (colored).

Field / type / MD / TVD.

Buttons: "Edit Well", "Export Report".

Tabs:

Overview

Schematic

Barriers

Measurements

Tasks

5.4.1 Overview Tab

Annulus summary cards in a grid:

For each annulus A/B/C/D:

Name ("A-Annulus")

Pressure vs MAASP

Utilisation bar (animated)

Status label (green/amber/red)

Mini sparkline chart of last N days.

Barrier status snippet:

Two horizontal bars: Primary / Secondary envelope.

Each shows count of OK, degraded, failed elements.

Integrity snapshot card:

Overall status, risk category, last updated, SAP yes/no.

5.4.2 Schematic Tab

The WellSchematicCanvas renders a vertical SVG schematic:

Left: depth scale (0 m to TD).

Centre: casings and tubing:

Outer casing string(s) with different widths.

Tubing in centre.

Cement intervals shaded behind casings.

Packer and SSSV drawn with simple icons.

Annuli shown as coloured bands between strings:

Colour = status (based on utilisation).

Tooltip on hover: pressure, MAASP, utilisation, last measured.

Interaction:

Pan/zoom with mouse wheel/drag.

Hover tooltips.

Legend showing colour mapping (green/amber/red).

Button "Export as PNG" (using toDataURL on the SVG).

Layout idea (inspired by IPT + Wellbarrier):

Left: big schematic panel.

Right: stacked cards:

Primary Barrier Envelope:

Table listing elements + last test + status.

Secondary Barrier Envelope:

Same but separate card.

5.4.3 Barriers Tab

Full Barrier table:

Columns: Envelope, Element type, Name, Depth, Last test date, Last result, Status (pill), Notes.

Filters: envelope (primary/secondary), status (failed only).

Button: "Add test result" opens a modal.

5.4.4 Measurements Tab

Time-series charts per annulus:

Multi-line line chart of pressure vs time (A/B/C/D).

MAASP line overlay for each.

Zoom + pan.

SAP detections highlighted (markers).

Data table below chart with raw values.

Button: "Import CSV".

5.4.5 Tasks Tab

List of tasks related to this well with:

Title, due date, priority, status, related annulus/barrier.

Filter: open/closed, by priority.

Action buttons: complete, snooze.

5.5 Admin Page

Manage users (create/update roles).

Configure:

Default safety factor.

SAP thresholds.

Leak-rate acceptance (just stored values for now).

Risk matrix categories.


---

If you’d like, next we can:

- Turn this into a **checklist** for the AI (so you can tick off which parts Codex has implemented well).  
- Or start generating **actual backend or frontend code** following these specs.
::contentReference[oaicite:15]{index=15}
