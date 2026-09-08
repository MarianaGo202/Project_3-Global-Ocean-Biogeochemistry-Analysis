import sqlite3
from pathlib import Path
import pandas as pd

print("PROJECT 3 — CREATING SQLITE DATABASE")

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DATABASE_DIR = PROJECT_ROOT / "data" / "database"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATABASE_DIR / "ocean_biogeochemistry.db"

print()
print("Project root:")
print(PROJECT_ROOT)

print()
print("Processed data directory:")
print(PROCESSED_DIR)

print()
print("Database:")
print(DATABASE_FILE)


# Check that every required CSV exists before loading anything
print()
print("CHECKING PROCESSED FILES")

required_files = [
    "surface_biogeochemistry_2025_09.csv",
    "global_surface_statistics.csv",
    "latitude_surface_statistics.csv",
    "longitude_surface_statistics.csv",
    "global_depth_profiles.csv",
    "dim_variable.csv",
    "dim_depth.csv",
    "dim_date.csv",
]

for filename in required_files:
    file_path = PROCESSED_DIR / filename
    if file_path.exists():
        print(f"OK: {filename}")
    else:
        print(f"MISSING: {filename}")


# Create / open the database
print()
print("CREATING DATABASE")

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

print()
print("SQLite database created/opened successfully!")


# Main fact table: surface observations
surface_file = PROCESSED_DIR / "surface_biogeochemistry_2025_09.csv"

if surface_file.exists():
    print()
    print("Loading surface biogeochemistry data...")
    df_surface = pd.read_csv(surface_file)
    print(f"Rows: {len(df_surface):,}")
    print(f"Columns: {len(df_surface.columns)}")
    df_surface.to_sql(
        "surface_biogeochemistry",
        connection,
        if_exists="replace",
        index=False
    )
    print("Table created: surface_biogeochemistry")


# Statistics tables (global, latitude, longitude, depth)
global_file = PROCESSED_DIR / "global_surface_statistics.csv"

if global_file.exists():
    df_global = pd.read_csv(global_file)
    df_global.to_sql(
        "global_surface_statistics",
        connection,
        if_exists="replace",
        index=False
    )
    print("Table created: global_surface_statistics")

latitude_file = PROCESSED_DIR / "latitude_surface_statistics.csv"

if latitude_file.exists():
    df_latitude = pd.read_csv(latitude_file)
    df_latitude.to_sql(
        "latitude_surface_statistics",
        connection,
        if_exists="replace",
        index=False
    )
    print("Table created: latitude_surface_statistics")

longitude_file = PROCESSED_DIR / "longitude_surface_statistics.csv"

if longitude_file.exists():
    df_longitude = pd.read_csv(longitude_file)
    df_longitude.to_sql(
        "longitude_surface_statistics",
        connection,
        if_exists="replace",
        index=False
    )
    print("Table created: longitude_surface_statistics")

depth_file = PROCESSED_DIR / "global_depth_profiles.csv"

if depth_file.exists():
    df_depth = pd.read_csv(depth_file)
    df_depth.to_sql(
        "global_depth_profiles",
        connection,
        if_exists="replace",
        index=False
    )
    print("Table created: global_depth_profiles")


# Dimension tables (variable, depth, date)
dimension_files = {
    "dim_variable.csv": "dim_variable",
    "dim_depth.csv": "dim_depth",
    "dim_date.csv": "dim_date",
}

for filename, table_name in dimension_files.items():
    file_path = PROCESSED_DIR / filename
    if file_path.exists():
        df = pd.read_csv(file_path)
        df.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )
        print(f"Table created: {table_name}")


# Indexes on the most commonly filtered columns
print()
print("CREATING INDEXES")

indexes = [

    """
    CREATE INDEX IF NOT EXISTS idx_surface_latitude
    ON surface_biogeochemistry(latitude)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_surface_longitude
    ON surface_biogeochemistry(longitude)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_surface_date
    ON surface_biogeochemistry(date)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_surface_year
    ON surface_biogeochemistry(year)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_surface_month
    ON surface_biogeochemistry(month)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_depth_depth
    ON global_depth_profiles(depth)
    """,

]

for index_sql in indexes:
    try:
        cursor.execute(index_sql)
    except sqlite3.OperationalError as error:

        print("Index warning:")
        print(error)

connection.commit()


# List final tables and database size
print()
print("DATABASE TABLES")

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
    """
)

tables = cursor.fetchall()

for table in tables:
    print(f"- {table[0]}")

connection.close()

database_size_mb = DATABASE_FILE.stat().st_size / (1024 ** 2)

print()
print("DATABASE SUMMARY")

print(f"Database file: {DATABASE_FILE}")
print(f"Database size: {database_size_mb:.2f} MB")

print()
print("STEP 09 COMPLETE")
