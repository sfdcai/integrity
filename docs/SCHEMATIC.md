# Schematic DTO and Rendering

Endpoint: `GET /wells/{id}/schematic`

Returns casing strings, tubing, cement, barrier elements, annulus pressures, MAASP values, and labels for the D3 engine (`frontend/src/components/WellSchematic.jsx`).

The D3 schematic scales depth linearly and renders casing rectangles, tubing gradient, and barrier markers with tooltips.
