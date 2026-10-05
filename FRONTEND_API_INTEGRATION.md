# SAT-SA frontend API integration

The frontend deliberately uses only routes currently implemented by FastAPI. All requests use `VITE_API_BASE_URL` (default `http://127.0.0.1:8000`) through `frontend/src/api/client.ts`.

| Frontend page | Method and API | Component/use |
| --- | --- | --- |
| Dashboard | GET `/intelligence/summary` | KPI cards and risk-distribution chart |
| Analysts | GET `/api/v1/analysts?page&limit&status` | paginated analyst directory |
| Analyst profile | GET `/api/v1/analysts/{id}`, GET `/intelligence/analysts/{id}/profile` | identity and canonical fused intelligence |
| Findings | GET `/intelligence/findings` | canonical findings list |
| Finding detail | GET `/intelligence/analysts/{id}/profile` | full evidence and recommendations |
| Alerts | GET `/api/v1/alerts?page&limit` and GET `/api/v1/alerts/{id}` | list/detail |
| Investigations | GET `/api/v1/investigations?page&limit` and GET `/api/v1/investigations/{id}` | list/detail |
| Assets | GET `/api/v1/assets?page&limit` and GET `/api/v1/assets/{id}` | list/detail |

No authentication, user/profile, organization, notifications, or server settings endpoints exist in the current backend. The UI makes this explicit rather than creating fake data or API calls. Preferences only stores table density in browser local storage.

## Startup

1. `cd backend`; activate the existing virtual environment; run `uvicorn app.main:app --reload`.
2. `cd frontend`; copy `.env.example` to `.env` if needed; run `npm install`; run `npm run dev`.

On this workstation the `npm` shim in `%APPDATA%` is misconfigured. The included launcher uses the working Node installation directly:

```powershell
cd C:\Users\Umesh\OneDrive\Documents\merged-repo\frontend
.\start.ps1 dev
```

Use `./start.ps1 build` or `./start.ps1 lint` for the matching verification command.
