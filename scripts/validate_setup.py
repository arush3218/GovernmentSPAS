"""Quick validation script to check project setup"""
import sys
from pathlib import Path

print("=== Validating Project Setup ===\n")

errors = []
warnings = []

# Check Python version
if sys.version_info < (3, 10):
    warnings.append(f"Python 3.10+ recommended, you have {sys.version_info.major}.{sys.version_info.minor}")

# Check required files
required_files = [
    "requirements.txt",
    ".env.example",
    "gov_analytics/__init__.py",
    "gov_analytics/config.py",
    "gov_analytics/db.py",
    "gov_analytics/models.py",
    "gov_analytics/schemas.py",
    "gov_analytics/web.py",
    "gov_analytics/prefect_flows.py",
    "gov_analytics/etl/extract.py",
    "gov_analytics/etl/transform.py",
    "gov_analytics/etl/load.py",
    "dashboard/templates/base.html",
    "dashboard/templates/overview.html",
    "dashboard/static/css/style.css",
]

for file in required_files:
    if not Path(file).exists():
        errors.append(f"Missing required file: {file}")

# Check .env
if not Path(".env").exists():
    warnings.append(".env file not found (copy from .env.example)")

# Try imports
print("Checking imports...")
try:
    from gov_analytics import config
    print("✓ config module")
except ImportError as e:
    errors.append(f"Cannot import config: {e}")

try:
    from gov_analytics import models
    print("✓ models module")
except ImportError as e:
    errors.append(f"Cannot import models: {e}")

try:
    from gov_analytics import schemas
    print("✓ schemas module")
except ImportError as e:
    errors.append(f"Cannot import schemas: {e}")

try:
    from gov_analytics.etl import extract, transform, load
    print("✓ ETL modules")
except ImportError as e:
    errors.append(f"Cannot import ETL modules: {e}")

try:
    from gov_analytics import web
    print("✓ web module")
except ImportError as e:
    errors.append(f"Cannot import web: {e}")

print("\n=== Validation Results ===\n")

if errors:
    print("ERRORS:")
    for err in errors:
        print(f"  ❌ {err}")
    print()

if warnings:
    print("WARNINGS:")
    for warn in warnings:
        print(f"  ⚠️  {warn}")
    print()

if not errors:
    print("✅ All checks passed! Project is ready.")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure")
    print("2. Run: python -m scripts.init_db")
    print("3. Run: $env:FLASK_APP='gov_analytics.web'; flask run")
    sys.exit(0)
else:
    print("❌ Validation failed. Fix errors above.")
    sys.exit(1)
