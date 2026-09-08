import sqlite3
from pathlib import Path

print("PROJECT 3 — DATABASE VALIDATION")

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "database"
    / "ocean_biogeochemistry.db"
)

print("\nChecking database...")

if not DATABASE_FILE.exists():
    raise FileNotFoundError(
        f"\nDatabase not found:\n{DATABASE_FILE}"
    )

print("Database found successfully!")
print(f"Location: {DATABASE_FILE}")

print("OPENING DATABASE")

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

print("Database opened successfully!")

database_size_mb = DATABASE_FILE.stat().st_size / (1024 ** 2)

print("\nDatabase size:")
print(f"{database_size_mb:.2f} MB")


# List all tables and compare against the expected schema
print("DATABASE TABLES")

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
""")

tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    print(f"- {table}")

print(f"\nTotal tables: {len(tables)}")

expected_tables = [
    "surface_biogeochemistry",
    "global_surface_statistics",
    "latitude_surface_statistics",
    "longitude_surface_statistics",
    "global_depth_profiles",
    "dim_variable",
    "dim_depth",
    "dim_date"
]

print("TABLE VALIDATION")

for table in expected_tables:

    if table in tables:
        print(f"PASS — {table}")
    else:
        print(f"FAIL — {table}")


# Row counts per table
print("ROW COUNTS")

for table in expected_tables:

    if table not in tables:
        continue

    cursor.execute(
        f'SELECT COUNT(*) FROM "{table}";'
    )

    count = cursor.fetchone()[0]

    print(f"{table:35} {count:,}")


# Structure of the main fact table
main_table = "surface_biogeochemistry"

print("MAIN TABLE STRUCTURE")

cursor.execute(
    f'PRAGMA table_info("{main_table}");'
)

columns = cursor.fetchall()

for column in columns:

    column_id = column[0]
    column_name = column[1]
    data_type = column[2]

    print(
        f"{column_id:2} | "
        f"{column_name:25} | "
        f"{data_type}"
    )

column_names = [column[1] for column in columns]

print("\nColumns detected:")
print(", ".join(column_names))


# Confirm every biogeochemical variable made it into the table
required_variables = [
    "spco2",
    "chl",
    "fe",
    "no3",
    "nppv",
    "o2",
    "ph",
    "phyc",
    "po4",
    "si"
]

print("BIOGEOCHEMICAL VARIABLE VALIDATION")

for variable in required_variables:

    if variable in column_names:
        print(f"PASS — {variable}")
    else:
        print(f"FAIL — {variable}")


# Null-value check per variable
print("NULL VALUE ANALYSIS")

cursor.execute(
    f'SELECT COUNT(*) FROM "{main_table}";'
)

total_rows = cursor.fetchone()[0]

print(f"Total rows: {total_rows:,}")

for column in required_variables:
    if column not in column_names:
        continue
    cursor.execute(
        f'''
        SELECT COUNT(*)
        FROM "{main_table}"
        WHERE "{column}" IS NULL;
        '''
    )
    null_count = cursor.fetchone()[0]
    percentage = (
        null_count / total_rows * 100
        if total_rows > 0
        else 0
    )
    print(
        f"{column:10} "
        f"NULL: {null_count:10,} "
        f"({percentage:6.2f}%)"
    )

# ------------------------------------------------------------
# Geographic range sanity check
print("GEOGRAPHIC VALIDATION")

if "latitude" in column_names:
    cursor.execute(
        f'''
        SELECT
            MIN(latitude),
            MAX(latitude)
        FROM "{main_table}";
        '''
    )
    min_lat, max_lat = cursor.fetchone()
    print(f"Latitude range: {min_lat:.2f}° to {max_lat:.2f}°")

if "longitude" in column_names:
    cursor.execute(
        f'''
        SELECT
            MIN(longitude),
            MAX(longitude)
        FROM "{main_table}";
        '''
    )
    min_lon, max_lon = cursor.fetchone()
    print(f"Longitude range: {min_lon:.2f}° to {max_lon:.2f}°")


# Date range sanity check
print("DATE VALIDATION")

date_column = None

possible_date_columns = ["date", "datetime", "time"]

for candidate in possible_date_columns:
    if candidate in column_names:
        date_column = candidate
        break
if date_column:
    cursor.execute(
        f'''
        SELECT
            MIN("{date_column}"),
            MAX("{date_column}")
        FROM "{main_table}";
        '''
    )
    min_date, max_date = cursor.fetchone()
    print(f"Date column: {date_column}")
    print(f"Minimum date: {min_date}")
    print(f"Maximum date: {max_date}")
else:
    print("No date column found in main table.")


# Value ranges for each biogeochemical variable
print("BIOGEOCHEMICAL RANGES")

for variable in required_variables:
    if variable not in column_names:
        continue
    cursor.execute(
        f'''
        SELECT
            MIN("{variable}"),
            MAX("{variable}"),
            AVG("{variable}")
        FROM "{main_table}"
        WHERE "{variable}" IS NOT NULL;
        '''
    )
    minimum, maximum, average = cursor.fetchone()
    print(f"\n{variable.upper()}")
    print(f"  Minimum: {minimum}")
    print(f"  Maximum: {maximum}")
    print(f"  Mean:    {average}")


# A handful of sample rows for a visual sanity check
print("SAMPLE RECORDS")

cursor.execute(
    f'''
    SELECT *
    FROM "{main_table}"
    LIMIT 5;
    '''
)

sample_rows = cursor.fetchall()

for row in sample_rows:
    print(row)


# SQLite's built-in integrity check
print("DATABASE INTEGRITY CHECK")

cursor.execute("PRAGMA integrity_check;")

integrity_result = cursor.fetchone()[0]

print(f"Integrity check: {integrity_result}")

if integrity_result == "ok":
    print("PASS — SQLite database integrity is OK.")
else:
    print("WARNING — Database integrity check returned:")
    print(integrity_result)

connection.close()

print("\n" + "=" * 70)
print("DATABASE VALIDATION COMPLETE")
print("=" * 70)

print("\nDatabase validation finished successfully!")
