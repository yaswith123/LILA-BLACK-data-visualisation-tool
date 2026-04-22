# 🎮 LILA Analytics: Player Journey Visualizer

A high-fidelity gameplay telemetry visualization platform built for LILA.  
This tool transforms raw Parquet telemetry data into interactive spatial insights, enabling level designers to analyze player behavior, identify combat hotspots, and understand match progression.

---

## 🌐 Live Demo

👉 https://lila-black-data-visualisation-tool-b9gf2tilfsijhhdkxdrnxq.streamlit.app/

---

## 🚀 Features

- **📍 Spatial Visualization**  
  Overlay player movement paths and gameplay events (Kills, Loot, Storm) directly on minimap images.

- **🕒 Interactive Timeline**  
  Replay match progression using a timeline slider with play/pause controls.

- **🔥 Dynamic Heatmaps**  
  Identify player density and combat hotspots to detect high-traffic zones and chokepoints.

- **📊 Match Intelligence**  
  View summarized metrics such as player distribution (humans vs bots), total events, and match activity.

- **🗺️ Multi-Map Support**  
  Supports Ambrose Valley, Grand Rift, and Lockdown with accurate coordinate mapping.

- **🎛️ Layer Controls**  
  Toggle player paths, event markers, and heatmaps for focused analysis.

- **🌓 Clean UI**  
  Modern, intuitive interface designed for quick exploration and usability.

---

## 🧭 How to Use

1. Select a **Map**, **Date**, and **Match** using the filters at the top  
2. View **player movement paths** and **event markers** (Kill, Death, Loot, Storm) on the minimap  
3. Distinguish between **human and bot players** through visual differences  
4. Use the **timeline slider** or **play button** to replay match progression over time  
5. Toggle between **heatmap modes** (Player Density / Kill Hotspots) to analyze activity patterns  
6. Enable or disable layers (paths, events, heatmap) for focused exploration  
7. Review **match summary metrics** (players, events, kills, etc.) for quick insights  
8. Explore the **Insights tab** to understand key gameplay patterns and design implications  

---

## 🛠️ Tech Stack

- **Core**: Python 3.8+
- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Data Processing**: Pandas, PyArrow
- **Image Handling**: Pillow
- **State Management**: Streamlit session state and query parameters

---

## 📂 Data Structure

The tool expects telemetry data organized as follows:

```text
player_data/
├── minimaps/
│   ├── AmbroseValley_Minimap.png
│   ├── GrandRift_Minimap.png
│   └── Lockdown_Minimap.jpg
├── YYYY-MM-DD/
│   └── player_matchid_...nakama-0
└── ...
```

* Each file represents **one player in one match**
* Matches are reconstructed by grouping files using `match_id`

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yaswith123/LILA-BLACK-data-visualisation-tool.git
cd LILA-BLACK-data-visualisation-tool
```

### 2. Install Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## 🏗️ Architecture Overview

* **app.py**
  Main entry point handling UI rendering, timeline playback, and visualization logic.

* **utils.py**
  Core processing layer:

  * Coordinate mapping (world → minimap)
  * Data loading and indexing
  * Match reconstruction and preprocessing

* **ARCHITECTURE.md**
  Detailed explanation of:

  * Data flow from parquet files to visualization
  * Coordinate mapping logic
  * Assumptions and tradeoffs

---

## ⚠️ Data Notes

The dataset contains partial player coverage for many matches.
Analysis shows that some matches include only a subset of players (e.g., 1–14 players), indicating that the dataset is sampled and does not represent full match participation.

The system is designed to handle this variability by reconstructing matches using all available player data without assuming completeness.

---

## 🚀 Deployment

The application is deployed using **Streamlit Cloud** and is accessible via the live demo link above.

---

## 📋 Requirements

* streamlit
* pandas
* plotly
* pyarrow
* Pillow
* numpy

---

## 🎯 Summary

This tool enables level designers to:

* Understand player movement patterns
* Identify combat hotspots and underutilized areas
* Analyze match progression over time
* Make data-driven gameplay and map design decisions

---

*Built with ❤️ for LILA Games.*
