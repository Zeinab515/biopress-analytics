# BIOPRESS Analytics (Phase 1 starter)

Software-only analytics for hand hygiene compliance audit data.

## Run
```bash
cd backend
pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload
```
Endpoints: `/health`, `/api/v1/analytics/summary`, `/api/v1/analytics/by-{ward,shift,indication,profcat}`.
Docs UI: http://127.0.0.1:8000/docs

## Status
- [x] Data audit and dictionary (`docs/`)
- [x] Descriptive analytics API with n, Wilson CI and chi-square test per dimension
- [ ] Database (PostgreSQL) and CSV import endpoint
- [ ] Dashboard
- [ ] ML evaluation (LogReg vs Dummy; allowed features only)
- [ ] XAI, reports, model_card

Raw data in `data/raw/` is read-only. Never commit patient-level or confidential data to a public repo.
