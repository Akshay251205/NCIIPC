# SAT-SA --- Supervisory Analytics Tool for SOC Assessment

> **Security Analytics & Threat Assessment Platform for supervisory
> assessment of Security Operations Centres (SOCs).**

SAT-SA is a security analytics platform designed to help supervisors
assess the effectiveness and operational quality of SOC activities from
structured evidence such as alerts, analysts, investigations, incidents,
assets, evidence review, escalation behaviour, and peer benchmarks.

Instead of acting as another SIEM or real-time SOC monitoring system,
SAT-SA works as a **supervisory analytics layer** that converts
operational evidence into explainable findings, risk indicators, and
actionable supervisory insights.

### Core workflow

``` text
SOC Data
   ↓
Data Validation & Ingestion
   ↓
Analytics & Behavioural Analysis
   ↓
Findings & Evidence
   ↓
Risk Fusion
   ↓
Supervisory Decision Support
```

------------------------------------------------------------------------

## 🎯 Project Objectives

SAT-SA aims to:

-   Analyse SOC operational data at scale.
-   Identify unusual or risky analyst and alert behaviour.
-   Detect investigation and evidence-review gaps.
-   Analyse alert workload, severity, status, closure time and
    escalation patterns.
-   Compare performance against peer benchmarks.
-   Detect negative-space indicators from available asset and alert
    evidence.
-   Produce explainable findings backed by measurable evidence.
-   Combine multiple risk signals into a unified risk assessment.
-   Provide a dashboard and API for supervisory analysis.

------------------------------------------------------------------------

## ✨ Key Features

### 1. Alert Intelligence

The analytics layer evaluates:

-   Alert workload
-   Alert severity
-   Alert status
-   Closure time
-   Evidence-review rate
-   Escalation behaviour
-   False-positive behaviour
-   Overall alert metrics

### 2. Analyst Intelligence

SAT-SA analyses individual analyst behaviour using:

-   Workload distribution
-   Average closure time
-   Evidence-review rate
-   Escalation rate
-   Investigation count
-   Investigation duration
-   Behavioural anomaly indicators
-   Suspicious activity indicators
-   Analyst risk scoring
-   Analyst metric distributions

### 3. Investigation & NLP Analysis

Investigation records can be analysed to identify patterns in
investigation quality and behaviour and support evidence-based
supervisory findings.

### 4. Peer Benchmarking

Analytical results can be compared with peer benchmark data to identify
significant deviations from expected operational behaviour.

### 5. Negative-Space Analysis

SAT-SA uses available asset and alert relationships to identify
situations where expected security activity may be missing or
insufficiently represented in the available evidence.

### 6. Risk Fusion

Multiple analytical signals can be combined into an overall risk
assessment:

``` text
Alert Risk
    +
Analyst Risk
    +
Investigation Risk
    +
Asset Risk
    +
Negative-Space Risk
    +
Peer Benchmark Deviation
    ↓
Overall Risk
```

### 7. Explainable Findings

Findings are intended to retain supporting indicators and evidence so
that a supervisor can understand **why** an entity or analyst was
flagged.

### 8. REST API

The backend exposes analytics through FastAPI endpoints for consumption
by the frontend.

Example intelligence endpoints include:

``` text
GET /intelligence/summary
GET /intelligence/findings
GET /intelligence/analysts/{analyst_id}/profile
GET /api/v1/analysts?page=&limit=&status=
GET /api/v1/analysts/{id}
```

------------------------------------------------------------------------

## 🏗️ Architecture

``` text
                  ┌─────────────────────────┐
                  │      SOC Evidence       │
                  │ CSV / Structured Data   │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Data Validation &       │
                  │ Ingestion Layer         │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ PostgreSQL Database     │
                  │ SQLAlchemy + Alembic   │
                  └────────────┬────────────┘
                               │
                               ▼
             ┌──────────────────────────────────┐
             │        Analytics Engine           │
             │                                  │
             │ Alert Intelligence               │
             │ Analyst Intelligence             │
             │ Behavioural Analysis             │
             │ Investigation/NLP Analysis       │
             │ Peer Benchmarking                │
             │ Negative-Space Analysis          │
             └────────────────┬─────────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ Unified Findings &      │
                  │ Risk Fusion              │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │       FastAPI API       │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ React + Vite Frontend   │
                  │ Supervisory Dashboard   │
                  └─────────────────────────┘
```

------------------------------------------------------------------------

## 🧰 Technology Stack

### Backend

-   Python
-   FastAPI
-   SQLAlchemy
-   Alembic
-   PostgreSQL
-   Pandas
-   Pydantic
-   Uvicorn

### Frontend

-   React
-   TypeScript
-   Vite
-   React Router
-   Recharts
-   Lucide React

### Data & Analytics

-   CSV-based structured datasets
-   PostgreSQL relational storage
-   Statistical and rule-based analytics
-   Behavioural analysis
-   Risk scoring and risk fusion
-   Investigation text analysis

### Testing & Development

-   Pytest
-   ESLint
-   Git
-   GitHub
-   VS Code

------------------------------------------------------------------------

## 📁 Project Structure

``` text
NCIIPC/
│
├── agents/                         # Agent/AI-related modules
│
├── backend/                        # FastAPI backend
│   ├── ...
│   └── ...
│
├── frontend/                       # React + Vite frontend
│   ├── src/
│   ├── package.json
│   └── ...
│
├── data/                           # Project datasets
│
├── docs/                           # Technical documentation
│
├── tests/                          # Automated tests
│
├── .env.example                    # Environment variable template
├── .gitignore
├── FRONTEND_API_INTEGRATION.md
├── Project_Progress.md
└── README.md
```

------------------------------------------------------------------------

## 📊 Dataset

The current project contains eight synthetic datasets:

``` text
organizations.csv
analysts.csv
assets.csv
alerts.csv
incidents.csv
investigations.csv
asset_activity.csv
peer_benchmarks.csv
```

The project progress documentation records:

``` text
8 datasets
×
25,000 rows each
=
200,000 total rows
```

The data pipeline includes validation for:

-   Row counts
-   Required columns
-   Data types
-   Foreign-key relationships
-   Cross-file relationships

------------------------------------------------------------------------

## 🗄️ Database

SAT-SA uses **PostgreSQL** as the primary relational database.

Database functionality includes:

-   Database schema
-   Relational tables
-   Foreign-key relationships
-   SQLAlchemy ORM
-   Alembic migrations
-   CSV-to-database ingestion
-   Database reset functionality
-   Connection verification

> Do not commit your real `.env` file or database password to GitHub.
> Use `.env.example` as the configuration template.

------------------------------------------------------------------------

## 🚀 Getting Started

### Prerequisites

Install the following before running the project:

-   Python 3.11+
-   Node.js and npm
-   PostgreSQL
-   Git

------------------------------------------------------------------------

## 1. Clone the Repository

``` bash
git clone https://github.com/Akshay251205/NCIIPC.git
cd NCIIPC
```

------------------------------------------------------------------------

## 2. Backend Setup

Open a terminal in the project root and create a Python virtual
environment:

### Windows

``` powershell
python -m venv .venv
```

Activate it:

``` powershell
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

``` bash
pip install -r backend/requirements.txt
```

If your repository uses a different backend dependency file, use the
requirements file provided inside `backend/`.

------------------------------------------------------------------------

## 3. Configure Environment Variables

Create your local environment file from the example:

``` text
.env.example
```

Copy it to:

``` text
.env
```

Then configure the PostgreSQL connection and other local settings
required by the backend.

**Never commit `.env` to GitHub.**

------------------------------------------------------------------------

## 4. PostgreSQL Setup

Create a PostgreSQL database for local development.

Then configure the database connection in your `.env` according to the
variables expected by the backend.

Run the project's database migrations using the Alembic configuration
provided by the backend.

Typical Alembic commands are:

``` bash
alembic upgrade head
```

> Use the project's configured Alembic working directory if your local
> setup requires running the command from `backend/`.

------------------------------------------------------------------------

## 5. Load the Dataset

The repository contains the project's synthetic data and ingestion
pipeline.

Use the data-loading/ingestion script available in the backend to
populate PostgreSQL.

After ingestion, verify that the expected tables and records are
present.

The current project documentation reports successful ingestion of
approximately:

``` text
200,000 rows
```

------------------------------------------------------------------------

## 6. Start the Backend

Start the FastAPI development server using the project's configured
entry point.

A typical FastAPI development command is:

``` bash
uvicorn <module>:app --reload --port 8000
```

After the backend starts, FastAPI documentation is normally available
at:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

## 7. Start the Frontend

Open a second terminal:

``` bash
cd frontend
npm install
npm run dev
```

Vite will display the local frontend URL in the terminal.

The frontend uses:

``` text
VITE_API_BASE_URL
```

for the backend API base URL. The documented default is:

``` text
http://127.0.0.1:8000
```

------------------------------------------------------------------------

## 🧪 Testing

Run the backend test suite using the project's configured test setup.

Typical command:

``` bash
pytest
```

The current project progress documentation records:

``` text
206 tests passed
```

and a full 25,000-analyst pipeline benchmark of approximately:

``` text
4.11 seconds
```

These figures refer to the project's current synthetic/local benchmark
and should not be interpreted as production performance guarantees.

------------------------------------------------------------------------

## 📈 Current Development Status

### Completed

-   [x] Project structure
-   [x] Requirements definition
-   [x] Database design
-   [x] PostgreSQL setup
-   [x] Alembic setup
-   [x] Synthetic CSV generation
-   [x] CSV validation
-   [x] Database ingestion
-   [x] Alert analytics
-   [x] Analyst analytics
-   [x] Analyst distributions
-   [x] Behavioural analysis
-   [x] Gaming detection
-   [x] Investigation NLP layer
-   [x] Peer benchmarking
-   [x] Negative-space integration
-   [x] Risk fusion
-   [x] Analyst trust profile API
-   [x] Automated testing

### Current / Future Work

-   [ ] Authentication
-   [ ] Role-Based Access Control (RBAC)
-   [ ] External notification delivery
-   [ ] Additional ML anomaly detection
-   [ ] Agentic AI capabilities
-   [ ] Report generation
-   [ ] Production deployment
-   [ ] Final documentation

------------------------------------------------------------------------

## 🔐 Security & Privacy

SAT-SA is intended as a supervisory analytics prototype and should be
deployed according to the security requirements of its target
environment.

Important practices:

-   Do not commit API keys.
-   Do not commit database passwords.
-   Do not commit private credentials.
-   Keep `.env` outside version control.
-   Use synthetic or appropriately sanitised datasets for public
    repositories.
-   Review generated reports before sharing sensitive information.

The current backend documentation describes the API as intended for a
trusted local/demo deployment; authentication, RBAC, and external
notification delivery are not currently part of the implemented backend
architecture.

------------------------------------------------------------------------

## 🎯 Design Philosophy

SAT-SA is designed around the principle:

> **Operational evidence → measurable analysis → explainable findings →
> risk → supervisory action**

The system is intended to assist supervisors rather than replace human
judgement.

The goal is not simply to show more SOC metrics, but to help identify:

-   Where operational processes may be weakening
-   Which analysts or activities require attention
-   Which findings have supporting evidence
-   Where expected security activity may be missing
-   How multiple signals contribute to overall risk

------------------------------------------------------------------------

## 📚 Documentation

Additional project documentation is available in:

-   `Project_Progress.md` --- development status and implementation
    progress
-   `FRONTEND_API_INTEGRATION.md` --- frontend/API integration details
-   `docs/` --- technical documentation
-   `backend/` --- backend implementation
-   `frontend/` --- dashboard implementation
-   `tests/` --- automated tests

------------------------------------------------------------------------

## 👨‍💻 Project

**SAT-SA --- Supervisory Analytics Tool for SOC Assessment**

Repository:

https://github.com/Akshay251205/NCIIPC

Developed as a cybersecurity and security analytics project focused on
supervisory assessment of SOC operations.

------------------------------------------------------------------------

## ⚠️ Disclaimer

SAT-SA is a prototype/research-oriented supervisory analytics platform.
The included datasets are synthetic and the system should not be
considered a production SOC, SIEM, national monitoring platform, or
replacement for professional security assessment.
