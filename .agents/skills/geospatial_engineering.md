# Skill — Geospatial engineering

Goal: implement safe and correct geospatial behavior.

Rules:
1. Use EPSG:4326 for API and frontend.
2. Validate geometries before saving.
3. Allow geometry to be optional when geographic precision is only regional/national.
4. Do not represent regional data as points.
5. Use GeoJSON for API layer responses.
6. Simplify demo geometries for frontend performance.
7. Store spatial data in PostGIS.
8. Include metadata for each layer.
9. Mark sample layers as `is_sample = true`.
10. Include `precision_level` for intervention geometries.

Required features:
- territories GeoJSON endpoint;
- layer list endpoint;
- intervention GeoJSON endpoint;
- map choropleth for prioritization;
- map choropleth for investment by territory.
