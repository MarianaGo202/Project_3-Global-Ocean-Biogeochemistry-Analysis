import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# NOTE: this must match the file created by create_database.py
DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "database"
    / "ocean_biogeochemistry.db"
)

OUTPUT_DIR = PROJECT_ROOT / "powerbi" / "data"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print("PROJECT 3 — POWER BI EXPORT")

print("\nChecking database...")

if not DATABASE_FILE.exists():
    raise FileNotFoundError(
        f"\nDatabase not found:\n{DATABASE_FILE}"
    )

print("Database found successfully!")
print(f"Location: {DATABASE_FILE}")

connection = sqlite3.connect(DATABASE_FILE)

# Table names below match the tables actually created in 09_criar_banco.py 
# (surface_biogeochemistry, etc.), not the earlier "fact_*" naming
queries = {

    "global_statistics.csv": """
        SELECT *
        FROM global_surface_statistics
        ORDER BY variable;
    """,

    "surface_biogeochemistry.csv": """
        SELECT *
        FROM surface_biogeochemistry;
    """,

    "latitude_statistics.csv": """
        SELECT *
        FROM latitude_surface_statistics
        ORDER BY variable, latitude;
    """,

    "longitude_statistics.csv": """
        SELECT *
        FROM longitude_surface_statistics
        ORDER BY variable, longitude;
    """,

    # Depth data: global_depth_profiles is the only depth table
    # actually loaded into the database (depth_statistics.csv from
    # create_aggregations.py duplicates this data and was never
    # loaded as a table, so it is not exported here)
    "depth_profiles.csv": """
        SELECT *
        FROM global_depth_profiles
        ORDER BY variable, depth;
    """

}

print("EXPORTING TABLES")

for filename, query in queries.items():
    print(f"\nExporting {filename}...")
    df = pd.read_sql_query(
        query,
        connection
    )
    df.to_csv(
        OUTPUT_DIR / filename,
        index=False
    )
    print(f"Rows: {len(df):,}")

connection.close()

print("POWER BI EXPORT COMPLETE")
