# ARCHITECTURE.md

## Player Journey Visualization Tool

---

## 1. Tech Stack & Rationale

- **Streamlit (Frontend + Backend)**  
  Chosen for rapid development, built-in interactivity, and easy deployment.

- **Plotly (Visualization Engine)**  
  Enables interactive map overlays, timelines, and heatmaps with minimal effort.

- **Pandas + PyArrow (Data Processing)**  
  Efficient handling of parquet files and flexible data transformations.

- **Pillow (Image Handling)**  
  Used to load and render minimap images.

**Why this stack:**  
Prioritized speed of development, simplicity, and sufficient interactivity for a data exploration tool.

---

## 2. Data Flow

```text
Parquet Files (player-level)
        ↓
Load all files (directory scan)
        ↓
Combine into single dataframe
        ↓
Group by match_id (match reconstruction)
        ↓
Sort by timestamp (ts)
        ↓
Coordinate transformation (x, z → px, py)
        ↓
Filtered by UI (map, date, match, time)
        ↓
Rendered via Plotly (map + overlays)
```

### Key Idea:

Each file represents **one player in one match**.
Matches are reconstructed by grouping all files with the same `match_id`.

---

## 3. Coordinate Mapping (Critical Component)

### Problem:

Game coordinates are in world space, but visualization requires mapping to a 2D minimap image.

### Approach:

```text
u = (x - origin_x) / scale
v = (z - origin_z) / scale

pixel_x = u * 1024
pixel_y = (1 - v) * 1024
```

### Explanation:

* `(x, z)` represent horizontal position in the game world
* Values are normalized using map-specific `origin` and `scale`
* Mapped to a fixed 1024×1024 minimap
* Y-axis is inverted to match image coordinate system

### Map Configuration:

Each map has predefined:

* `scale`
* `origin_x`, `origin_z`

### Result:

Accurate alignment of player positions and events on the minimap.

---

## 4. Assumptions

* Each parquet file represents a single player’s telemetry for a match
* `x` and `z` define spatial position; `y` (height) is ignored
* Timestamps (`ts`) represent progression within a match
* Minimap resolution is fixed at 1024×1024

### Data Limitation:

The dataset contains **partial player coverage**.
Some matches include only a subset of players (e.g., 1–14), indicating sampled data.

### Handling:

The system reconstructs matches using all available data without assuming full completeness.

---

## 5. Tradeoffs

| Decision                   | Reason                        | Tradeoff                           |
| -------------------------- | ----------------------------- | ---------------------------------- |
| Streamlit                  | Fast development & deployment | Limited UI customization           |
| Plotly                     | Built-in interactivity        | Less control than custom rendering |
| Load all data upfront      | Simpler pipeline              | Higher memory usage                |
| Downsampling movement data | Improves performance          | Slight loss of path granularity    |
| Use static minimaps        | Simplicity                    | No zoom-level detail               |

---

## 6. Summary

This system transforms fragmented, player-level telemetry into an interactive, map-based visualization tool.
It enables spatial and temporal analysis of gameplay data, helping level designers identify patterns and make informed design decisions.
