"""Prioritization API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.prioritization import PrioritizationScore
from app.models.territory import Territory
from app.schemas.schemas import PrioritizationWeights, PrioritizationScoreResponse

router = APIRouter()

@router.get("/ranking")
def get_ranking(scenario: str = "default", limit: int = 20, db: Session = Depends(get_db)):
    rows = db.query(PrioritizationScore, Territory.name, Territory.code).join(
        Territory, PrioritizationScore.territory_id == Territory.id
    ).filter(PrioritizationScore.scenario_name == scenario
    ).order_by(PrioritizationScore.score_total.desc()).limit(limit).all()
    return [{"territory_id": s.territory_id, "territory_name": name,
             "territory_code": code, "score_total": s.score_total,
             "priority_class": s.priority_class, "scenario": s.scenario_name,
             "scores": {"forest_restoration": s.score_forest_restoration,
                        "climate_risk": s.score_climate_risk,
                        "degradation_loss": s.score_degradation_loss,
                        "financial_gap": s.score_financial_gap,
                        "biodiversity": s.score_biodiversity,
                        "social_vulnerability": s.score_social_vulnerability,
                        "operational_feasibility": s.score_operational_feasibility,
                        "mechanism_alignment": s.score_mechanism_alignment}}
            for s, name, code in rows]

@router.post("/calculate")
def calculate_prioritization(weights: PrioritizationWeights, scenario_name: str = "custom",
                              db: Session = Depends(get_db)):
    """Recalculate prioritization with custom weights."""
    communes = db.query(Territory).filter(Territory.type == "commune").all()
    # Get existing default scores as base values
    results = []
    for c in communes:
        existing = db.query(PrioritizationScore).filter(
            PrioritizationScore.territory_id == c.id,
            PrioritizationScore.scenario_name == "default").first()
        if not existing:
            continue
        total = round(
            weights.forest_restoration_potential * (existing.score_forest_restoration or 0) / 0.20 * weights.forest_restoration_potential +
            weights.climate_risk * (existing.score_climate_risk or 0) / 0.15 * weights.climate_risk +
            weights.degradation_loss_risk * (existing.score_degradation_loss or 0) / 0.15 * weights.degradation_loss_risk +
            weights.financial_gap * (existing.score_financial_gap or 0) / 0.15 * weights.financial_gap +
            weights.biodiversity_value * (existing.score_biodiversity or 0) / 0.10 * weights.biodiversity_value +
            weights.social_vulnerability * (existing.score_social_vulnerability or 0) / 0.10 * weights.social_vulnerability +
            weights.operational_feasibility * (existing.score_operational_feasibility or 0) / 0.10 * weights.operational_feasibility +
            weights.mechanism_alignment * (existing.score_mechanism_alignment or 0) / 0.05 * weights.mechanism_alignment
        , 1)
        # Simpler recalculation using raw scores
        raw_total = round(
            weights.forest_restoration_potential * (existing.score_forest_restoration or 0) +
            weights.climate_risk * (existing.score_climate_risk or 0) +
            weights.degradation_loss_risk * (existing.score_degradation_loss or 0) +
            weights.financial_gap * (existing.score_financial_gap or 0) +
            weights.biodiversity_value * (existing.score_biodiversity or 0) +
            weights.social_vulnerability * (existing.score_social_vulnerability or 0) +
            weights.operational_feasibility * (existing.score_operational_feasibility or 0) +
            weights.mechanism_alignment * (existing.score_mechanism_alignment or 0)
        , 1)
        if raw_total >= 80: pc = "muy_alta"
        elif raw_total >= 60: pc = "alta"
        elif raw_total >= 40: pc = "media"
        elif raw_total >= 20: pc = "baja"
        else: pc = "muy_baja"
        results.append({"territory_id": c.id, "name": c.name, "score": raw_total, "priority_class": pc})
    results.sort(key=lambda x: x["score"], reverse=True)
    return {"scenario": scenario_name, "results": results}

@router.get("/territory/{territory_id}")
def get_territory_prioritization(territory_id: int, db: Session = Depends(get_db)):
    score = db.query(PrioritizationScore).filter(
        PrioritizationScore.territory_id == territory_id).first()
    if not score:
        return {"detail": "Sin datos de priorización para este territorio"}
    territory = db.query(Territory).filter(Territory.id == territory_id).first()
    return {
        "territory": {"id": territory.id, "name": territory.name} if territory else None,
        "score_total": score.score_total,
        "priority_class": score.priority_class,
        "components": {
            "forest_restoration": score.score_forest_restoration,
            "climate_risk": score.score_climate_risk,
            "degradation_loss": score.score_degradation_loss,
            "financial_gap": score.score_financial_gap,
            "biodiversity": score.score_biodiversity,
            "social_vulnerability": score.score_social_vulnerability,
            "operational_feasibility": score.score_operational_feasibility,
            "mechanism_alignment": score.score_mechanism_alignment,
        }
    }
