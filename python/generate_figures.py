import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "database"
    / "ocean_biogeochemistry.db"
)

FIGURES_DIR = PROJECT_ROOT / "figures" / "analysis"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("PROJECT 3 — GENERATING FIGURES")

connection = sqlite3.connect(DATABASE_FILE)

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 11,
})


# Figure 1 — Dissolved oxygen depth profile
print("\nFigure 1: oxygen depth profile...")

df_o2 = pd.read_sql_query(
    """
    SELECT depth, mean_value AS oxygen
    FROM global_depth_profiles
    WHERE variable = 'o2'
    ORDER BY depth;
    """,
    connection
)

fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(df_o2["oxygen"], df_o2["depth"], color="#1f77b4", linewidth=2)
ax.invert_yaxis()
ax.set_xlabel("Dissolved oxygen (mmol m-3)")
ax.set_ylabel("Depth (m)")
ax.set_title("Dissolved Oxygen Profile with Depth")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "01_oxygen_depth_profile.png", dpi=150)
plt.close(fig)


# Figure 2 — Chlorophyll and primary production by latitude
print("Figure 2: chlorophyll and NPP by latitude...")

df_chl = pd.read_sql_query(
    """
    SELECT latitude, mean_value AS chlorophyll
    FROM latitude_surface_statistics
    WHERE variable = 'chl'
    ORDER BY latitude;
    """,
    connection
)

df_nppv = pd.read_sql_query(
    """
    SELECT latitude, mean_value AS nppv
    FROM latitude_surface_statistics
    WHERE variable = 'nppv'
    ORDER BY latitude;
    """,
    connection
)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

ax1.plot(df_chl["latitude"], df_chl["chlorophyll"], color="#2ca02c")
ax1.set_ylabel("Chlorophyll (mg m-3)")
ax1.set_title("Surface Chlorophyll by Latitude")

ax2.plot(df_nppv["latitude"], df_nppv["nppv"], color="#d62728")
ax2.set_ylabel("Net Primary Production (mg m-3 day-1)")
ax2.set_xlabel("Latitude (°)")
ax2.set_title("Net Primary Production by Latitude")

fig.tight_layout()
fig.savefig(FIGURES_DIR / "02_chlorophyll_nppv_by_latitude.png", dpi=150)
plt.close(fig)


# Figure 3 — Coefficient of variation per variable
print("Figure 3: variability ranking...")

df_var = pd.read_sql_query(
    """
    SELECT
        variable,
        std / NULLIF(mean, 0) AS coefficient_variation
    FROM global_surface_statistics
    ORDER BY coefficient_variation DESC;
    """,
    connection
)

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df_var["variable"], df_var["coefficient_variation"], color="#9467bd")
ax.invert_yaxis()
ax.set_xlabel("Coefficient of variation (std / mean)")
ax.set_title("Variability Ranking of Biogeochemical Variables")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "03_variability_ranking.png", dpi=150)
plt.close(fig)


# Figure 4 — Productivity classification
print("Figure 4: productivity classification...")

df_prod = pd.read_sql_query(
    """
    SELECT
        CASE
            WHEN chl >= (SELECT AVG(chl) FROM surface_biogeochemistry)
             AND nppv >= (SELECT AVG(nppv) FROM surface_biogeochemistry)
                THEN 'High Productivity'
            WHEN chl < (SELECT AVG(chl) FROM surface_biogeochemistry)
             AND nppv < (SELECT AVG(nppv) FROM surface_biogeochemistry)
                THEN 'Low Productivity'
            ELSE 'Intermediate Productivity'
        END AS productivity_class,
        COUNT(*) AS observations
    FROM surface_biogeochemistry
    GROUP BY productivity_class
    ORDER BY observations DESC;
    """,
    connection
)

fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#fffb00", "#71ff5b", "#00fbff"]
ax.bar(df_prod["productivity_class"], df_prod["observations"], color=colors)
ax.set_ylabel("Number of observations")
ax.set_title("Ocean Surface Productivity Classification")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "04_productivity_classification.png", dpi=150)
plt.close(fig)


# Figure 5 — Global surface map of chlorophyll
print("Figure 5: global chlorophyll map...")

df_map = pd.read_sql_query(
    """
    SELECT latitude, longitude, chl
    FROM surface_biogeochemistry;
    """,
    connection
)

fig, ax = plt.subplots(figsize=(11, 6))
scatter = ax.scatter(
    df_map["longitude"],
    df_map["latitude"],
    c=df_map["chl"],
    cmap="viridis",
    s=2,
    vmax=df_map["chl"].quantile(0.95)
)
ax.set_xlabel("Longitude (°)")
ax.set_ylabel("Latitude (°)")
ax.set_title("Global Surface Chlorophyll Concentration")
fig.colorbar(scatter, ax=ax, label="Chlorophyll (mg m-3)")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "05_global_chlorophyll_map.png", dpi=150)
plt.close(fig)

connection.close()

print("FIGURES SAVED TO:")
print(FIGURES_DIR)

for figure in sorted(FIGURES_DIR.glob("*.png")):
    print(f" - {figure.name}")

print("STEP 12 COMPLETE")
