import pandas as pd
import os

print("\n" + "=" * 50)
print("  Exporting Data for Tableau")
print("=" * 50)

os.makedirs("data/tableau", exist_ok=True)

yearly = pd.read_csv("data/processed/yearly_with_events.csv")
events = pd.read_csv("data/processed/events_clean.csv")
yearly_full = yearly.merge(events, on="year", how="left", suffixes=("", "_event"))
yearly_full["event_name"] = yearly_full["event"].fillna("No Major Event")
yearly_full["has_event"] = yearly_full["event"].notna().astype(int)

def get_era(year):
    if year < 1940:
        return "Pre-War (1920-1939)"
    elif year < 1950:
        return "WWII Era (1940-1949)"
    elif year < 1960:
        return "Post-War (1950-1959)"
    elif year < 1970:
        return "Counterculture (1960-1969)"
    elif year < 1980:
        return "Disco & Funk (1970-1979)"
    elif year < 1990:
        return "Pop & MTV (1980-1989)"
    elif year < 2000:
        return "Grunge & Hip-Hop (1990-1999)"
    elif year < 2010:
        return "Digital Age (2000-2009)"
    else:
        return "Streaming Era (2010-2020)"

yearly_full["era"] = yearly_full["year"].apply(get_era)
yearly_full.to_csv("data/tableau/yearly_mood_events.csv", index=False)
print(f"  1. yearly_mood_events.csv: {len(yearly_full)} rows")

tracks = pd.read_csv("data/processed/tracks_with_events.csv")
tracks_sample = tracks.sample(min(20000, len(tracks)), random_state=42)
tracks_sample.to_csv("data/tableau/tracks_sample.csv", index=False)
print(f"  2. tracks_sample.csv: {len(tracks_sample)} rows")

genres = pd.read_csv("data/processed/genres_clean.csv")
genres["mood_score"] = genres["valence"] * 0.5 + genres["energy"] * 0.3 + genres["danceability"] * 0.2
genres_top = genres.nlargest(50, "count") if "count" in genres.columns else genres.head(50)
genres_top.to_csv("data/tableau/genres_top50.csv", index=False)
print(f"  3. genres_top50.csv: {len(genres_top)} genres")

events_ref = events.copy()
events_ref["event_label"] = events_ref["event"] + " (" + events_ref["year"].astype(str) + ")"
events_ref.to_csv("data/tableau/events_reference.csv", index=False)
print(f"  4. events_reference.csv: {len(events_ref)} events")

decade_summary = yearly.groupby("decade").agg({"valence": "mean", "energy": "mean", "danceability": "mean", "acousticness": "mean", "tempo": "mean", "mood_score": "mean"}).round(3).reset_index()
decade_summary["decade_label"] = decade_summary["decade"].astype(str) + "s"
decade_summary.to_csv("data/tableau/decade_summary.csv", index=False)
print(f"  5. decade_summary.csv: {len(decade_summary)} decades")

print("\n  All files saved to data/tableau/")
print("=" * 50)