# Government Scheme Performance Analytics System

A complete data analytics platform that tracks and visualizes the performance of major Indian government schemes using official data.gov.in APIs.

## Features

- **Automated ETL Pipeline**: Prefect-orchestrated data ingestion from data.gov.in
- **Data Validation**: Strict Pydantic schemas for data quality
- **PostgreSQL Storage**: SQLAlchemy models for persistent storage
- **Flask Web Dashboard**: Interactive visualizations with Plotly
- **CSV Export**: Download cleaned datasets
- **Admin Panel**: Trigger ETL runs via web interface
- **DVC Integration**: Dataset versioning support

## Tracked Schemes

- **PMAY** (Pradhan Mantri Awas Yojana): Housing for all
- **MNREGA**: Rural employment guarantee
- **Startup India**: Startup funding and support
- **Saubhagya**: Rural electrification

## Tech Stack

- Python 3.10+
- Flask (Web Framework)
- PostgreSQL + SQLAlchemy
- Prefect (ETL Orchestration)
- Plotly (Visualizations)
- Pydantic (Data Validation)
- DVC (Data Versioning)

## Quick Start

### 1. Install Dependencies

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/gov_analytics
DATA_GOV_API_KEY=your_api_key_from_data_gov_in
ETL_TRIGGER_SECRET=your_secret_token_here
```

### 3. Initialize Database

```powershell
python -m scripts.init_db
```

### 4. Run ETL Pipeline

#### Option A: Single Scheme
```powershell
python -m gov_analytics.prefect_flows --scheme pmay --resource-id <RESOURCE_ID>
```

#### Option B: Full Pipeline with Config
Create `etl_config.json`:
```json
{
  "pmay": "your-pmay-resource-id",
  "mnrega": "your-mnrega-resource-id",
  "startup_india": "your-startup-resource-id",
  "saubhagya": "your-saubhagya-resource-id"
}
```

Then run:
```powershell
python -m gov_analytics.prefect_flows --config-file etl_config.json
```

### 5. Start Web Dashboard

```powershell
$env:FLASK_APP='gov_analytics.web'
$env:FLASK_ENV='development'
flask run --host=0.0.0.0 --port=5000
```

Visit: http://localhost:5000

## Dashboard Pages

- **Overview**: High-level KPIs across all schemes
- **Scheme Analytics**: Detailed breakdown by scheme with filters
- **State Comparison**: Choropleth maps showing state-level performance
- **Trends**: Time series analysis and YoY comparisons
- **Admin**: Trigger ETL runs and export CSV files

## Project Structure

```
GOV_DATA/
├── gov_analytics/           # Main package
│   ├── config.py           # Pydantic settings
│   ├── db.py              # SQLAlchemy setup
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic validation schemas
│   ├── validation.py      # Validation helpers
│   ├── kpis.py           # KPI calculation functions
│   ├── prefect_flows.py  # Prefect ETL orchestration
│   ├── web.py            # Flask application
│   └── etl/              # ETL modules
│       ├── extract.py    # Data extraction
│       ├── transform.py  # Data transformation
│       └── load.py       # Data loading
├── dashboard/            # Web frontend
│   ├── templates/       # Jinja2 templates
│   └── static/         # CSS and assets
├── scripts/            # Utility scripts
│   └── init_db.py     # Database initialization
├── data/              # Data storage (DVC tracked)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

---
