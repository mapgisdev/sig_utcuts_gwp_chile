"""Vector tiles API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.deps import get_db

router = APIRouter()

@router.get("/{layer}/{z}/{x}/{y}.pbf")
def get_tile(layer: str, z: int, x: int, y: int, db: Session = Depends(get_db)):
    """Serve vector tiles using PostGIS ST_AsMVT."""
    
    # We map layer names to Territory types
    valid_layers = ["region", "commune", "ecosystem", "protected_area"]
    if layer not in valid_layers:
        raise HTTPException(status_code=404, detail="Capa no encontrada")

    # PostGIS ST_AsMVT query
    # ST_TileEnvelope generates the bounding box for the tile (Web Mercator 3857)
    # We transform our 4326 geometry to 3857 for the tile generation.
    query = text(f"""
        WITH bounds AS (
            SELECT ST_TileEnvelope(:z, :x, :y) AS geom
        ),
        mvtgeom AS (
            SELECT 
                t.id,
                t.name,
                t.code,
                t.area_ha,
                p.priority_class,
                p.score_total AS priority_score,
                p.score_climate_risk,
                ST_AsMVTGeom(ST_Transform(t.geom, 3857), bounds.geom) AS geom
            FROM territories t
            LEFT JOIN prioritization_scores p ON t.id = p.territory_id AND p.scenario_name = 'default'
            JOIN bounds ON ST_Intersects(ST_Transform(t.geom, 3857), bounds.geom)
            WHERE t.type = :layer AND t.geom IS NOT NULL
        )
        SELECT ST_AsMVT(mvtgeom, :layer) FROM mvtgeom;
    """)

    result = db.execute(query, {"z": z, "x": x, "y": y, "layer": layer}).scalar()

    if not result:
        return Response(content=b"", media_type="application/x-protobuf")

    return Response(content=bytes(result), media_type="application/x-protobuf")
