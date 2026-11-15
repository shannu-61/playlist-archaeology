\# 🎵 Playlist Archaeology: How World Events Shape Music Mood



> Analyzing 100 years of Spotify audio data (1921-2020) to discover how wars, recessions, pandemics, and cultural shifts influence the mood of popular music.



!\[Python](https://img.shields.io/badge/Python-3.12-blue)

!\[Streamlit](https://img.shields.io/badge/Streamlit-Interactive\_App-red)

!\[Status](https://img.shields.io/badge/Status-Complete-green)



\## 📸 Dashboard Preview



\### Overview

!\[Overview](screenshots/streamlit\_overview.png)



\### Mood Timeline (100 Years)

!\[Timeline](screenshots/streamlit\_timeline.png)



\### Event Impact Analysis

!\[Events](screenshots/streamlit\_events.png)



\### Genre Mood Explorer

!\[Genres](screenshots/streamlit\_genres.png)



\### Statistical Deep Dive

!\[Analysis](screenshots/streamlit\_analysis.png)



\## 🎯 Project Overview



\*\*The Question:\*\* Does the world around us change the music we create and listen to?



Using 170,653 tracks spanning 100 years of music history, this project correlates audio features (valence, energy, danceability) with 28 major world events to uncover how global crises and cultural moments shape musical expression.



\## 🔬 Key Findings



| Finding | Detail | Statistical Evidence |

|---------|--------|---------------------|

| 🎵 Music IS getting sadder | Valence declining since 1970s | r=-0.195, p=0.051 |

| ⚡ Events boost energy | Event years have 24% more energy | p=0.022 (significant) |

| 😷 Pandemics = saddest music | Lowest mood category (0.501) | Category comparison |

| 💰 Recessions = party music | Highest mood category (0.585) | Category comparison |

| 📉 2020s: sad songs win | First decade where sad beats happy | r=-0.092 (popularity) |

| 🔊 Acoustic → Electronic | Energy vs acousticness: r=-0.967 | Near-perfect inverse |



\## 🛠️ Tech Stack



| Tool | Purpose |

|------|---------|

| Python 3.12 | Core programming language |

| Pandas | Data cleaning \& manipulation |

| SciPy | Statistical testing (t-tests, Pearson correlation) |

| Matplotlib \& Seaborn | Static visualizations |

| Plotly | Interactive charts |

| Streamlit | Interactive web application |

| Git/GitHub | Version control |



\## 📊 Dataset



\- \*\*Source:\*\* \[Kaggle - Spotify Dataset 1921-2020](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-160k-tracks)

\- \*\*Tracks:\*\* 170,653 songs across 100 years

\- \*\*Features:\*\* Valence, energy, danceability, acousticness, tempo, loudness, and more

\- \*\*World Events:\*\* 28 manually curated events across 7 categories (war, economic, political, social, positive, disaster, pandemic)



\## 📁 Project Structure



```

playlist-archaeology/

├── scripts/

│   ├── explore\_data.py          # Initial data exploration

│   ├── create\_events.py         # World events dataset creation

│   ├── clean\_and\_merge.py       # Data cleaning \& merging

│   ├── analyze.py               # Statistical analysis \& visualizations

│   ├── deep\_analysis.py         # Genre, war vs recession, popularity analysis

│   ├── export\_for\_tableau.py    # Tableau data export

│   └── app.py                   # Streamlit interactive dashboard

├── data/

│   ├── raw/                     # Original Kaggle datasets

│   ├── processed/               # Cleaned \& merged data + charts

│   └── tableau/                 # Tableau-ready exports

├── screenshots/                 # App screenshots

├── .gitignore

├── requirements.txt

└── README.md

```



\## 🧪 Statistical Methods



\- \*\*Independent T-Tests:\*\* Comparing audio features between event years vs peaceful years

\- \*\*Pearson Correlation:\*\* Testing year vs valence trend (is music getting sadder?)

\- \*\*Year-over-Year Change Analysis:\*\* Tracking mood shifts around specific events

\- \*\*Before/During/After Analysis:\*\* 3-year window around major events

\- \*\*Decade Aggregation:\*\* Identifying era-level patterns



\## 💡 Interesting Insights



\### The 1940s Were the Saddest Decade

During WWII, music valence dropped to 0.379 — the lowest in 100 years. The mood didn't fully recover until the 1960s counterculture movement.



\### People Party Through Recessions

Economic crises (Great Depression, 2008 Financial Crisis) produced music with the HIGHEST mood scores. When times are tough, people turn to uplifting music as escapism.



\### The 2020s Shift

For the first time in recorded music history, sadder songs are becoming MORE popular than happy ones (r=-0.092). This reversal coincides with the streaming era and social media culture.



\### Energy Explosion

Music energy has increased by 200%+ from the 1920s to 2020s (r=0.933, p=0.000), reflecting the shift from acoustic instruments to electronic production.



\## 🚀 How to Run



```bash

\# Clone the repository

git clone https://github.com/shannu-61/playlist-archaeology.git

cd playlist-archaeology



\# Create virtual environment

python -m venv venv

venv\\Scripts\\activate



\# Install dependencies

pip install -r requirements.txt



\# Run the Streamlit app

streamlit run scripts/app.py

```



\## 📈 Mood Score Formula



```

mood\_score = valence × 0.5 + energy × 0.3 + danceability × 0.2

```



This weighted composite captures the overall "mood" of music, emphasizing happiness (valence) while accounting for energy and danceability.



\## 👤 Author



\*\*Shanmuga Kothapalli\*\*

\- GitHub: \[@shannu-61](https://github.com/shannu-61)



\## 📜 License



This project is for educational and portfolio purposes. Dataset sourced from Kaggle under its terms of use.

