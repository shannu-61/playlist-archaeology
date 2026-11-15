import pandas as pd

print("=" * 50)
print("  PLAYLIST ARCHAEOLOGY: Data Exploration")
print("=" * 50)

# Load main dataset
df = pd.read_csv("data/raw/data.csv")
print(f"\n  Main dataset: {len(df)} tracks")
print(f"  Columns: {list(df.columns)}")
print(f"\n  Sample:\n{df.head()}")
print(f"\n  Year range: {df['year'].min()} to {df['year'].max()}")

# Load yearly data
yearly = pd.read_csv("data/raw/data_by_year.csv")
print(f"\n\n  Yearly dataset: {len(yearly)} years")
print(f"  Columns: {list(yearly.columns)}")
print(f"\n  Sample:\n{yearly.head()}")

# Key audio features we care about
print("\n\n  KEY AUDIO FEATURES (from yearly data):")
print("  " + "-" * 45)
for col in ["valence", "energy", "danceability", "acousticness", "tempo"]:
    if col in yearly.columns:
        print(f"    {col:20s} | min: {yearly[col].min():.3f} | max: {yearly[col].max():.3f}")

print("\n  DONE!")