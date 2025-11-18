
# DeepGuard Frontend Design

## 1. Goals

Deliver a **modern, beautiful, and highly usable** web UI:

- Make complex well integrity data visually intuitive.
- Provide dashboards for portfolios and per-well details.
- Render high-quality D3 schematics similar to professional barrier diagrams.
- Be fast, responsive, and usable on laptops + tablets.
- Run natively on headless Ubuntu (served via `npm run dev` or `npm run build && pm2`).

---

## 2. Tech Stack

- Framework: **React** (with **Vite**)
- Language: **TypeScript**
- Styling: **Tailwind CSS**
- Charts: **Recharts** (for time-series graphs, risk matrix)
- Schematic: **D3.js + SVG**
- State: lightweight store (Zustand or React Query for server state)
- HTTP: Axios
- Icons: Lucide React

---

## 3. App Structure

```text
frontend/
  src/
    main.tsx
    App.tsx
    router.tsx
    api/
      client.ts
      wells.ts
      annuli.ts
      barriers.ts
      tasks.ts
      auth.ts
    store/
      authStore.ts
      uiStore.ts
    components/
      layout/
        Shell.tsx
        Sidebar.tsx
        Topbar.tsx
      common/
        Card.tsx
        Badge.tsx
        StatusPill.tsx
        DataTable.tsx
        Modal.tsx
        Tabs.tsx
        Tag.tsx
      charts/
        AnnulusTrendChart.tsx
        RiskMatrixChart.tsx
      wells/
        WellListTable.tsx
        WellStatusStrip.tsx
        AnnulusSummaryCard.tsx
        BarrierTable.tsx
        TaskList.tsx
      schematic/
        WellSchematicCanvas.tsx
    pages/
      LoginPage.tsx
      DashboardPage.tsx
      WellsPage.tsx
      WellDetailPage/
        WellOverviewTab.tsx
        WellSchematicTab.tsx
        WellBarriersTab.tsx
        WellMeasurementsTab.tsx
        WellTasksTab.tsx
      AdminPage.tsx
