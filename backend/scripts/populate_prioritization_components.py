import os
import sys
import json
from sqlalchemy import text

# Configurar el path para poder importar módulos de la app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.territory import Territory
from app.models.prioritization import PrioritizationScore

def populate_components():
    db = SessionLocal()
    try:
        # 1. Hacer válidas todas las geometrías y crear índices espaciales
        print("  > Optimizando y reparando geometrías en PostGIS...")
        db.execute(text("UPDATE territories SET geom = ST_MakeValid(geom) WHERE geom IS NOT NULL AND NOT ST_IsValid(geom);"))
        db.execute(text("CREATE INDEX IF NOT EXISTS territories_geom_gist_idx ON territories USING gist(geom);"))
        db.commit()
        print("  > Geometrías optimizadas e índice GiST verificado.")

        # Cargar los datos de ARClim
        arclim_path = "/insumos/datos_geo/descargas/arclim_riesgo.json"
        arclim_data = {}
        if os.path.exists(arclim_path):
            with open(arclim_path, "r", encoding="utf-8") as f:
                records = json.load(f)
                for r in records:
                    cud = r.get("ComCod_CUD")
                    if cud:
                        arclim_data[cud] = r
            print(f"  > Leídos {len(arclim_data)} registros de ARClim.")

        # 2. Consulta espacial masiva (Bulk) para intersección de comunas y áreas de biodiversidad
        print("  > Calculando intersecciones espaciales en masa (Bulk)...")
        intersecting_rows = db.execute(text("""
            SELECT DISTINCT c.id
            FROM territories c
            JOIN territories ap ON ap.type = 'protected_area'
            WHERE c.type = 'commune'
              AND c.geom IS NOT NULL
              AND ap.geom IS NOT NULL
              AND ST_Intersects(ap.geom, c.geom)
        """)).fetchall()
        intersecting_ids = {row[0] for row in intersecting_rows}
        print(f"  > Detectadas {len(intersecting_ids)} comunas que intersectan con biodiversidad.")

        communes = db.query(Territory).filter(Territory.type == "commune").all()
        print(f"  > Procesando componentes para {len(communes)} comunas...")

        for idx, c in enumerate(communes):
            # 1. Componente Climático (ARClim)
            r_data = arclim_data.get(c.code) or arclim_data.get(c.code.zfill(5))
            climate_risk = 0.0
            if r_data:
                incendio = r_data.get("paarc_aysen_incendios_riesgo")
                humedal = r_data.get("parcc_magallanes_biodiversidadturismo_humedales_riesgo_humedal")
                nothofagus = r_data.get("parcc_magallanes_biodiversidadturismo_nothofagus_riesgo_nothofagus")
                if incendio is not None:
                    climate_risk = float(incendio) * 100
                elif humedal is not None:
                    climate_risk = abs(float(humedal)) * 100
                elif nothofagus is not None:
                    climate_risk = abs(float(nothofagus)) * 100
            
            # 2. Componente Biodiversidad
            biodiversity_score = 100.0 if c.id in intersecting_ids else 0.0

            # 3. Componentes Base (None si no hay datos reales cargados aún)
            forest_restoration = None
            degradation_loss = None
            financial_gap = None
            social_vulnerability = None
            operational_feasibility = None
            mechanism_alignment = None

            # Calcular score total inicial con normalización dinámica de pesos
            components = [
                (0.20, forest_restoration),
                (0.15, climate_risk),
                (0.15, degradation_loss),
                (0.15, financial_gap),
                (0.10, biodiversity_score),
                (0.10, social_vulnerability),
                (0.10, operational_feasibility),
                (0.05, mechanism_alignment),
            ]
            
            weighted_sum = 0.0
            weight_denominator = 0.0
            for w, val in components:
                if val is not None:
                    weighted_sum += w * val
                    weight_denominator += w
            
            total = (weighted_sum / weight_denominator) if weight_denominator > 0 else 0.0
            total = round(total, 1)

            if total >= 80: pc = "muy_alta"
            elif total >= 60: pc = "alta"
            elif total >= 40: pc = "media"
            elif total >= 20: pc = "baja"
            else: pc = "muy_baja"

            # Buscar si ya existe el registro
            score = db.query(PrioritizationScore).filter(
                PrioritizationScore.territory_id == c.id,
                PrioritizationScore.scenario_name == "default"
            ).first()

            if not score:
                score = PrioritizationScore(
                    territory_id=c.id,
                    scenario_name="default",
                    is_sample=False
                )
                db.add(score)

            score.score_forest_restoration = forest_restoration
            score.score_climate_risk = climate_risk
            score.score_degradation_loss = degradation_loss
            score.score_financial_gap = financial_gap
            score.score_biodiversity = biodiversity_score
            score.score_social_vulnerability = social_vulnerability
            score.score_operational_feasibility = operational_feasibility
            score.score_mechanism_alignment = mechanism_alignment
            score.score_total = total
            score.priority_class = pc

            if idx % 100 == 0:
                db.flush()

        db.commit()
        print("  [OK] Componentes e intersecciones espaciales de biodiversidad guardados exitosamente.")

    except Exception as e:
        db.rollback()
        print(f"Error al poblar componentes: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_components()
