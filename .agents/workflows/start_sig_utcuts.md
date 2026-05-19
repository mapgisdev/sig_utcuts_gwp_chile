---
description: Start autonomous development pipeline for SIG-UTCUTS Chile
---

When the user types `/start_sig_utcuts`, orchestrate the development process using `.agents/agents.md` and `.agents/skills/`.

## Execution sequence

1. Act as `@pm` and execute `read_project_insumos.md`.
2. Act as `@pm` and execute `write_technical_spec.md`.
3. Act as `@geo` and review geospatial design.
4. Act as `@backend` and execute backend implementation from `generate_fullstack_app.md`.
5. Act as `@frontend` and execute frontend implementation from `generate_fullstack_app.md`.
6. Act as `@geo` and execute `geospatial_engineering.md`.
7. Act as `@devops` and execute `deploy_local.md`.
8. Act as `@qa` and execute `qa_audit.md`.
9. If QA finds failures, route fixes to the responsible agent and repeat QA.
10. Finish by summarizing:
    - how to run the app;
    - what was implemented;
    - what remains for future phases.
