import pandas as pd
import numpy as np

print("=" * 50)
print("  PLAYLIST ARCHAEOLOGY: Clean & Merge")
print("=" * 50)

# Load datasets
tracks = pd.read_csv("data/raw/data.csv")
yearly = pd.read_csv("data/raw/data_by_year.csv")
genres = pd.read_csv("data/raw/data_by_genres.csv")
events = pd.read_csv("data/raw/world_events.csv")

print(f"\n  Tracks: {len(tracks)}")
print(f"  Yearly: {len(yearly)}")
print(f"  Genres: {len(genres)}")
print(f"  Events: {len(events)}")

# === CLEAN YEARLY DATA ===
# Add mood score (combination of valence + energy + danceability)
yearly["mood_score"] = (yearly["valence"] * 0.5 + yearly["energy"] * 0.3 + yearly["danceability"] * 0.2)

# Add decade column
yearly["decade"] = (yearly["year"] // 10) * 10
yearly["decade_label"] = yearly["decade"].astype(str) + "s"

# Calculate year-over-year changes
yearly = yearly.sort_values("year")
yearly["valence_change"] = yearly["valence"].pct_change() * 100
yearly["energy_change"] = yearly["energy"].pct_change() * 100
yearly["mood_change"] = yearly["mood_score"].pct_change() * 100

print(f"\n  Yearly data cleaned. Columns: {list(yearly.columns)}")

# === MERGE WITH EVENTS ===
# Mark event years
yearly["has_event"] = yearly["year"].isin(events["year"]).astype(int)

# Merge event details
merged = yearly.merge(events, on="year", how="left")
merged["event"] = merged["event"].fillna("No major event")
merged["category"] = merged["category"].fillna("none")
merged["severity"] = merged["severity"].fillna(0)

# Create event window (1 year before and after each event)
event_years = set(events["year"].tolist())
def get_event_period(year):
    if year in event_years:
        return "event_year"
    elif (year - 1) in event_years or (year + 1) in event_years:
        return "near_event"
    else:
        return "peaceful"

merged["event_period"] = merged["year"].apply(get_event_period)

print(f"\n  Merged dataset: {len(merged)} rows")
print(f"\n  Event periods:")
print(f"    {merged['event_period'].value_counts().to_dict()}")

# === CLEAN TRACKS DATA ===
tracks_clean = tracks[["name", "artists", "year", "valence", "energy",
                        "danceability", "acousticness", "tempo", "popularity",
                        "loudness", "speechiness", "instrumentalness"]].copy()
tracks_clean["decade"] = (tracks_clean["year"] // 10) * 10
tracks_clean["mood_score"] = (tracks_clean["valence"] * 0.5 + tracks_clean["energy"] * 0.3 + tracks_clean["danceability"] * 0.2)

# Add event info to tracks
tracks_merged = tracks_clean.merge(events, on="year", how="left")
tracks_merged["event"] = tracks_merged["event"].fillna("No major event")
tracks_merged["category"] = tracks_merged["category"].fillna("none")
tracks_merged["severity"] = tracks_merged["severity"].fillna(0)

print(f"  Tracks with events: {len(tracks_merged)}")

# === SAVE EVERYTHING ===
yearly.to_csv("data/processed/yearly_clean.csv", index=False)
merged.to_csv("data/processed/yearly_with_events.csv", index=False)
tracks_clean.to_csv("data/processed/tracks_clean.csv", index=False)
tracks_merged.to_csv("data/processed/tracks_with_events.csv", index=False)
events.to_csv("data/processed/events_clean.csv", index=False)
genres.to_csv("data/processed/genres_clean.csv", index=False)

print("\n  FILES SAVED:")
print("    data/processed/yearly_clean.csv")
print("    data/processed/yearly_with_events.csv")
print("    data/processed/tracks_clean.csv")
print("    data/processed/tracks_with_events.csv")
print("    data/processed/events_clean.csv")
print("    data/processed/genres_clean.csv")

# Quick insight preview
print("\n" + "=" * 50)
print("  QUICK INSIGHTS")
print("=" * 50)

print("\n  Average mood by decade:")
decade_mood = merged.groupby("decade_label")[["valence", "energy", "danceability", "mood_score"]].mean()
print(decade_mood.round(3).to_string())

print("\n  Mood during event years vs peaceful years:")
event_mood = merged.groupby("event_period")["mood_score"]