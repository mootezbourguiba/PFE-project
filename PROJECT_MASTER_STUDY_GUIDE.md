# AVIONAV — PROJECT MASTER STUDY GUIDE

**Purpose:** make you able to demonstrate, explain, and defend every part of the platform.
Every claim below was checked against the actual source code and the LaTeX report.
Where the report and the code disagree, the difference is stated explicitly.

Legend:

- **[IMPLEMENTED]** — verified directly in source code
- **[CONCEPTUAL]** — described in the report/design, not in code
- **[DEFERRED]** — planned, intentionally not built yet
- **[NOT VERIFIED]** — cannot be confirmed from available evidence
- **[EVIDENCE LIMITATION]** — script/report exists but no retained output proves the numbers

---

# 1. THE PROJECT IN ONE BIG PICTURE

**Problem.** UAV propulsion failures cause crashes. Bearing wear in a brushless DC motor is a *progressive* failure: friction rises slowly → the motor draws more current to hold speed → temperature rises (Joule heating, P = I²R). That slow drift is detectable *before* failure. The platform monitors motor **current** and **temperature** to detect that drift early.

**Platform.** A three-tier web application:

- **Streamlit frontend** (port 8501) — dashboards per role, Plotly charts/gauges
- **FastAPI backend** (port 8000, prefix `/api/v1`) — auth, RBAC, telemetry endpoints, ML inference
- **SQLite database** (`avionics.db`) via SQLAlchemy ORM + Alembic migrations
- **Isolation Forest** model (scikit-learn) trained on synthetic healthy flight data

**Users.** Administrator (manages accounts), Maintenance Engineer (full telemetry workflow + AI analysis), Drone Operator (read-only live status + alerts).

**Actual end-to-end flow (as implemented):**

```
User → Streamlit login form
     → POST /api/v1/auth/login (OAuth2 form)
     → bcrypt verify → JWT (sub, user_id, role, exp=24h)
     → JWT stored in st.session_state → role-based routing
     → every request carries "Authorization: Bearer <jwt>"
     → backend: decode → load user → disabled? → role check → endpoint
     → telemetry enters via 3 sources: SIMULATED / UPLOADED(CSV) / MANUAL(JSON)
     → validated → TelemetryReading rows committed to SQLite (owned by user_id)
     → Isolation Forest loaded once from isolation_forest.pkl
     → predict_anomaly(current, temperature) → HEALTHY/ANOMALY + score
     → prediction computed ON DEMAND per request (never stored)
     → Streamlit renders badges, gauges, charts, alert cards, tables, CSV export
```

**What comes out:** a HEALTHY/ANOMALY verdict, an anomaly score, a fixed recommendation string ("Normal operation" / "Maintenance inspection recommended"), dashboards, alerts, history, CSV export.

---

# 2. ARCHITECTURE I MUST BE ABLE TO EXPLAIN

```
┌──────────────────────────────┐         HTTP/JSON (requests.Session)
│  STREAMLIT FRONTEND :8501    │ ─────────────────────────────────────►
│  app.py (router)             │         Authorization: Bearer JWT
│  views/  components/  utils/ │ ◄─────────────────────────────────────
└──────────────────────────────┘         JSON responses
              │
┌─────────────▼─────────────── FASTAPI BACKEND :8000 ────────────────┐
│  main.py → api_router (/api/v1)                                    │
│    ├── auth.py        POST /auth/login                             │
│    ├── telemetry.py   7 endpoints (list/latest/stats/ingest/       │
│    │                 simulate/upload/predict)                      │
│    └── users.py       7 endpoints (admin CRUD)                     │
│  dependencies.py: get_current_user → role guards                   │
│  services/   → business logic                                      │
│  crud/       → SQLAlchemy queries                                  │
│  schemas/    → Pydantic validation                                 │
│  ml/anomaly_detector.py → joblib model                             │
└──────┬───────────────────────────┬─────────────────────────────────┘
       │ SQLAlchemy ORM            │ predict() / decision_function()
┌──────▼──────────┐       ┌────────▼────────────────────┐
│  avionics.db    │       │  isolation_forest.pkl       │
│  user           │       │  (Isolation Forest, trained │
│  telemetryread. │       │   on healthy data only)     │
│  alembic_vers.  │       └─────────────────────────────┘
└─────────────────┘
```

## Component-by-component

| Component | What / Why | Technology | File | Defense line |
|---|---|---|---|---|
| Entry point | Page config, session init, role router | Streamlit | `frontend/app.py` | "The router maps `session_state.current_page` + role to a view; unknown pages fall back to the role dashboard" |
| API client | Single HTTP client; injects JWT; converts errors to UI messages | `requests.Session` | `frontend/utils/api.py:14` | "All backend traffic goes through `APIClient`; the token header is added automatically" |
| Session/auth | session_state, login, role guards | Streamlit + PyJWT | `frontend/utils/auth.py` | "Frontend decodes the JWT claims to route; enforcement is still server-side" |
| API layer | Thin endpoints: authorize → validate → service → schema | FastAPI | `backend/api/v1/*` | "Endpoints contain no business logic" |
| Dependency layer | JWT→User, role guards, DB session | FastAPI `Depends` | `backend/dependencies.py` | "Every protected call passes through `get_current_user`" |
| Service layer | All telemetry business rules, CSV parsing, scoping, prediction calls | Python/pandas | `backend/services/telemetry_service.py` | "This is where the interesting decisions live" |
| CRUD layer | Pure DB access, no rules | SQLAlchemy | `backend/crud/*.py` | "Separating queries from rules makes both testable" |
| Schemas | Request/response validation | Pydantic v2 | `backend/schemas/*.py` | "Bad input → automatic 422 before my code runs" |
| Models | ORM entities | SQLAlchemy | `backend/models/*.py` | "Class = table; attribute = column" |
| Database | Persistence | SQLite + Alembic | `backend/database.py`, `alembic/` | "File-based for prototype; swap `DATABASE_URL` for Postgres" |
| ML engine | Anomaly inference | sklearn IF + joblib | `backend/ml/` | "Train offline once; load once at import; predict per request" |
| Simulator | Synthetic telemetry | NumPy | `backend/simulator/telemetry_generator.py` | "Physics-inspired: AR(1) current + I²R-coupled temperature" |

---

# 3. TECHNOLOGY STACK

| Technology | Purpose | Where used | Why used | Must know |
|---|---|---|---|---|
| Python 3.12 | Language | all | — | actual venvs are 3.12 (report says 3.9 — see discrepancies) |
| FastAPI 0.104.1 | REST API | `backend/` | async, auto-docs, Pydantic, DI | `/docs` Swagger is free |
| Uvicorn 0.24 | ASGI server | backend run | runs FastAPI | `uvicorn backend.main:app` |
| Streamlit 1.59 | Frontend | `frontend/` | pure-Python UI, fast to build | script reruns top-to-bottom per interaction |
| SQLite | DB | `avionics.db` | zero-config, file persistence | single-writer limitation |
| SQLAlchemy 2.0 | ORM | models/crud | Python objects ↔ rows | `add_all`/`commit`/`query` |
| Alembic 1.12 | Migrations | `alembic/` | versioned schema changes | `alembic upgrade head` |
| Pydantic 2.5 | Validation | `schemas/` | declarative validation | `Field(gt=0)`, enums, `field_validator` |
| python-jose 3.3 | JWT | `core/security.py` | sign/verify tokens | HS256 |
| PyJWT | JWT decode | `frontend/utils/auth.py` | read claims client-side | same SECRET_KEY/HS256 |
| passlib 1.7 + bcrypt 3.2 | Password hashing | `core/security.py` | salted, slow, standard | `CryptContext(schemes=["bcrypt"])` |
| scikit-learn 1.3 | ML | `backend/ml/` | IsolationForest | predict + decision_function |
| Joblib | Model persistence | `ml/train_model.py`, `anomaly_detector.py` | serialize sklearn objects | `.pkl` file |
| pandas 2.1 | Data wrangling | service CSV path, views | DataFrame ops | `pd.to_datetime(..., errors='coerce')` |
| NumPy 1.26 | Simulation | generator | RNG + vector math | `default_rng(seed)` |
| Plotly | Charts/gauges | `components/charts.py`, `gauges.py` | interactive figures | `st.plotly_chart` |
| python-multipart | Form/file uploads | auth login, CSV upload | FastAPI needs it for forms | OAuth2 form + `UploadFile` |
| LaTeX | Report | `main.tex`, `chapters/` | thesis document | — |

> Note: `requirements.txt` does **not** list `streamlit`, `plotly`, `requests`, or `Pillow` — the frontend runs from `venv_frontend` with its own deps. Small doc gap; harmless but know it.

---

# 4. BACKEND — DEEP EXPLANATION

## Module map

| Module | Responsibility | Key items | Talks to |
|---|---|---|---|
| `backend/main.py` | App factory, CORS, router mount, `/`, `/health` | `app`, `api_router` | everything |
| `backend/database.py` | Engine, SessionLocal, `get_db` | `DATABASE_URL`, `check_same_thread=False` | models, dependencies |
| `backend/models/base.py` | `BaseModel`: `id`, `created_at`, `updated_at`, auto `__tablename__` | `declared_attr` | all models |
| `backend/models/user.py` | `UserRole` enum, `User`, `is_*()` helpers | 3 roles | dependencies, services |
| `backend/models/telemetry.py` | `TelemetrySource` enum, `TelemetryReading` | FK user_id, source, anomaly | services, crud |
| `backend/schemas/*` | Validation in/out | `TelemetrySimulationRequest`, `UserCreate` (+validators), `Token` | endpoints |
| `backend/core/security.py` | bcrypt + JWT | `verify_password`, `create_access_token`, `decode_access_token` | auth service, dependencies |
| `backend/services/auth_service.py` | Authenticate + issue token | `authenticate_user`, `create_token_for_user` | auth endpoint |
| `backend/services/telemetry_service.py` | simulate, ingest_json, ingest_csv, scoping, latest+predict, stats | see §9 | endpoints, crud, generator, ml |
| `backend/crud/*` | Queries only | `create_many`, `get_by_user`, `create_user`… | services, endpoints |
| `backend/dependencies.py` | `get_current_user` + role deps + `require_role` factory | the RBAC gate | every endpoint |
| `backend/simulator/*` | Synthetic data | `generate_telemetry_data`, `generate_dataset.py` | service |
| `backend/ml/*` | train / detect / evaluate | `train_model.py`, `anomaly_detector.py`, `evaluate_model.py` | service, endpoints |

## Actual API surface (verified — nothing else exists)

Base URL: `http://localhost:8000/api/v1`. Unprotected: `GET /`, `GET /health`, `POST /auth/login`.

| Method | Endpoint | Purpose | Auth/Role | In → Out | Errors | Source |
|---|---|---|---|---|---|---|
| POST | `/auth/login` | OAuth2 password login | public | form `username`,`password` → `Token{access_token,token_type}` | 401 bad creds | `api/v1/auth.py:11` |
| GET | `/telemetry/` | list readings | ME or DO | `skip`,`limit` → `TelemetryList{total,items}` | 403 admin; 403 DO if `limit>50` or `skip≠0` | `endpoints/telemetry.py:35` |
| GET | `/telemetry/latest` | newest reading + prediction + recommendation | ME or DO | → `TelemetryLatest` | 403 admin | `:69` |
| GET | `/telemetry/stats` | counts + latest prediction | Admin or ME | → `TelemetryStats` | 403 DO | `:95` |
| POST | `/telemetry/` | JSON ingest (MANUAL) | ME | `List[TelemetryCreate]` → `TelemetryList` (201) | 400 empty; 400 invalid values | `:122` |
| POST | `/telemetry/simulate` | generate flight | ME | `TelemetrySimulationRequest` → `TelemetryList` (201) | 422 bad params | `:146` |
| POST | `/telemetry/upload` | CSV ingest (UPLOADED) | ME | multipart file → `TelemetryList` (201) | 400 for each validation rule | `:167` |
| POST | `/telemetry/predict` | one-shot inference | ME | `{current,temperature}` → `TelemetryPrediction` | 422 if ≤0 | `:192` |
| GET | `/users/` | list users | Admin | `skip`,`limit` → `List[UserResponse]` | 403 others | `endpoints/users.py:13` |
| POST | `/users/` | create user | Admin | `UserCreate` → `UserResponse` (201) | 400 dup username/email; 400 admin role | `:47` |
| GET | `/users/{id}` | one user | Admin | → `UserResponse` | 404 | `:115` |
| PUT | `/users/{id}` | update email/role | Admin | `UserUpdate` → `UserResponse` | 404; 400 admin/`administrator` | `:153` |
| PATCH | `/users/{id}/disable` | soft-disable | Admin | `{disabled,reason}` → `UserStatusResponse` | 404; 400 self/`admin` | `:230` |
| PATCH | `/users/{id}/enable` | re-enable | Admin | → `UserStatusResponse` | 404 | `:304` |

> The report/README list `/api/flights`, `/api/anomalies`, `/api/auth/login` — those were **planned** routes. Implemented routes are above. Say: *"The flight-resource API from the design phase was consolidated into the telemetry resource; the functional coverage is equivalent."*

---

# 5. AUTHENTICATION AND SECURITY — FULL TRACE

```
1. User types username+password → views/login.py:398 st.button
2. utils/auth.py:43 login() → utils/api.py:283 login()
3. api_client.post("/auth/login", form_data=True)
   → POST /api/v1/auth/login  (x-www-form-urlencoded)
4. auth.py: OAuth2PasswordRequestForm → AuthService.authenticate_user
5. services/auth_service.py:39-47:
     user = query(username)            # not found → None
     verify_password(pw, hashed)       # bcrypt; wrong → None
     user.disabled                     # disabled → None
   → None ⇒ HTTP 401 "Incorrect username or password" (generic, no enumeration)
6. create_token_for_user: claims = {sub: username, user_id: id, role: value}
   → security.py create_access_token: adds exp = utcnow()+1440min, HS256, SECRET_KEY
7. Frontend: stores access_token → session_state.token/authenticated;
   jwt.decode locally (utils/auth.py:59) → user, user_id, role
   → sets landing page per role → st.rerun → app.py router
8. Every later request: _get_headers() adds Authorization: Bearer <jwt>
9. Backend: HTTPBearer → get_current_user (dependencies.py:13):
     decode_access_token (signature + exp)  → None ⇒ 401
     payload["user_id"] → DB user lookup    → missing ⇒ 401
     user.disabled                          → 401 "Account disabled"
10. Role dependency (get_current_admin / _maintenance_engineer /
    _drone_operator) or inline role checks → wrong role ⇒ 403
11. Endpoint executes → response → frontend renders
```

**Must-say facts:**
- Passwords never stored in plaintext — bcrypt hash (salt + cost embedded, `$2b$…`), constant-time verify via passlib.
- JWT is **stateless**: server doesn't store sessions; validity = signature + expiry + DB-side user/disabled check.
- 401 = authentication failure ("who are you"); 403 = authorization failure ("known user, wrong role").
- Disabled accounts are checked **twice**: at login AND per-request → disabling takes effect even for tokens already issued.
- Frontend hiding is UX only; the real gate is `Depends(get_current_*)` + inline role checks — proven by the 66-assertion audit where raw API calls as operator still got 403.

**Honest weaknesses (say them first if asked):** `SECRET_KEY` falls back to a dev default (backend) and is duplicated hardcoded in `frontend/utils/auth.py:15`; no refresh tokens; no rate limiting/lockout; HTTP not HTTPS. Prototype-acceptable, production-TODO (TESTING.md says the same).

**Likely Q: "What if a Drone Operator calls `GET /api/v1/users/` directly?"**
A: HTTPBearer supplies the token → `get_current_user` returns the operator User → `get_current_admin` runs `is_administrator()` → false → **403** before any CRUD executes. Verified live during the audit.

---

# 6. ROLES AND RBAC

| Role | Can do | Cannot do | View | Business purpose |
|---|---|---|---|---|
| **Administrator** | user CRUD, disable/enable, stats | detailed telemetry (latest/list = 403), predict, simulate, upload; cannot modify/disable `admin`; cannot create admins | Dashboard + Users + Settings | account governance, separation of duties |
| **Maintenance Engineer** | own telemetry list/latest/stats, predict, simulate, CSV upload, JSON ingest, history, AI analysis, CSV export | `/users/*` (403) | Dashboard + Telemetry + History + Settings | analyze propulsion health, plan maintenance |
| **Drone Operator** | shared `/latest`, shared list (limit≤50, skip=0 only) | stats, predict, ingest, simulate, upload, `/users/*` — all 403 | Dashboard + Logout only | in-flight status + alerts, nothing else |

**Enforcement locations (memorize):**
- Role guards: `dependencies.py:85,115,140` (+ `require_role` factory :165)
- Operator limits inline: `endpoints/telemetry.py:54`
- Admin denial of telemetry inline: `:48, :79`
- Data scoping in service: `telemetry_service.py:246` (list) and `:284` (latest) — operators bypass the `user_id` filter → **shared operational feed**
- Admin-account protection: `users.py:195` (update), `:273` (disable), `:280` (self); admin-role creation blocked in schema validator `schemas/user.py:42` + endpoint `:95` (defense in depth)
- Frontend: `sidebar.py:94-142` role menus; `app.py:61` router

---

# 7. DATABASE

```
            user                                    telemetryreading
┌───────────────────────────────┐         ┌───────────────────────────────────┐
│ id            PK auto         │◄────────│ user_id      FK → user.id  (idx)  │
│ username      VARCHAR(50) UQ  │  1   N  │ timestamp    DATETIME      (idx)  │
│ email         VARCHAR(100) UQ │         │ current      FLOAT NOT NULL       │
│ hashed_password VARCHAR(255)  │         │ temperature  FLOAT NOT NULL       │
│ role          ENUM(*)         │         │ anomaly      BOOLEAN NULL         │
│ disabled      BOOLEAN         │         │ source       ENUM(**) NOT NULL    │
│ disabled_reason TEXT          │         │ id           PK auto       (idx)  │
│ created_at / updated_at       │         │ created_at / updated_at           │
└───────────────────────────────┘         └───────────────────────────────────┘
(*) stored as enum NAME: ADMINISTRATOR / MAINTENANCE_ENGINEER / DRONE_OPERATOR
(**) SIMULATED / UPLOADED / MANUAL  — CHECK-constrained (create_constraint=True)
```

- `BaseModel` gives every table `id`, `created_at`, `updated_at` (server defaults) — `models/base.py`.
- Ownership: `TelemetryReading.user_id` FK + `relationship("User", backref="telemetry_readings")` — every row belongs to whoever created it.
- `anomaly` is a **stored ground-truth label** (generator/CSV), nullable — **not** the model's prediction. This distinction is a likely trap question.
- Migrations: `001_initial_schema` (user) → `a6b348beb400` (adds `disabled`) → `8c163a76a997` (telemetryreading + indexes + enum). `alembic upgrade head` applies; each has a `downgrade()`.
- Why SQLAlchemy: ORM = write Python objects instead of SQL; engine-agnostic (SQLite today, Postgres by env var).
- Why Alembic: `create_all` can't ALTER existing tables; migrations version the schema and preserve data. `main.py:48` explicitly defers table creation to Alembic.

> **[DEFERRED]** `FlightSession` and `AnomalyEvent` appear in report acceptance criteria (US-07/US-08/US-09) and TESTING.md "Next Steps" — **they are not implemented**. `TelemetryReading` links to `user`, not to a flight. The commented relationship sits at `models/user.py:60-66`. If asked: *"Flight grouping was descoped; readings carry a timestamp + owner instead; FlightSession is future work."*

---

# 8. TELEMETRY PIPELINE

Fields per reading: `timestamp`, `current` (A), `temperature` (°C), `anomaly` (bool|null), `source`, `user_id`.

### Source 1 — Simulation (SIMULATED)
`POST /telemetry/simulate` → `simulate_telemetry` (service :64) → `generate_telemetry_data` → ORM rows → `create_many` (`db.add_all`+`commit`) → `TelemetryList`.

### Source 2 — CSV upload (UPLOADED)
`POST /telemetry/upload` (multipart) → `ingest_csv` (service :172):
1. read bytes → `pd.read_csv`; empty → 400
2. lowercase/strip headers; required: `timestamp`, `current`|`motor_current`, `temperature`|`motor_temperature` → 400 if missing
3. `pd.to_datetime(errors="coerce")` → any NaT → 400 with count
4. `pd.to_numeric(errors="coerce")` → any NaN → 400
5. `current <= 0` → 400; `temperature <= -273.15` → 400
6. optional `anomaly`: bool/int→bool; strings in {1,true,yes}→True else False
7. rows → ORM (source=UPLOADED) → commit → 201 + items

**CSV validation — precise limits (know these):**
- **All-or-nothing**: one bad row → whole file rejected, nothing stored (transactional, clean).
- **No upper range checks**: current=9999 A or temp=500 °C is accepted — only physical minimums enforced.
- **Unsupported anomaly text → False** (e.g. `"maybe"` becomes False — falsifiable label risk).
- **`+inf` passes `pd.to_numeric`** — the CSV path does not check `math.isfinite`; the JSON path *does* (`_validate_value` checks finiteness, service :34). Slight asymmetry — honest detail.
- No duplicate detection, no monotonic-timestamp check, no row-count cap beyond HTTP limits.

### Source 3 — Manual/JSON ingest (MANUAL)
`POST /telemetry/` with `List[TelemetryCreate]` → `ingest_json` (service :97) → per-item `_validate_value` (number, finite, above min) → commit → 201. Default source when CSV/simulator aren't used.

### Retrieval & display
`GET /telemetry/` → service scopes by role → newest-first → frontend `_to_dataframe` (parse timestamps, sort) → tables + Plotly charts with red anomaly markers (`charts.py:69`). `GET /latest` → newest row + on-demand prediction + fixed recommendation. History page = limit=1000 + client-side date filter + 5-column CSV download.

---

# 9. TELEMETRY SIMULATION — DEEP

`backend/simulator/telemetry_generator.py:34 generate_telemetry_data(samples, anomaly, wear_start, seed, start_time)`.

- **Healthy current**: AR(1) mean-reverting — `I[t] = 0.92·(I[t-1] − 15) + 15 + N(0, 0.18)` (line 85). Mean 15 A, nominal σ 0.6. Why AR(1): real signals are temporally correlated, not white noise.
- **Healthy temperature**: `target = 42 + 0.045·I²` (thermal coupling = Joule heating), then exponential smoothing `T[t] = 0.85·T[t-1] + 0.15·target + noise` (lines 91-95). Mean ≈ 42 °C at I=0 baseline, ≈ 52 °C at 15 A.
- **Wear scenario** (`anomaly=True`): healthy until `wear_start` (default = 30% of samples, line 75), then per-sample drift `+0.08·t` A and `+0.25·t` °C plus noise, and `anomaly=True` labels from that point (lines 101-113).
- **Timestamps**: 1-second steps from `utcnow()` (line 130).
- **Seed**: `np.random.default_rng(seed)` — identical params+seed ⇒ identical series (reproducibility; your demo used 42 → 18.16 A / 60.2 °C final → ANOMALY).
- **Clamps**: current [0,100], temperature [−273.15,200].

**Frontend**: `views/telemetry.py:128-190` — selects scenario/samples/seed/wear_start → `simulate_telemetry` → `POST` → success banner + preview table (fixed recently — no more silent `st.rerun`).

**What simulation does NOT prove** — say it unprompted: synthetic series ≠ real flight data; injected linear drift ≠ physically measured bearing degradation. It proves the *pipeline* (generate→store→detect→display), not physical validity. The generator and detector share assumptions — a fair evaluation needs real telemetry or an independent dataset.

---

# 10. ISOLATION FOREST — BEGINNER TO IMPLEMENTATION

### Concept
Anomaly detection = find observations unlike the rest. **Unsupervised**: trained on healthy data only — no labeled faults needed (we don't have them).

Isolation Forest intuition: recursively split the feature space on random feature/random split value. Points deep inside the "normal cloud" need many splits to isolate; outliers sit alone → isolated in **few** splits → short average path length across 100 trees → low score → anomaly.

### Actual implementation

```
datasets/healthy_flight_data.csv   (1000 rows, generator output, all healthy)
   │ train_model.py
   ▼
X = df[["current","temperature"]]                      (line 22 — TWO features only)
IsolationForest(contamination=0.01, random_state=42)   (line 26 — everything else default)
model.fit(X)                                           (line 31 — healthy-only training)
joblib.dump → backend/ml/saved_models/isolation_forest.pkl   (line 39)
   │
   ▼ runtime
anomaly_detector.py: model = joblib.load(MODEL_PATH)   (line 14 — once, at import)
predict_anomaly(current, temperature):
   predict()    → +1 = HEALTHY, −1 = ANOMALY           (line 30/34)
   decision_function() → float score                  (line 31/35)
   → {"prediction": "HEALTHY"|"ANOMALY", "score": rounded}
```

**Consumers:** `POST /telemetry/predict` (direct), `GET /latest` and `GET /stats` (embedded, per-request). Predictions are **computed, never persisted**.

**Parameters to explain:**
- `contamination=0.01` — expect ~1% anomalies; positions the score threshold. Conservative → few false alarms.
- `random_state=42` — reproducible training.
- `n_estimators` — *not set* → sklearn default **100** trees. (Report says 100 — consistent, but it's the default, not a chosen value.)
- Two features only: current + temperature — matching the scope reduction (P=I²R link).

### Three distinct things (trap question insurance)
1. **Stored `anomaly` column** — ground-truth label injected by the generator/CSV.
2. **Model prediction** — fresh inference from current+temperature; independent of the stored flag.
3. **Anomaly score** — `decision_function` magnitude; sign = verdict, magnitude = confidence.

They can disagree — and that disagreement is exactly what `evaluate_model.py` measures (predictions vs labels → precision/recall/F1).

### Clear boundaries
- IMPLEMENTED: binary anomaly **detection** + score.
- NOT implemented: fault diagnosis ("*which* fault"), failure-time prediction, RUL, explainability (feature importance — report FR-09/ch6 mention it; **no such code exists**).

---

# 11. ML LIMITATIONS — HONEST ANSWERS

**"How do you know the model is accurate?"** — the honest answer:

> "Two levels of evidence. (1) The evaluation script `backend/ml/evaluate_model.py` computes accuracy/precision/recall/F1 against the labeled synthetic set — the report cites ~0.90 F1, but I have no retained execution output, so treat that as *claimed, not independently reproduced*. (2) Live validation: I demonstrated end-to-end that healthy inputs score positive and bearing-wear-generated flights score negative — e.g. the demo flight ends at 18.16 A / 60.2 °C → ANOMALY, score −0.036. What I do **not** have: real motor data, an independent test set, or a physical bearing experiment — so accuracy claims apply to the synthetic distribution only."

- No held-out protocol: training set = the same generator that produced test data (shared assumptions → optimistic metrics).
- Report ch6 says "cross-validation" — **[NOT IMPLEMENTED]**: `evaluate_model.py` does a single concat+predict pass; Isolation Forest isn't cross-validated anywhere.
- `contamination` in code is **0.01**; report ch6 says **0.05** — code wins; say 1%.
- No explainability module, no per-feature contribution, no confidence intervals.

---

# 12. FRONTEND / STREAMLIT — VIEW BY VIEW

| View | File | Role | Sees | Calls |
|---|---|---|---|---|
| Login | `views/login.py` | all | glassmorphism form | `POST /auth/login` |
| Admin dashboard | `dashboard_admin.py` | admin | user count, telemetry totals, pie, status, user table | `GET /users/`, `GET /telemetry/stats` |
| Users | `views/users.py` | admin | list/search/filter, create form, manage (update/disable/enable; admin protected) | `GET/POST/PUT/PATCH /users*` |
| ME dashboard | `dashboard_maintenance.py` | ME | health banner+recommendation, 4 KPIs, gauges, trend charts, AI card + Run Prediction, recent alerts | `GET /latest`, `GET /telemetry/?limit=100`, `POST /predict` |
| Telemetry workspace | `views/telemetry.py` | ME | 5 tabs: Live(50)/Historical(1000)/Simulation/CSV/AI Analysis | `GET /telemetry/`, `POST /simulate`, `POST /upload`, `POST /predict` |
| History | `views/history.py` | ME | date-filtered charts+table, CSV download, batch AI analysis, alert history | `GET /telemetry/?limit=1000`, `POST /predict` ×N |
| Settings | `views/settings.py` | admin+ME | platform info, model file path/status, dataset row counts, About | none (filesystem reads) |
| Operator dashboard | `dashboard_operator.py` | DO | status badge+recommendation, anomaly alert card, 3 KPIs, 2 gauges, last-50 charts | `GET /latest`, `GET /telemetry/?limit=50` |

Mechanics to explain: session_state auth → `app.py` router → sidebar sets `current_page` → each view calls `require_*` guard then API wrappers → pandas DataFrame → Plotly/`st.dataframe`. **No auto-refresh**: "live" = newest stored reading at render time; updates happen on navigation/rerun. (Report's "5s updates" — **[NOT IMPLEMENTED]**.)

---

# 13. DEMO SCENARIO (10–15 min)

State check first: services up (`uvicorn backend.main:app` / `streamlit run frontend/app.py`), `/docs` loads, model `.pkl` exists.

| # | Click/type | See | Technically | Say |
|---|---|---|---|---|
| 1 | open :8501 | login page | unauthenticated → sidebar hidden (`app.py:34`) | "Three roles; I'll start as the engineer" |
| 2 | login `maint1` | ME dashboard | OAuth2 form → bcrypt → JWT → claims → router | "JWT carries my role; every request re-verifies it" |
| 3 | point at banner | HEALTHY + recommendation | `GET /latest` → newest row → `predict_anomaly` | "Prediction is computed on the fly, not stored" |
| 4 | Run Prediction 15A/45°C → then 18A/60°C | HEALTHY → ANOMALY card | `POST /predict` → IF score sign | "Two features; score positive=healthy" |
| 5 | Telemetry→SIMULATION: bearing_wear, 50, seed 42, wear_start 15 → GENERATE | "Stored 50 readings" + table | generator drift → `create_many` → SQLite | "AR(1) baseline + I²R coupling + linear wear drift; seed=reproducible" |
| 6 | LIVE/HISTORICAL tabs | gauges, red anomaly markers | `GET /telemetry/` own-scope | "Red = generator's ground-truth label — separate from model inference" |
| 7 | History→AI ANALYSIS→RUN | table + "N anomalies" | loop `POST /predict` over tail rows | "Batch inference over persisted history" |
| 8 | History→Download CSV | file w/ 5 cols | client-side `to_csv` of displayed subset | "Export matches what you see" |
| 9 | Settings→AI MODEL | model path, "Loaded", 1000/300 rows | filesystem reads | "Offline-trained joblib artifact" |
| 10 | logout → `admin` → Users→MANAGE→select admin | controls disabled | endpoint + UI double protection | "Admin manages accounts but can't touch telemetry or itself" |
| 11 | logout → `operator_test` | ANOMALY badge + alert + gauges | shared `/latest` (no user filter for DO) | "Operator sees the flight I just generated — same feed, minimal view" |
| 12 | close | — | — | "Detection, not diagnosis; simulated data; per-engineer scoping; future: real ingestion + FlightSession" |

Backup if a step fails: stored data already contains anomaly rows → jump to History AI analysis; Swagger `/docs` can demo every endpoint including the 403s.

---

# 14. "WHAT IS HAPPENING BEHIND THE BUTTON?"

**Login** — see §5 trace.

**GENERATE FLIGHT** — `telemetry.py:173` button → `simulate_telemetry()` (`api.py:441`) → `POST /telemetry/simulate` → `get_current_maintenance_engineer` → `TelemetrySimulationRequest` validation → `service.simulate_telemetry` → `generate_telemetry_data` → `_readings_to_model` (user_id stamped) → `crud.create_many` (`add_all`+`commit`) → `TelemetryList` → success + `st.dataframe(head(20))`.

**UPLOAD CSV** — `st.file_uploader` + `telemetry.py:207` button → `upload_telemetry_csv` → `post_file` multipart → `POST /upload` → `ingest_csv` 6-step validation → `create_many` → 201 → success + preview table. Reject → 400 detail → `alert_card`.

**Open History** — `history.py:31` → `get_telemetry(limit=1000)` → `GET /telemetry/` → own-user rows newest-first → `_load_telemetry` → date mask → charts + table + download button.

**RUN AI ANALYSIS** — `history.py:119` → loop `df.tail(N)` → `predict_telemetry` each → results df + anomaly count card. (N HTTP calls — honest inefficiency.)

**Download CSV** — pure frontend: `filtered[5 cols].to_csv(index=False)` → `st.download_button` — no backend call.

**Operator dashboard load** — `GET /latest` → service skips user filter for operators → newest system-wide row + prediction → badge/alert; `GET /telemetry/?limit=50` → shared newest-50.

---

# 15. SPRINTS — WHAT WAS ACTUALLY BUILT

Report planning table (ch3) says Sprints 0–5; chapter titles then label implementation chapters "Sprint 1/2/3" with shifted content — a numbering quirk to be aware of, not a defect. Present it as six phases:

| Sprint | Objective (planned) | Actually delivered | Key files |
|---|---|---|---|
| 0 | Scope, UAV context, architecture, DB design | Scope reduced 5→2 params; BWB/fixed-wing + BLDC/ESC design; layered architecture | ch3/ch4, models, alembic 001 |
| 1 | Auth + database | user table, bcrypt, JWT login, admin user CRUD, disabled flag | `auth.py`, `security.py`, `users.py`, `crud/user.py`, migrations |
| 2 | Data pipeline | telemetry table, simulator, CSV ingest, JSON ingest, datasets | `telemetry_generator.py`, `telemetry_service.py`, migration `8c163a76a997` |
| 3 | Anomaly engine | IF training (healthy-only), `.pkl`, `predict_anomaly`, `/predict`, embedded in `/latest`+`/stats` | `ml/train_model.py`, `anomaly_detector.py` |
| 4 | API + dashboard | all `/telemetry`+`/users` endpoints, 3 role dashboards, charts/gauges/alerts | `endpoints/*`, `frontend/*` |
| 5 | Integration + report | e2e browser validation, 66-assertion RBAC audit, bug fixes (CSV export, HTML render, admin crash, simulation feedback) | TESTING.md, git history |

**Why Scrum:** incremental demonstrable increments, supervisor-as-PO validation each sprint, DoD gates — matches a solo project with industrial supervision.

> DoD claims "unit tests ≥80% coverage" — **[NOT IMPLEMENTED]** as a suite: `backend/tests/` is empty; validation was manual/browser + ad-hoc scripts. If asked, be straight: *"The DoD target wasn't met formally; coverage evidence is functional/browser-level plus the API assertion matrix."*

---

# 16. TESTING & VALIDATION — WHAT EVIDENCE EXISTS

**A. Actually demonstrated/verified (retained evidence):**
- Login/invalid-login/logout; JWT missing→403, invalid→401 — executed.
- Full browser pass of all role views; operator healthy + anomaly dashboards; screenshots in `report_assets/`.
- Simulation writes (DB counts before/after), CSV accept+reject paths, predict both classes — executed and DB-verified.
- 66-assertion multi-account API/RBAC audit (all operators/MEs/admin) — executed, zero writes, script retained (`_matrix_test.py`).
- DB integrity: counts, source distribution, zero orphans — executed.

**B. Source-verified (not dynamically run):** disabled-account enforcement, admin protection guards, enum constraints, migration chain.

**C. Scripts exist, execution output not retained:** `evaluate_model.py` (metrics claimed in report but no output file), `_*.py` probes, `test_role_isolation.py`.

**D. Not validated:** real-hardware telemetry; performance/load (NFR-01 <2s claimed 0.5s — plausible for localhost, unmeasured formally); Python 3.9/Ubuntu env from report vs actual 3.12/Windows; "5s real-time updates" (not implemented); pytest coverage.

**Report metric table (ch8/annexA: P .92, R .88, F1 .90, FPR 8%)** — **[EVIDENCE LIMITATION]**: defensible as "from `evaluate_model.py` on the synthetic labeled set", not independently reproduced. Never volunteer as hard truth.

---

# 17. LIMITATIONS

| Category | Limitation | Why | Impact | Future |
|---|---|---|---|---|
| Technical | SQLite single-writer | prototype choice | concurrency ceiling | Postgres via `DATABASE_URL` |
| Technical | Poll-not-push UI | Streamlit model | "live" = per-render | websocket/refresh component |
| Technical | No refresh token; default SECRET_KEY fallback; HTTP | scope | token lifetime 24h; dev key | env secrets, HTTPS, refresh, rate-limit |
| Technical | Per-engineer telemetry scoping | current ownership model | MEs don't share one dataset | FlightSession grouping |
| Data | Synthetic telemetry only | no UAV hardware | unknown real-world drift | real ESC/telemetry ingest |
| ML | 2 features, 1 failure mode | scope decision | no diagnosis, no other faults | vibration/current-spectrum features, multi-class |
| ML | Predictions not persisted | on-demand design | no prediction history audit | AnomalyEvent table |
| ML | No explainability | not built | "why" = score only | feature attribution module |
| Validation | Metrics not independently reproduced; no unit suite | time | claims rest on synthetic data | retained eval output + pytest |
| Deployment | localhost only, no containers | prototype | not production | Docker, CI, monitoring |
| Evidence | Report numbers (F1, response time, test env) partially unverifiable | docs ahead of impl | defense risk | regenerate metrics before defense if possible |

---

# 18. 50+ SUPERVISOR QUESTIONS

**General**

1. *What does the platform do?* — Monitors BLDC-motor current+temperature, detects bearing-wear-like anomalies via Isolation Forest, alerts operators, gives engineers history+analysis. Follow-up: why bearing wear → only progressive failure mode with time-series precursors.
2. *What data do you use?* — Simulated (AR(1)+thermal coupling), CSV uploads, JSON ingest. Follow-up: real data? → not yet; ingestion contract is ready (`POST /telemetry/`).

**Architecture**

3. *Why FastAPI+Streamlit instead of React?* — Annex-A comparison: single-developer velocity; Streamlit for data apps; FastAPI for typed APIs. Follow-up: scalability → swap frontend freely; API is independent.
4. *Where is business logic?* — `services/`; endpoints thin; CRUD thinner. Follow-up: why → testability/separation.
5. *Is it real-time?* — Honest: on-demand inference + render-time refresh; no streaming. Follow-up: how to make real-time → polling component or websockets.

**Backend/API**

6. *List your endpoints.* — §4 table (15 routes). Follow-up: which need auth → all except `/`, `/health`, `/auth/login`.
7. *What does Depends do?* — Injects authenticated User/DB session before handler; the RBAC seam.
8. *What validates input?* — Pydantic: types, ranges (`gt=0`, `ge/le`), enums, custom validators; 422 automatic.
9. *Status codes used?* — 200/201/400/401/403/404/422. Follow-up: 401 vs 403 → authn vs authz.

**Database**

10. *Schema?* — `user` + `telemetryreading`, FK `user_id`, enum constraints, 3 indexes. 
11. *Where's FlightSession?* — **[DEFERRED]** — descoped; readings carry timestamp+owner. Don't let them think it's implemented.
12. *Why Alembic?* — versioned, reversible schema changes; `create_all` can't alter.
13. *Orphaned readings possible?* — FK + no user-delete endpoint → none (verified: 0 orphans).

**Auth/Security/RBAC**

14. *How does login work?* — §5 trace, verbatim.
15. *Where are passwords?* — bcrypt hash only; verify via passlib constant-time.
16. *JWT contents?* — `sub`, `user_id`, `role`, `exp` (24h), HS256.
17. *Can the frontend be bypassed?* — yes, and that's fine: backend re-checks role on every request (66-assertion audit).
18. *What if account disabled mid-session?* — next request → 401 (per-request check).
19. *Known security gaps?* — dev SECRET_KEY fallback, no rate limiting/lockout/HTTPS/refresh — production TODO.

**Telemetry/Simulation/CSV**

20. *How is telemetry generated?* — AR(1) + I²R coupling + linear wear drift; seed-deterministic.
21. *Why AR(1)?* — temporal autocorrelation like real sensors.
22. *What does wear_start do?* — sample index where degradation+labels begin (default 30%).
23. *CSV rules?* — required cols+aliases, timestamps parseable, numeric, physical mins, all-or-nothing.
24. *CSV limitations?* — §8 list (inf passes, unknown anomaly text→False, no ranges/dups).
25. *Three sources?* — SIMULATED/UPLOADED/MANUAL, enum-enforced.

**ML / Isolation Forest**

26. *Why Isolation Forest?* — unsupervised, healthy-only training, effective on tabular anomalies.
27. *How does IF work?* — random splits; anomalies isolate in fewer partitions → low score.
28. *What is contamination?* — expected anomaly fraction (0.01) → threshold position. **(Report says 0.05 — code says 0.01; code is truth.)**
29. *Features?* — `[current, temperature]` only.
30. *Training data?* — 1000 healthy generated samples.
31. *Score meaning?* — `decision_function`; >0 healthy, <0 anomaly; magnitude=confidence.
32. *Stored flag vs prediction?* — label vs inference — never conflate.
33. *Where's the model?* — `backend/ml/saved_models/isolation_forest.pkl`, loaded once at import.
34. *Is it predictive maintenance?* — Early-warning anomaly detection enabling preventive inspection; **not** RUL/failure-time.
35. *Metrics?* — §11 honest script + no-retained-output answer.

**Frontend**

36. *How does routing work?* — session_state `current_page`+role in `app.py`; sidebar buttons rerun.
37. *How are charts drawn?* — Plotly `line_chart`/`gauge` components; anomaly markers from stored flag.
38. *What happens on each click?* — full script rerun; session_state persists.

**Testing/Validation**

39. *How did you test?* — §16 tiers: browser-verified flows, 66-assertion audit, DB integrity; `evaluate_model.py` exists.
40. *Coverage?* — DoD target unmet formally; honest answer per §15 note.
41. *RBAC proof?* — operator direct-API calls → 403 (audit).

**Limitations/Future**

42. *Biggest limitation?* — synthetic-only data; single failure mode; per-user scoping.
43. *Next steps?* — FlightSession, real ingestion, richer features, RUL, Postgres, explainability.
44. *Deploy to production?* — env secrets, Postgres, HTTPS, Docker, monitoring.

**Design decisions**

45. *Why operators see shared data but engineers own-user?* — operational feed semantics for operators (they fly "the" drone); engineer ownership keeps data provenance per analyst. FlightSession would unify it.
46. *Why deny admins telemetry?* — separation of duties; admins manage accounts, not operations.
47. *Why store the anomaly label AND predict?* — labels enable evaluation; prediction is operational verdict.
48. *Why disable instead of delete?* — preserve audit history (aviation maintenance).
49. *Why can't admins create admins?* — single-root-of-trust; prevents privilege escalation.
50. *Why 1 Hz in data vs 10 Hz sensor spec?* — simulator granularity choice; detection is unaffected — drift is slow.

---

# 19. MY PROJECT — MASTER UNDERSTANDING (memorize)

I built **AVIONAV**, a full-stack UAV propulsion-health prototype focused on the most dangerous progressive motor failure: **bearing wear**. It watches two physically-linked parameters — motor **current** and **temperature** (linked by Joule heating P=I²R) — because worn bearings raise friction → current → temperature.

It's three tiers: a **Streamlit** frontend with role-specific dashboards, a **FastAPI** REST backend under `/api/v1`, and **SQLite** persisted through **SQLAlchemy ORM** with **Alembic** migrations. Two tables: `user` and `telemetryreading` (FK owner). Everything a user sees comes over authenticated HTTP.

**Security:** login posts OAuth2 form credentials → bcrypt-verified → a signed **JWT** (sub/user_id/role, HS256, 24 h) → stored in Streamlit session → sent as Bearer on every call → backend decodes, re-loads the user (so disabled accounts die immediately), and checks the role per endpoint. Three roles: Administrator (user management only), Maintenance Engineer (full telemetry workflow), Drone Operator (shared read-only live feed, hard-capped at 50 readings). Frontend menus hide things for UX; the backend enforces — I proved it with a 66-assertion audit calling the API directly.

**Telemetry** enters three ways — a physics-inspired **simulator** (AR(1) current around 15 A, temperature thermally coupled at `42+0.045·I²`, and a wear scenario that drifts both signals linearly after a configurable start index — deterministic via seed), **CSV upload** (strict column/timestamp/numeric validation, all-or-nothing), and **JSON ingest**. Each row stores `timestamp, current, temperature, anomaly(ground-truth), source, user_id`.

**AI:** an **Isolation Forest** trained once, offline, on 1000 healthy synthetic samples with features `[current, temperature]`, `contamination=0.01`, `random_state=42`, saved by joblib and loaded at backend import. Inference is **on-demand**: `predict()` gives HEALTHY/ANOMALY, `decision_function()` gives the score. The prediction is never stored — the stored `anomaly` column is the generator's label, kept separate precisely so the model can be evaluated against ground truth. This is **anomaly detection**, not diagnosis, not RUL, not failure-time prediction.

**Dashboards:** the engineer sees status+recommendation, KPIs, gauges, trend charts with anomaly markers, an interactive predictor, simulation/CSV/AI-analysis tabs, history with date filtering and CSV export; the operator sees a minimal alert-focused view of the shared feed; the admin manages accounts.

**Validation:** every feature was exercised in the real browser; security was proven by direct API calls per role; database integrity was audited (counts, sources, zero orphans). What I **don't** claim: real-flight validation, independently reproduced metrics, or unit-test coverage — those are the honest edges of the prototype.

**Future:** FlightSession/AnomalyEvent tables (already sketched), real telemetry ingestion, vibration/current-spectrum features, explainability, RUL, Postgres, Docker.

---

# 20. DEFENSE CHEAT SHEET

**20 facts**
1. Two monitored params: current (A), temperature (°C) — linked by P=I²R
2. Failure focus: bearing wear — the only progressive BLDC failure mode
3. Three roles: Administrator / Maintenance Engineer / Drone Operator
4. JWT: HS256, claims `sub`,`user_id`,`role`,`exp`; 24 h (1440 min)
5. bcrypt via passlib; constant-time verify; passwords never stored
6. Disabled accounts rejected at login AND per-request
7. 401 = authn fail; 403 = wrong role
8. Two tables: `user`, `telemetryreading`; FK `user_id`; 3 Alembic revisions
9. Sources: SIMULATED / UPLOADED / MANUAL (DB enum constraint)
10. Generator: AR(1) (coef 0.92, mean 15 A) + `T=42+0.045·I²` smoothed; wear drift +0.08 A, +0.25 °C/sample; 1 s steps; seed-deterministic
11. wear_start default = 30% of samples
12. IF trained on 1000 healthy rows; features `[current,temperature]`; contamination 0.01; random_state 42; default 100 trees
13. Model file: `backend/ml/saved_models/isolation_forest.pkl`; joblib; loaded at import
14. predict→±1 maps to ANOMALY/HEALTHY; score=decision_function (sign=verdict)
15. Predictions computed per request, never stored; stored anomaly=ground-truth label
16. Operators: shared feed, limit≤50, skip=0, everything else 403
17. Engineers: own-user scope; admins: no detailed telemetry (403), stats OK
18. Admin account protected: no modify/disable/self-disable; admin role not assignable
19. No auto-refresh — Streamlit reruns on interaction
20. DB state at last audit: 11 users, ~940 readings, 0 orphans

**Numbers/config:** ports 8501/8000; prefix `/api/v1`; sim bounds samples 1–10000 (UI 10–1000); predict inputs `>0`; operator cap 50; healthy means 15 A/42 °C; thermal coef 0.045; clamps I∈[0,100], T∈[−273.15,200]; datasets 1000+300 rows.

**Main files:** `app.py`, `utils/{api,auth}.py`, `views/*`, `endpoints/{telemetry,users}.py`, `auth.py`, `dependencies.py`, `security.py`, `auth_service.py`, `telemetry_service.py`, `crud/*`, `models/*`, `schemas/*`, `telemetry_generator.py`, `ml/{train_model,anomaly_detector,evaluate_model}.py`, `database.py`, `alembic/versions/*`.

## CLAIMS I MUST NOT MAKE

- ✗ Physical UAV/sensor deployment or real flight-test validation
- ✗ Real-time sensor streaming or "live" push updates (it's per-render polling)
- ✗ Monitoring voltage / RPM / error counters / message frequency (only current+temperature)
- ✗ FlightSession or AnomalyEvent as implemented tables — **[DEFERRED]**
- ✗ `/api/flights` or `/api/anomalies` endpoints — they don't exist
- ✗ RUL, failure-time prediction, or fault diagnosis
- ✗ Explainability/feature-importance module (report mentions it; code doesn't)
- ✗ Anomaly "types" (spike/drift/intermittent taxonomy from spec) — binary IF only
- ✗ contamination=0.05 — code uses **0.01**
- ✗ Cross-validation of the model — not implemented
- ✗ Accuracy/precision/recall/F1 as proven fact — evaluate_model.py exists, **no retained output** → "[EVIDENCE LIMITATION]"
- ✗ "5-second dashboard refresh" (T4) — not implemented
- ✗ Unit tests / 80% coverage — no pytest suite retained
- ✗ Test env "Python 3.9 / Ubuntu" — actual: Python 3.12 / Windows
- ✗ Stored predictions — predictions are computed, not persisted
- ✗ Tests passed just because scripts exist — only claim what was actually executed

---

# 21. REPORT ↔ CODE DISCREPANCY MAP (defense-critical)

| # | Report says | Code implements | What to say |
|---|---|---|---|
| 1 | Abstract/spec: 5 parameters | 2 (current, temperature) | "Scope reduced with the industrial supervisor — documented in ch3" |
| 2 | Abstract: 3 anomaly types | binary HEALTHY/ANOMALY | "The wear scenario embodies the gradual-drift type; spike/intermittent taxonomy was design-phase" |
| 3 | FR-09/ch6: explainability, feature importance | none (score + fixed recommendation) | "Explainability was scoped to score+recommendation; feature attribution is future work" |
| 4 | ch6: contamination=0.05 | `0.01` | "Final tuning used 1% — conservative false-alarm rate" |
| 5 | ch6: "cross-validation" | single labeled eval in `evaluate_model.py` | "Evaluation is held-out-style on labeled synthetic data, not k-fold" |
| 6 | US-07/08/09: FlightSession/AnomalyEvent tables | only `user`+`telemetryreading` | "Flight grouping descoped; FK moved to user" |
| 7 | ch7/README: `/api/flights*`, `/api/anomalies` | `/api/v1/telemetry/*`, `/users/*` | "Consolidated into the telemetry resource; same coverage" |
| 8 | ch5: preprocessing (null removal, outlier filter, Min-Max, rolling avg) | validation/coercion only | "The pipeline validates and normalizes formats; statistical preprocessing was descoped" |
| 9 | FR-01: email+password login | **username**+password | "Username chosen; email stored but not the login key" |
| 10 | FR-06: "real-time streams" | on-demand inference | "Detection is per-request, which fits the polling dashboard" |
| 11 | FR-08/US-16: "send alert", severity panel | in-app alert cards only | "Alerts are visual in-app; notification channels are future work" |
| 12 | ch7/US-15: flight selector | date-range filter | "Without FlightSession, filtering is by time range" |
| 13 | ch8/annex: metrics P.92/R.88/F1.90, T3 0.5 s, 100×3600 dataset | `evaluate_model.py` exists; no retained output; datasets 1000+300 | "Script-generated on synthetic data; treat as indicative" |
| 14 | ch8: env Python 3.9, Ubuntu | Python 3.12, Windows venvs | "Documentation env vs dev env" |
| 15 | DoD: ≥80% unit coverage | no pytest suite | "DoD aspirational; validation was functional+audit-based" |
| 16 | ch4: 10 Hz sensing, ~10 A cruise | generator 1 s, 15 A baseline | "Sensing spec is hardware design; simulator uses 1 s granularity" |
| 17 | US-13: "anomalies stored in DB" | predictions not persisted | "Detection verdict is live; stored flag is ground truth" |
| 18 | Spec: React.js frontend | Streamlit | "Annex-A trade-off decision: Streamlit for a solo data-app build" |

---

# 22. SOURCE TRACEABILITY

| Concept | Source(s) | Proves |
|---|---|---|
| Login endpoint | `backend/api/v1/auth.py` | OAuth2 form → Token |
| bcrypt hash/verify | `backend/core/security.py:10,18,42` | salted adaptive hashing |
| JWT create/decode | `security.py:70,112` | claims+exp, HS256 |
| Claims content | `services/auth_service.py:72` | sub/user_id/role |
| Auth service | `auth_service.py:18` | lookup+verify+disabled |
| Per-request auth | `dependencies.py:13` | token→user→disabled |
| Role guards | `dependencies.py:85,115,140` | 403 enforcement |
| Operator limits | `endpoints/telemetry.py:54` | ≤50, skip=0 |
| Admin telemetry denial | `endpoints/telemetry.py:48,79` | 403 |
| User schema | `models/user.py` | roles, unique fields, disabled |
| Telemetry schema | `models/telemetry.py`, `base.py` | fields, FK, enum, indexes |
| Migrations | `alembic/versions/*` | 3-revision chain |
| DB engine/session | `database.py` | SQLite URL, get_db |
| Validation schemas | `schemas/telemetry.py`, `schemas/user.py` | request/response shapes, admin-role block |
| Simulation | `simulator/telemetry_generator.py` | AR(1), coupling, wear, seed |
| Service logic | `services/telemetry_service.py` | ingest/simulate/scope/predict |
| Persistence | `crud/telemetry.py:12`, `crud/user.py` | add_all+commit, hashing |
| IF training | `ml/train_model.py` | healthy-only, params, joblib |
| IF inference | `ml/anomaly_detector.py` | load-once, predict+score |
| IF evaluation | `ml/evaluate_model.py` | metrics script (no retained output) |
| Router/RBAC UX | `frontend/app.py`, `components/sidebar.py` | role pages/menus |
| Session/login FE | `utils/auth.py`, `utils/api.py` | token store, Bearer injection |
| Demo views | `views/telemetry.py`, `history.py`, dashboards | tabs, charts, alerts, export |
| Requirements | `chapters/chapter3*.tex` | FR/NFR, actors, sprints |
| Metrics claims | `chapters/chapter8*.tex`, `annexes/annexA` | reported numbers (unverified) |
| Deferred scope | `TESTING.md:229-241`, `models/user.py:60` | FlightSession/AnomalyEvent TODO |

---

# 23. CONFIDENCE MAP

**GREEN — verified from source/execution**
- Auth chain (bcrypt→JWT→deps→403/401), RBAC incl. operator caps & admin denial
- Full telemetry CRUD/simulate/upload/predict paths; DB persistence & scoping
- IF pipeline: train→pkl→load→predict→score→HEALTHY/ANOMALY
- Frontend routing, views, charts, export; browser-validated flows
- Schema/tables/migrations; zero orphans; source enum
- CSV validation behavior incl. its exact limits

**YELLOW — documented, limited evidence**
- Report metrics (P/R/F1, response time) — script exists, no retained output
- "Precision 92% / FPR 8%" — reproduce `evaluate_model.py` before quoting
- NFR-01 <2 s — plausible on localhost, unmeasured
- Dataset representativeness — synthetic only
- Python 3.9/Ubuntu test-env claim — actual env differs

**RED — conceptual / deferred / not implemented**
- FlightSession, AnomalyEvent tables; `/api/flights`, `/api/anomalies`
- Explainability/feature-importance; anomaly-type taxonomy detection
- Real-time push/5 s refresh; notification channels (email/SMS)
- RUL/failure-time/fault diagnosis; physical hardware integration
- Unit-test suite & coverage; rate limiting/lockout/HTTPS; production secrets

---

*Generated by cross-reading `backend/`, `frontend/`, `alembic/`, `datasets/`, `chapters/*.tex`, `annexes/*.tex`, `Technical_Specification.txt`, `README.md`, and `TESTING.md`. Where the report and code diverge, the code was treated as truth.*
