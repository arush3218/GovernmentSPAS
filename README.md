# Government Scheme Performance Analytics System

Track and visualize the performance of major Indian government schemes (PMAY, MNREGA, Startup India, Saubhagya) using official data.gov.in APIs.

## Screenshots

### Dashboard Overview
![Overview](screenshots/Screenshot%202025-11-21%20133753.png)

### Scheme Analytics
![Scheme Analytics](screenshots/Screenshot%202025-11-21%20141029.png)

### State Comparison
![State Comparison](screenshots/Screenshot%202025-11-21%20141044.png)

### Trends Analysis
![Trends](screenshots/Screenshot%202025-11-21%20141059.png)

### Admin Panel
![Admin](screenshots/Screenshot%202025-11-21%20141119.png)

### CSV Export
![Export](screenshots/Screenshot%202025-11-21%20141125.png)

## Features

✅ Flask web dashboard with Plotly charts  
✅ ETL pipeline with Prefect  
✅ SQLite/PostgreSQL storage  
✅ Admin panel for ETL triggers  
✅ CSV export functionality  
✅ Sample data generator

## Quick Start

```powershell
# 1. Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Configure (copy .env.example to .env and edit)
Copy-Item .env.example .env
# Edit .env: set DATABASE_URL=sqlite:///./gov_analytics.db

# 3. Initialize database
python -m scripts.init_db

# 4. Add sample data (optional - for testing)
python scripts\add_sample_data.py

# 5. Run Flask app
$env:FLASK_APP='gov_analytics.web'
flask run
```

**Open browser:** http://localhost:5000

## Using Real Data

1. Get API key from https://data.gov.in
2. Find resource IDs from data.gov.in datasets
3. Use Admin panel or run:
```powershell
python -m gov_analytics.prefect_flows --scheme pmay --resource-id YOUR_ID
```

## Tech Stack

Python 3.10+ • Flask • SQLAlchemy • Prefect • Plotly • Pydantic

## Contributing

Pull requests welcome! Please open an issue first to discuss changes.

