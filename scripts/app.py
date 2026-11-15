import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Playlist Archaeology", page_icon="🎵", layout="wide")

# Load data
@st.cache_data
def load_data():
    yearly = pd.read_csv("data/processed/yearly_with_events.csv")
    tracks = pd.read_csv("data/processed/tracks_with_events.csv")
    events = pd.read_csv("data/processed/events_clean.csv")
    genres = pd.read_csv("data/processed/genres_clean.csv")
    genres["mood_score"] = genres["valence"] * 0.5 + genres["energy"] * 0.3 + genres["danceability"] * 0.2
    return yearly, tracks, events, genres

yearly, tracks, events, genres = load_data()

# Sidebar
st.sidebar.title("🎵 Playlist Archaeology")
st.sidebar.markdown("*How do world events shape the music we listen to?*")

page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "📈 Mood Timeline",
    "💥 Event Impact",
    "🎸 Genre Explorer",
    "🔬 Deep Analysis"
])

# KPI Cards
def show_kpis():
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Years Analyzed", "100", "1921-2020")
    col2.metric("🎵 Tracks", f"{len(tracks):,}")
    col3.metric("🎸 Genres", f"{len(genres):,}")
    col4.metric("💥 World Events", f"{len(events)}")

# PAGE 1: Overview
if page == "🏠 Overview":
    st.title("🎵 Playlist Archaeology")
    st.markdown("### How World Events Shape the Music We Listen To")
    st.markdown("---")
    show_kpis()

    st.markdown("### Key Findings")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🔍 Music IS getting sadder over time**
        - Valence correlation with year: r=-0.195 (p=0.051)
        - Peak happiness: 1970s (valence=0.585)
        - Lowest: 2010s (valence=0.456)

        **⚡ Events make music MORE energetic**
        - Event years energy: 0.488 vs peaceful: 0.391
        - Statistically significant (p=0.022)
        """)
    with col2:
        st.markdown("""
        **😢 Pandemics create the saddest music**
        - Pandemic mood: 0.501 (lowest category)
        - Wars: 0.521 | Economic crises: 0.585

        **🔄 2020s flipped the script**
        - First decade where sad songs are MORE popular
        - Valence-popularity correlation: r=-0.092
        """)

    # Quick mood timeline
    fig = px.line(yearly, x="year", y="mood_score", title="100 Years of Music Mood",
                  labels={"year": "Year", "mood_score": "Mood Score"})
    fig.update_traces(line_color="#3498db", line_width=2)
    for _, e in events[events["severity"] >= 5].iterrows():
        fig.add_vline(x=e["year"], line_dash="dash", line_color="red", opacity=0.4)
        fig.add_annotation(x=e["year"], y=yearly["mood_score"].max(),
                          text=e["event"][:15], showarrow=False, textangle=-45, font_size=8)
    st.plotly_chart(fig, use_container_width=True)

# PAGE 2: Mood Timeline
elif page == "📈 Mood Timeline":
    st.title("📈 100 Years of Music Mood")

    feature = st.selectbox("Select Feature", ["valence", "energy", "danceability", "mood_score", "acousticness", "tempo"])

    fig = go.Figure()
    for period, color in [("event_year", "#e74c3c"), ("near_event", "#f39c12"), ("peaceful", "#2ecc71")]:
        mask = yearly["event_period"] == period
        fig.add_trace(go.Scatter(
            x=yearly[mask]["year"], y=yearly[mask][feature],
            mode="markers+lines", name=period,
            marker=dict(color=color, size=8),
            line=dict(color=color, width=1)
        ))

    fig.update_layout(title=f"{feature.title()} Over 100 Years (Colored by Event Period)",
                      xaxis_title="Year", yaxis_title=feature.title(), height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Decade averages
    st.markdown("### Decade Averages")
    decade_avg = yearly.groupby("decade_label")[["valence", "energy", "danceability", "mood_score"]].mean().round(3)
    st.dataframe(decade_avg, use_container_width=True)

# PAGE 3: Event Impact
elif page == "💥 Event Impact":
    st.title("💥 Do World Events Change Music?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Event Period Comparison")
        comparison = yearly.groupby("event_period")[["valence", "energy", "danceability", "mood_score"]].mean().round(4)
        fig = px.bar(comparison.reset_index(), x="event_period", y=["valence", "energy", "danceability"],
                     barmode="group", title="Audio Features by Event Period",
                     color_discrete_sequence=["#3498db", "#e74c3c", "#2ecc71"])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Mood by Event Category")
        event_mood = yearly.merge(events, on="year").groupby("category_y")["valence"].mean().sort_values()
        fig = px.bar(event_mood.reset_index(), x="valence", y="category_y", orientation="h",
                     title="Average Valence by Event Type",
                     color="valence", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig, use_container_width=True)

    # Before/During/After
    st.markdown("### Before / During / After Major Events")
    selected_event = st.selectbox("Select Event", events[events["severity"] >= 4]["event"].tolist())
    evt = events[events["event"] == selected_event].iloc[0]
    yr = evt["year"]

    before = yearly[yearly["year"].between(yr - 3, yr - 1)][["year", "valence", "energy", "mood_score"]]
    during = yearly[yearly["year"] == yr][["year", "valence", "energy", "mood_score"]]
    after = yearly[yearly["year"].between(yr + 1, yr + 3)][["year", "valence", "energy", "mood_score"]]

    timeline = pd.concat([before.assign(period="Before"), during.assign(period="During"), after.assign(period="After")])
    fig = px.line(timeline, x="year", y="valence", color="period", markers=True,
                  title=f"Valence Around: {selected_event} ({yr})",
                  color_discrete_map={"Before": "#2ecc71", "During": "#e74c3c", "After": "#3498db"})
    st.plotly_chart(fig, use_container_width=True)

# PAGE 4: Genre Explorer
elif page == "🎸 Genre Explorer":
    st.title("🎸 Genre Mood Explorer")

    n_genres = st.slider("Number of genres to show", 10, 50, 20)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 😊 Happiest Genres")
        top = genres.nlargest(n_genres, "mood_score")
        fig = px.bar(top, x="mood_score", y="genres", orientation="h",
                     title=f"Top {n_genres} Happiest Genres",
                     color="mood_score", color_continuous_scale="Greens")
        fig.update_layout(yaxis=dict(autorange="reversed"), height=600)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 😢 Saddest Genres")
        bottom = genres.nsmallest(n_genres, "mood_score")
        fig = px.bar(bottom, x="mood_score", y="genres", orientation="h",
                     title=f"Top {n_genres} Saddest Genres",
                     color="mood_score", color_continuous_scale="Reds_r")
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

    # Genre scatter
    st.markdown("### Genre Map: Valence vs Energy")
    top_genres = genres.nlargest(50, "count") if "count" in genres.columns else genres.head(50)
    fig = px.scatter(top_genres, x="valence", y="energy", size="danceability",
                     hover_name="genres", color="mood_score",
                     title="Genre Mood Map (size = danceability)",
                     color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)

# PAGE 5: Deep Analysis
elif page == "🔬 Deep Analysis":
    st.title("🔬 Statistical Deep Dive")

    st.markdown("### Correlation Heatmap")
    features = ["valence", "energy", "danceability", "acousticness", "instrumentalness", "liveness", "speechiness", "tempo"]
    available = [f for f in features if f in yearly.columns]
    corr = yearly[available].corr()

    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                    title="Audio Feature Correlations", aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

    # Popularity analysis
    st.markdown("### Do Sad Songs Get More Popular?")
    if "popularity" in tracks.columns:
        sample = tracks.sample(min(5000, len(tracks)), random_state=42)
        fig = px.scatter(sample, x="valence", y="popularity", opacity=0.2,
                        trendline="ols", title="Valence vs Popularity (5K sample)",
                        color_discrete_sequence=["#3498db"])
        st.plotly_chart(fig, use_container_width=True)

        # By decade
        st.markdown("### Popularity-Mood Trend by Decade")
        from scipy import stats
        decade_corrs = []
        for decade in sorted(tracks["decade"].unique()):
            dec = tracks[tracks["decade"] == decade]
            if len(dec) > 10:
                r, p = stats.pearsonr(dec["valence"], dec["popularity"])
                decade_corrs.append({"Decade": f"{decade}s", "Correlation": round(r, 3),
                                     "Direction": "Happy wins" if r > 0 else "Sad wins"})
        dc_df = pd.DataFrame(decade_corrs)
        fig = px.bar(dc_df, x="Decade", y="Correlation", color="Direction",
                     title="Valence-Popularity Correlation by Decade",
                     color_discrete_map={"Happy wins": "#2ecc71", "Sad wins": "#e74c3c"})
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Shanmuga** | Data: Spotify/Kaggle")
st.sidebar.markdown("🎓 Portfolio Project 2")