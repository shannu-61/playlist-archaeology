import pandas as pd

events = [
    {"year": 1929, "event": "Great Depression Begins", "category": "economic", "severity": 5},
    {"year": 1933, "event": "Hitler Rises to Power", "category": "political", "severity": 5},
    {"year": 1939, "event": "World War II Begins", "category": "war", "severity": 5},
    {"year": 1941, "event": "Pearl Harbor Attack", "category": "war", "severity": 5},
    {"year": 1945, "event": "WWII Ends / Atomic Bombs", "category": "war", "severity": 5},
    {"year": 1947, "event": "Cold War Begins", "category": "political", "severity": 4},
    {"year": 1950, "event": "Korean War Begins", "category": "war", "severity": 4},
    {"year": 1955, "event": "Vietnam War Escalates", "category": "war", "severity": 4},
    {"year": 1962, "event": "Cuban Missile Crisis", "category": "political", "severity": 5},
    {"year": 1963, "event": "JFK Assassination", "category": "political", "severity": 5},
    {"year": 1968, "event": "MLK & RFK Assassinations / Protests", "category": "social", "severity": 5},
    {"year": 1969, "event": "Moon Landing / Woodstock", "category": "positive", "severity": 5},
    {"year": 1973, "event": "Oil Crisis / Watergate", "category": "economic", "severity": 4},
    {"year": 1975, "event": "Vietnam War Ends", "category": "war", "severity": 4},
    {"year": 1979, "event": "Iran Hostage Crisis", "category": "political", "severity": 4},
    {"year": 1980, "event": "John Lennon Killed", "category": "social", "severity": 3},
    {"year": 1986, "event": "Chernobyl Disaster", "category": "disaster", "severity": 4},
    {"year": 1989, "event": "Berlin Wall Falls", "category": "positive", "severity": 5},
    {"year": 1991, "event": "Soviet Union Collapses / Gulf War", "category": "war", "severity": 4},
    {"year": 1997, "event": "Princess Diana Dies", "category": "social", "severity": 3},
    {"year": 2001, "event": "9/11 Attacks", "category": "war", "severity": 5},
    {"year": 2003, "event": "Iraq War Begins", "category": "war", "severity": 4},
    {"year": 2005, "event": "Hurricane Katrina", "category": "disaster", "severity": 4},
    {"year": 2008, "event": "Global Financial Crisis", "category": "economic", "severity": 5},
    {"year": 2011, "event": "Arab Spring / Bin Laden Killed", "category": "political", "severity": 4},
    {"year": 2014, "event": "ISIS Rise / Ebola Outbreak", "category": "war", "severity": 4},
    {"year": 2016, "event": "Brexit / Trump Election", "category": "political", "severity": 4},
    {"year": 2020, "event": "COVID-19 Pandemic", "category": "pandemic", "severity": 5},
]

df = pd.DataFrame(events)
df.to_csv("data/raw/world_events.csv", index=False)

print(f"Created {len(df)} world events")
print(f"Categories: {df['category'].value_counts().to_dict()}")
print(f"\nSample:\n{df.head(10)}")
print("\nSaved to data/raw/world_events.csv")