import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import warnings
warnings.filterwarnings("ignore")

sns.set_style("whitegrid")

def load_data():
    yearly = pd.read_csv("data/processed/yearly_with_events.csv")
    tracks = pd.read_csv("data/processed/tracks_with_events.csv")
    events = pd.read_csv("data/processed/events_clean.csv")
    return yearly, tracks, events

def analysis_1_mood_timeline(yearly, events):
    print("\n" + "=" * 50)
    print("  ANALYSIS 1: 100 Years of Music Mood")
    print("=" * 50)

    fig, axes = plt.subplots(3, 1, figsize=(18, 14), sharex=True)

    # Plot 1: Valence (happiness) over time
    axes[0].plot(yearly["year"], yearly["valence"], color="#3498db", linewidth=2, label="Valence (Happiness)")
    axes[0].fill_between(yearly["year"], yearly["valence"], alpha=0.3, color="#3498db")
    for _, e in events.iterrows():
        if e["severity"] >= 5:
            axes[0].axvline(x=e["year"], color="red", alpha=0.4, linestyle="--")
            axes[0].text(e["year"], axes[0].get_ylim()[1] * 0.95, e["event"],
                        rotation=45, fontsize=6, ha="left", va="top")
    axes[0].set_ylabel("Valence (Happiness)", fontsize=11)
    axes[0].set_title("100 Years of Music Mood vs World Events", fontsize=15, fontweight="bold")
    axes[0].legend()

    # Plot 2: Energy over time
    axes[1].plot(yearly["year"], yearly["energy"], color="#e74c3c", linewidth=2, label="Energy")
    axes[1].fill_between(yearly["year"], yearly["energy"], alpha=0.3, color="#e74c3c")
    for _, e in events.iterrows():
        if e["severity"] >= 5:
            axes[1].axvline(x=e["year"], color="red", alpha=0.4, linestyle="--")
    axes[1].set_ylabel("Energy", fontsize=11)
    axes[1].legend()

    # Plot 3: Danceability over time
    axes[2].plot(yearly["year"], yearly["danceability"], color="#2ecc71", linewidth=2, label="Danceability")
    axes[2].fill_between(yearly["year"], yearly["danceability"], alpha=0.3, color="#2ecc71")
    for _, e in events.iterrows():
        if e["severity"] >= 5:
            axes[2].axvline(x=e["year"], color="red", alpha=0.4, linestyle="--")
    axes[2].set_ylabel("Danceability", fontsize=11)
    axes[2].set_xlabel("Year", fontsize=11)
    axes[2].legend()

    plt.tight_layout()
    plt.savefig("data/processed/mood_timeline.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved: mood_timeline.png")

def analysis_2_event_impact(yearly, events):
    print("\n" + "=" * 50)
    print("  ANALYSIS 2: Do World Events Change Music Mood?")
    print("=" * 50)

    # Compare event years vs peaceful years
    event_data = yearly[yearly["event_period"] == "event_year"]
    peaceful_data = yearly[yearly["event_period"] == "peaceful"]

    print(f"\n  Event years: {len(event_data)} | Peaceful years: {len(peaceful_data)}")

    for feature in ["valence", "energy", "danceability", "mood_score"]:
        event_mean = event_data[feature].mean()
        peaceful_mean = peaceful_data[feature].mean()
        t_stat, p_value = stats.ttest_ind(event_data[feature], peaceful_data[feature])
        diff_pct = ((event_mean - peaceful_mean) / peaceful_mean) * 100
        sig = "SIGNIFICANT" if p_value < 0.05 else "Not significant"
        print(f"\n    {feature:15s}")
        print(f"      Event years:   {event_mean:.4f}")
        print(f"      Peaceful years: {peaceful_mean:.4f}")
        print(f"      Difference:    {diff_pct:+.2f}%")
        print(f"      p-value:       {p_value:.6f} | {sig}")

    # Compare by event category
    print("\n\n  Mood by Event Category:")
    print("  " + "-" * 50)
    cat_mood = yearly.merge(events, on="year", how="inner").groupby("category_y")["valence"].mean().sort_values()
    for cat, val in cat_mood.items():
        bar = "x" * int(val * 50)
        print(f"    {cat:15s}: {val:.4f} {bar}")

    # Visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Plot 1: Event vs Peaceful comparison
    comparison = yearly.groupby("event_period")[["valence", "energy", "danceability"]].mean()
    comparison.plot(kind="bar", ax=axes[0], colormap="Set2")
    axes[0].set_title("Music Features: Event vs Peaceful Years", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Score")
    axes[0].tick_params(axis="x", rotation=45)

    # Plot 2: Mood by event category
    if len(cat_mood) > 0:
        colors = ["#e74c3c" if v < 0.52 else "#f39c12" if v < 0.55 else "#2ecc71" for v in cat_mood.values]
        axes[1].barh(cat_mood.index, cat_mood.values, color=colors)
        axes[1].set_title("Valence by Event Type", fontsize=12, fontweight="bold")
        axes[1].set_xlabel("Avg Valence (Happiness)")

    # Plot 3: Before vs After major events
    major_events = events[events["severity"] >= 5]
    before_after = []
    for _, e in major_events.iterrows():
        yr = e["year"]
        before = yearly[yearly["year"] == yr - 1]["valence"].values
        during = yearly[yearly["year"] == yr]["valence"].values
        after = yearly[yearly["year"] == yr + 1]["valence"].values
        if len(before) > 0 and len(during) > 0 and len(after) > 0:
            before_after.append({
                "event": e["event"][:20],
                "before": before[0],
                "during": during[0],
                "after": after[0]
            })
    ba_df = pd.DataFrame(before_after)
    if len(ba_df) > 0:
        x = range(len(ba_df))
        axes[2].plot(ba_df["event"], ba_df["before"], "go-", label="Year Before", markersize=8)
        axes[2].plot(ba_df["event"], ba_df["during"], "ro-", label="Event Year", markersize=8)
        axes[2].plot(ba_df["event"], ba_df["after"], "bo-", label="Year After", markersize=8)
        axes[2].set_title("Valence: Before/During/After Events", fontsize=12, fontweight="bold")
        axes[2].tick_params(axis="x", rotation=90)
        axes[2].legend(fontsize=8)
        axes[2].set_ylabel("Valence")

    plt.tight_layout()
    plt.savefig("data/processed/event_impact.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("\n  Saved: event_impact.png")

def analysis_3_decade_trends(yearly):
    print("\n" + "=" * 50)
    print("  ANALYSIS 3: Decade-by-Decade Trends")
    print("=" * 50)

    decade_stats = yearly.groupby("decade").agg({
        "valence": "mean",
        "energy": "mean",
        "danceability": "mean",
        "acousticness": "mean",
        "tempo": "mean",
        "mood_score": "mean"
    }).round(3)
    print(f"\n{decade_stats.to_string()}")

    # Trend correlation (is music getting sadder over time?)
    corr, p_val = stats.pearsonr(yearly["year"], yearly["valence"])
    print(f"\n  Year vs Valence correlation: r={corr:.3f}, p={p_val:.6f}")
    if corr < 0:
        print("  >>> Music IS getting sadder over time!")
    else:
        print("  >>> Music is getting happier over time!")

    corr2, p_val2 = stats.pearsonr(yearly["year"], yearly["energy"])
    print(f"  Year vs Energy correlation:  r={corr2:.3f}, p={p_val2:.6f}")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Decade radar-style comparison
    decades = decade_stats.index.tolist()
    decade_labels = [f"{d}s" for d in decades]
    features = ["valence", "energy", "danceability"]
    for feat in features:
        axes[0].plot(decade_labels, decade_stats[feat], marker="o", label=feat, linewidth=2)
    axes[0].set_title("Music Features by Decade", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Score")
    axes[0].legend()
    axes[0].tick_params(axis="x", rotation=45)

    # Acousticness vs Energy shift
    axes[1].scatter(decade_stats["acousticness"], decade_stats["energy"],
                    s=200, c=decades, cmap="viridis", zorder=5)
    for i, d in enumerate(decade_labels):
        axes[1].annotate(d, (decade_stats["acousticness"].iloc[i], decade_stats["energy"].iloc[i]),
                        fontsize=9, ha="center", va="bottom")
    axes[1].set_xlabel("Acousticness", fontsize=11)
    axes[1].set_ylabel("Energy", fontsize=11)
    axes[1].set_title("Music Evolution: Acoustic -> Electronic", fontsize=13, fontweight="bold")

    plt.tight_layout()
    plt.savefig("data/processed/decade_trends.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved: decade_trends.png")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  PLAYLIST ARCHAEOLOGY: Full Analysis")
    print("  100 Years of Music vs World Events")
    print("=" * 50)

    yearly, tracks, events = load_data()

    analysis_1_mood_timeline(yearly, events)
    analysis_2_event_impact(yearly, events)
    analysis_3_decade_trends(yearly)

    print("\n" + "=" * 50)
    print("  ALL ANALYSIS COMPLETE!")
    print("=" * 50)