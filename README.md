<<<<<<< HEAD
# AI Interview Evaluation & Feedback System

An NLP/Transformer-based mock interview platform that evaluates candidate
answers on relevance, semantic similarity, concept coverage, completeness,
and grammar — and generates personalized, evaluation-grounded feedback.

> **Build status:** Phase 1 (Backend + Database + Authentication) complete
> and tested. See [Roadmap](#roadmap) below — this README will grow with
> each phase.

## 1. Features (target — see roadmap for current status)

- JWT-based authentication with bcrypt password hashing
- Technical & HR interview modes, ~10 questions per session
- Weighted, configurable evaluation engine (relevance / semantic / concept
  coverage / completeness / grammar)
- Sentence-BERT semantic similarity (`all-MiniLM-L6-v2`)
- TF-IDF baseline and BiLSTM model for comparison
- Concept coverage via semantic (not just keyword) matching
- Rubric-based completeness scoring
- Personalized, evaluation-grounded feedback (strengths / weaknesses / suggestions)
- Adaptive difficulty based on score thresholds
- Human-vs-AI evaluation comparison (MAE, RMSE, Pearson, Spearman)
- Results dashboard with charts, interview history, exportable report

## 2. Architecture

```
frontend (React/Vite/TS/Tailwind)
        │  REST + JWT
        ▼
backend (FastAPI)
        │
        ├── api/          route handlers
        ├── evaluation/    orchestrator + 5 scoring modules
        ├── nlp/           tokenization, keyword extraction, grammar
        ├── ml/            TF-IDF baseline, BiLSTM
        ├── services/      interview-flow / adaptive-difficulty logic
        ├── models/        SQLAlchemy ORM
        └── database/      engine/session
        │
        ▼
PostgreSQL
```

## 3. Technology Stack

| Layer | Tech |
|---|---|
| Frontend | React, Vite, TypeScript, Tailwind CSS, Recharts |
| Backend | Python, FastAPI, Uvicorn |
| NLP | NLTK, spaCy, scikit-learn |
| Deep Learning | PyTorch, BiLSTM |
| Transformers | Hugging Face Transformers, Sentence-Transformers (SBERT) |
| Database | PostgreSQL + SQLAlchemy |
| Auth | JWT (python-jose) + bcrypt (passlib) |

## 4. Folder Structure

```
ai-interview-system/
├── frontend/
│   └── src/{components,pages,services,types}
├── backend/
│   ├── app/
│   │   ├── api/            # routers: auth.py (done), questions/interviews/dashboard (upcoming)
│   │   ├── core/config.py  # settings incl. evaluation weights, loaded from env
│   │   ├── models/         # SQLAlchemy models: User, Question, QuestionConcept,
│   │   │                   #   Interview, Answer, HumanEvaluation
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── services/       # business logic (interview flow, adaptive difficulty) — upcoming
│   │   ├── nlp/            # upcoming
│   │   ├── ml/             # upcoming
│   │   ├── evaluation/     # upcoming
│   │   ├── database/       # engine + session
│   │   ├── utils/security.py  # password hashing + JWT
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── data/{questions,datasets,sample}
├── models/
├── docker-compose.yml       # upcoming (Phase 12)
├── .env.example
└── README.md
```

## 5. Installation & Running Locally (Phase 1)

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ running locally (or Docker, once Phase 12 lands)

### Steps

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# from the project root:
cp .env.example .env
# edit .env: set DATABASE_URL to your local Postgres, and a real JWT_SECRET_KEY

# create the database (adjust user/db name to match your .env)
createdb interview_db

# run the API (tables auto-created on startup for dev)
uvicorn app.main:app --reload --app-dir backend
```

The API will be live at `http://localhost:8000`, interactive docs at
`http://localhost:8000/docs`.

### Environment Variables

See `.env.example` for the full list: `DATABASE_URL`, `JWT_SECRET_KEY`,
`JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `SBERT_MODEL_NAME`,
`EVAL_WEIGHT_*` (must sum to 1.0 — validated at startup), adaptive
difficulty thresholds, and `CORS_ORIGINS`.

## 6. API Reference (implemented so far)

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | — | Create account, returns JWT + user |
| POST | `/api/auth/login` | — | Login, returns JWT + user |
| GET | `/api/auth/me` | Bearer | Current user profile |
| GET | `/api/health` | — | Health check |

Full spec for questions/interviews/dashboard endpoints is in the project
plan and will be implemented in Phases 2–3.

## 7. Testing

```bash
cd backend
pip install -r requirements.txt
JWT_SECRET_KEY=testsecret python -m pytest tests/ -v
```

Tests use an in-memory SQLite database (via fixture overrides), so no
Postgres instance is required to run them. Current coverage: registration,
duplicate-email rejection, login success/failure, protected-route auth
enforcement, health check (7/7 passing).

## 8. Roadmap

- [x] **Phase 1** — Backend + database + authentication
- [ ] Phase 2 — Question bank + interview session
- [ ] Phase 3 — Basic evaluation engine
- [ ] Phase 4 — TF-IDF baseline
- [ ] Phase 5 — BiLSTM
- [ ] Phase 6 — Sentence-BERT semantic evaluation
- [ ] Phase 7 — Concept coverage + completeness
- [ ] Phase 8 — Feedback generation
- [ ] Phase 9 — Frontend dashboard
- [ ] Phase 10 — Model comparison
- [ ] Phase 11 — Testing (expanded)
- [ ] Phase 12 — Docker + deployment
- [ ] Phase 13 — Optional voice/CV features

## 9. Academic Notes

This is an NLP course project. The evaluation pipeline is built from
first principles (TF-IDF → BiLSTM → Sentence-BERT/BERT, cosine
similarity, concept extraction, classification/regression metrics) —
it does not outsource evaluation to a black-box external LLM API. Any
external API use is restricted to optional natural-language feedback
phrasing, not the core scoring logic. Sample/seed data used during
development is clearly distinguished from real evaluation results;
no experimental accuracy/F1/MAE numbers are fabricated — they will be
computed from actual runs once the relevant module is implemented.
=======
# AI-Interview-Preparation-Evaluation-Platform
>>>>>>> c9d7868f5fd64366d42109df41b7092cfca5a2cd
