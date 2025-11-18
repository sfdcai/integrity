Schematic DTO Builder

schematic_builder.py composes a data structure for the frontend D3 engine:

{
  "well": { "id": 1, "name": "A-15", "md": 3200, "tvd": 2950 },
  "casings": [
    { "id": 1, "name": "Surface", "od_in": 13.375, "top_md": 0, "bottom_md": 300 },
    { "id": 2, "name": "Production", "od_in": 9.625, "top_md": 0, "bottom_md": 2800 }
  ],
  "tubing": [
    { "id": 1, "name": "Production tubing", "od_in": 3.5, "top_md": 0, "bottom_md": 2700 }
  ],
  "cement": [
    { "casing_id": 2, "top_md": 1000, "bottom_md": 2800, "quality": "ok" }
  ],
  "annuli": [
    { "id": 1, "name": "A", "pressure_bar": 180, "maasp_bar": 230, "status": "amber" }
  ],
  "barriers": [
    { "id": 1, "type": "packer", "envelope": "primary", "depth_md": 2100, "status": "ok" },
    { "id": 2, "type": "sssv", "envelope": "primary", "depth_md": 1600, "status": "ok" }
  ]
}


Frontend uses this to render the schematic.
