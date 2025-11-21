"""Script to populate database with sample data for testing"""
from gov_analytics.db import SessionLocal
from gov_analytics import models
import random

# Sample Indian states
states = [
    ("MH", "Maharashtra"),
    ("UP", "Uttar Pradesh"),
    ("DL", "Delhi"),
    ("KA", "Karnataka"),
    ("TN", "Tamil Nadu"),
    ("GJ", "Gujarat"),
    ("RJ", "Rajasthan"),
    ("WB", "West Bengal"),
]

years = [2020, 2021, 2022, 2023, 2024]

db = SessionLocal()

print("Adding sample PMAY data...")
for state_code, state_name in states:
    for year in years:
        record = models.PMAY(
            state_code=state_code,
            state_name=state_name,
            year=year,
            beneficiaries=random.randint(10000, 100000),
            houses_completed=random.randint(5000, 80000),
            funds_released=random.uniform(100, 1000)
        )
        db.add(record)

print("Adding sample MNREGA data...")
for state_code, state_name in states:
    for year in years:
        record = models.MNREGA(
            state_code=state_code,
            state_name=state_name,
            year=year,
            person_days_generated=random.randint(100000, 1000000),
            job_cards=random.randint(50000, 500000),
            funds_spent=random.uniform(500, 5000)
        )
        db.add(record)

print("Adding sample Startup India data...")
for state_code, state_name in states:
    for year in years:
        record = models.StartupIndia(
            state_code=state_code,
            state_name=state_name,
            year=year,
            startups_supported=random.randint(100, 5000),
            funds_allocated=random.uniform(50, 500)
        )
        db.add(record)

print("Adding sample Saubhagya data...")
for state_code, state_name in states:
    for year in years:
        record = models.Saubhagya(
            state_code=state_code,
            state_name=state_name,
            year=year,
            households_electrified=random.randint(10000, 200000),
            percent_coverage=random.uniform(70, 99)
        )
        db.add(record)

db.commit()
db.close()

print("\n✅ Sample data added successfully!")
print("Now visit http://localhost:5000 to see the dashboard with data")
