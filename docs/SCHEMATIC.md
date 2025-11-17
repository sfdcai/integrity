# Schematic DTO and D3

Endpoint: `GET /api/wells/{id}/schematic`
Returns well metadata, annulus measurements, MAASP, utilisation, status, recommendation, and barrier elements with depths. The frontend D3 component (`frontend/src/d3/WellSchematic.jsx`) renders concentric casings, tubing, barrier markers, and pressure badges with zoom-friendly SVG.
