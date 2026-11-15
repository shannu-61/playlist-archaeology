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
    genres = pd.read_csv("data/processed/genres_clean.csv")
    return yearly, tracks, events, genres

def analysis_4_genre_mood(genres):
    print("\n" + "=" * 50)
    print("  ANALYSIS 4: Genre Mood Map")
    print("=" * 50)

    # Top 20 genres by track count
    top_genres = genres.nlargest(20, "count") if "count" in genres.columns else genres.head(20)

    print("\n  Top 20 Genres by Mood Score:")
    print("  " + "-" * 50)

    if "valence" in genres.columns and "energy" in genres.columns and "danceability" in genres.columns:
        genres["mood_score"] = genres["valence"] * 0.5 + genres["energy"] * 0.3 + genres["danceability"] * 0.2
        top_by_mood = genres.nlargest(10, "mood_score")
        bottom_by_mood = genres.nsmallest(10, "mood_score")

        print("\n  HAPPIEST Genres:")
        for _, g in top_by_mood.iterrows():
            name = g.get("genres", g.get("genre", "unknown"))
            print(f"    {str(name):30s} mood={g['mood_score']:.3f} val={g['valence']:.3f} energy={g['energy']:.3f}")

        print("\n  SADDEST Genres:")
        for _, g in bottom_by_mood.iterrows():
            name = g.get("genres", g.get("genre", "unknown"))
            print(f"    {str(name):30s} mood={g['mood_score']:.3f} val={g['valence']:.3f} energy={g['energy']:.3f}")

        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))

        # Happiest genres
        happy_names = [str(g.get("genres", g.get("genre", "")))[:25] for _, g in top_by_mood.iterrows()]
        axes[0].barh(happy_names, top_by_mood["mood_score"], color="#2ecc71")
        axes[0].set_title("Top 10 HAPPIEST Genres", fontsize=13, fontweight="bold")
        axes[0].set_xlabel("Mood Score")
        axes[0].invert_yaxis()

        # Saddest genres
        sad_names = [str(g.get("genres", g.get("genre", "")))[:25] for _, g in bottom_by_mood.iterrows()]
        axes[1].barh(sad_names, bottom_by_mood["mood_score"], color="#e74c3c")
        axes[1].set_title("Top 10 SADDEST Genres", fontsize=13, fontweight="bold")
        axes[1].set_xlabel("Mood Score")
        axes[1].invert_yaxis()

        plt.tight_layout()
        plt.savefig("data/processed/genre_mood.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("\n  Saved: genre_mood.png")
    else:
        print("  Genre data missing valence/energy columns")

def analysis_5_war_vs_recession(yearly, events):
    print("\n" + "=" * 50)
    print("  ANALYSIS 5: Wars vs Recessions - Music Response")
    print("=" * 50)

    wars = events[events["category"] == "war"]
    economic = events[events["category"] == "economic"]

    war_years = yearly[yearly["year"].isin(wars["year"])]
    econ_years = yearly[yearly["year"].isin(economic["year"])]
    peaceful = yearly[yearly["event_period"] == "peaceful"]

    print(f"\n  War years ({len(war_years)}): avg valence = {war_years['valence'].mean():.4f}, energy = {war_years['energy'].mean():.4f}")
    print(f"  Recession years ({len(econ_years)}): avg valence = {econ_years['valence'].mean():.4f}, energy = {econ_years['energy'].mean():.4f}")
    print(f"  Peaceful years ({len(peaceful)}): avg valence = {peaceful['valence'].mean():.4f}, energy = {peaceful['energy'].mean():.4f}")

    # T-tests
    for feat in ["valence", "energy", "mood_score"]:
        t1, p1 = stats.ttest_ind(war_years[feat], peaceful[feat])
        t2, p2 = stats.ttest_ind(econ_years[feat], peaceful[feat])
        print(f"\n  {feat}:")
        print(f"    War vs Peaceful:      p={p1:.4f} {'SIGNIFICANT' if p1 < 0.05 else 'not sig'}")
        print(f"    Recession vs Peaceful: p={p2:.4f} {'SIGNIFICANT' if p2 < 0.05 else 'not sig'}")

    # Major event deep dives
    print("\n\n  DEEP DIVE: Before/During/After Major Events")
    print("  " + "-" * 50)
    major = events[events["severity"] >= 4].sort_values("year")

    deep_dive_data = []
    for _, e in major.iterrows():
        yr = e["year"]
        before = yearly[yearly["year"].between(yr - 3, yr - 1)]["valence"].mean()
        during = yearly[yearly["year"] == yr]["valence"].values
        after = yearly[yearly["year"].between(yr + 1, yr + 3)]["valence"].mean()
        if len(during) > 0 and not np.isnan(before) and not np.isnan(after):
            during_val = during[0]
            recovery = after - during_val
            print(f"    {e['event']:35s} ({yr}): before={before:.3f} during={during_val:.3f} after={after:.3f} recovery={recovery:+.3f}")
            deep_dive_data.append({
                "event": e["event"][:20], "year": yr,
                "before": before, "during": during_val, "after": after
            })

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    # War vs Recession comparison
    categories = ["War Years", "Recession Years", "Peaceful Years"]
    valence_vals = [war_years["valence"].mean(), econ_years["valence"].mean(), peaceful["valence"].mean()]
    energy_vals = [war_years["energy"].mean(), econ_years["energy"].mean(), peaceful["energy"].mean()]

    x = np.arange(len(categories))
    width = 0.35
    axes[0].bar(x - width/2, valence_vals, width, label="Valence", color="#3498db")
    axes[0].bar(x + width/2, energy_vals, width, label="Energy", color="#e74c3c")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(categories)
    axes[0].set_title("Wars vs Recessions vs Peace", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Score")
    axes[0].legend()

    # Recovery timeline
    if len(deep_dive_data) > 0:
        dd = pd.DataFrame(deep_dive_data)
        for i, row in dd.iterrows():
            axes[1].plot(["Before", "During", "After"], [row["before"], row["during"], row["after"]],
                        "o-", label=row["event"], linewidth=2, markersize=6)
        axes[1].set_title("Valence Recovery After Major Events", fontsize=13, fontweight="bold")
        axes[1].set_ylabel("Valence (Happiness)")
        axes[1].legend(fontsize=7, loc="best")

    plt.tight_layout()
    plt.savefig("data/processed/war_vs_recession.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("\n  Saved: war_vs_recession.png")

def analysis_6_popularity_vs_mood(tracks):
    print("\n" + "=" * 50)
    print("  ANALYSIS 6: Do Sad Songs Get More Popular?")
    print("=" * 50)

    if "popularity" in tracks.columns:
        corr, p_val = stats.pearsonr(tracks["valence"], tracks["popularity"])
        print(f"\n  Valence vs Popularity: r={corr:.3f}, p={p_val:.6f}")
        if corr < 0:
            print("  >>> SAD songs ARE more popular!")
        else:
            print("  >>> HAPPY songs are more popular!")

        corr2, p2 = stats.pearsonr(tracks["energy"], tracks["popularity"])
        print(f"  Energy vs Popularity:  r={corr2:.3f}, p={p2:.6f}")

        corr3, p3 = stats.pearsonr(tracks["danceability"], tracks["popularity"])
        print(f"  Dance vs Popularity:   r={corr3:.3f}, p={p3:.6f}")

        # By decade
        print("\n  Popularity-Mood Correlation by Decade:")
        for decade in sorted(tracks["decade"].unique()):
            dec_data = tracks[tracks["decade"] == decade]
            if len(dec_data) > 10:
                r, p = stats.pearsonr(dec_data["valence"], dec_data["popularity"])
                direction = "sad wins" if r < 0 else "happy wins"
                sig = "*" if p < 0.05 else ""
                print(f"    {decade}s: r={r:.3f} ({direction}) {sig}")

        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Scatter: valence vs popularity
        sample = tracks.sample(min(5000, len(tracks)), random_state=42)
        axes[0].scatter(sample["valence"], sample["popularity"], alpha=0.1, s=5, color="#3498db")
        z = np.polyfit(sample["valence"], sample["popularity"], 1)
        p_line = np.poly1d(z)
        x_line = np.linspace(0, 1, 100)
        axes[0].plot(x_line, p_line(x_line), "r-", linewidth=2, label=f"r={corr:.3f}")
        axes[0].set_xlabel("Valence (Happiness)")
        axes[0].set_ylabel("Popularity")
        axes[0].set_title("Do Sad Songs Get More Popular?", fontsize=13, fontweight="bold")
        axes[0].legend()

        # Decade trend of popularity-mood correlation
        decade_corrs = []
        for decade in sorted(tracks["decade"].unique()):
            dec_data = tracks[tracks["decade"] == decade]
            if len(dec_data) > 10:
                r, _ = stats.pearsonr(dec_data["valence"], dec_data["popularity"])
                decade_corrs.append({"decade": f"{decade}s", "correlation": r})
        dc_df = pd.DataFrame(decade_corrs)
        colors = ["#e74c3c" if v < 0 else "#2ecc71" for v in dc_df["correlation"]]
        axes[1].bar(dc_df["decade"], dc_df["correlation"], color=colors)
        axes[1].axhline(y=0, color="black", linewidth=0.5)
        axes[1].set_title("Valence-Popularity Correlation by Decade", fontsize=13, fontweight="bold")
        axes[1].set_ylabel("Correlation (negative = sad wins)")
        axes[1].tick_params(axis="x", rotation=45)

        plt.tight_layout()
        plt.savefig("data/processed/popularity_vs_mood.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("\n  Saved: popularity_vs_mood.png")
    else:
        print("  No popularity column found")

def analysis_7_correlation_heatmap(yearly):
    print("\n" + "=" * 50)
    print("  ANALYSIS 7: Feature Correlation Heatmap")
    print("=" * 50)

    features = ["valence", "energy", "danceability", "acousticness",
                "instrumentalness", "liveness", "speechiness", "tempo", "loudness"]
    available = [f for f in features if f in yearly.columns]

    corr_matrix = yearly[available].corr()
    print(f"\n  Strongest correlations:")
    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            r = corr_matrix.iloc[i, j]
            if abs(r) > 0.5:
                print(f"    {available[i]:20s} vs {available[j]:20s}: r={r:.3f}")

    fig, ax = plt.subplots(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f",
                cmap="RdBu_r", center=0, square=True,
                linewidths=0.5, ax=ax, vmin=-1, vmax=1)
    ax.set_title("Audio Feature Correlations (Yearly Averages)", fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.savefig("data/processed/correlation_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved: correlation_heatmap.png")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  PLAYLIST ARCHAEOLOGY: Deep Analysis")
    print("  Week 3 - Genre, Wars, Popularity & Correlations")
    print("=" * 50)

    yearly, tracks, events, genres = load_data()

    analysis_4_genre_mood(genres)
    analysis_5_war_vs_recession(yearly, events)
    analysis_6_popularity_vs_mood(tracks)
    analysis_7_correlation_heatmap(yearly)

    print("\n" + "=" * 50)
    print("  DEEP ANALYSIS COMPLETE!")
    print(f"  Charts saved: genre_mood.png, war_vs_recession.png,")
    print(f"  popularity_vs_mood.png, correlation_heatmap.png")
    print("=" * 50)