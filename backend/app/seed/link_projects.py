"""Link projects helper script — associates existing projects with real communes."""
import os
import sys

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_dir)

from app.db.session import SessionLocal

# Import all models so they register with Base.metadata to prevent foreign key errors
from app.models import user, territory, mechanism, project, investment  # noqa
from app.models import intervention, mrv, prioritization, data_quality  # noqa
from app.models import layer, evidence, audit  # noqa

from app.models.project import Project
from app.models.territory import Territory

def link_projects():
    db = SessionLocal()
    try:
        print("Linking sample projects to real communes in the database...")
        projects = db.query(Project).all()
        
        # Mapping projects to real commune codes
        communes_mapping = {
            "Restauración cuenca Elqui": ["04101", "04102"],
            "Forestación Valparaíso": ["05101", "05109"],
            "Conservación bosque nativo Maule": ["07101", "07301"],
            "Prevención incendios Biobío": ["08101", "08201"],
            "Carbono campesino piloto": ["04101", "04102", "05101", "05109"],
            "Compensación biodiversidad minera": ["07101", "07301"]
        }
        
        for p in projects:
            codes = communes_mapping.get(p.name, [])
            if codes:
                # Find the territories with these codes
                com_territories = db.query(Territory).filter(Territory.code.in_(codes)).all()
                p.territories = com_territories
                print(f"  Linked project '{p.name}' to communes: {[c.name for c in com_territories]}")
        
        db.commit()
        print("[OK] Projects linked successfully to real geographical boundaries!")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to link projects: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    link_projects()
