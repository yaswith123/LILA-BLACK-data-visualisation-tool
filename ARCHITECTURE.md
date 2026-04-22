# System Architecture - Player Journey Visualization Tool

## Overview
The tool is built as a reactive Streamlit application that processes gameplay telemetry data (Parquet) and overlays it onto 2D minimaps using Plotly.

## Data Flow
1. **Discovery**: The `scan_data` utility indexes the `player_data/` directory by date and match metadata.
2. **On-Demand Loading**: When a match is selected, only the relevant `.parquet` files for that match are loaded into memory.
3. **Transformation**:
   - Event bytes are decoded to UTF-8 strings.
   - Bot vs. Human logic is applied based on `user_id` format.
   - World coordinates `(x, z)` are mapped to pixel coordinates `(px, py)` using map-specific constants.
4. **Visualization**: Plotly renders multiple layers (Heatmap -> Paths -> Markers) on top of the minimap image.

## Coordinate Mapping
The conversion follows the formula provided in the PRD:
- **U/V Normalization**: `u = (x - origin_x) / scale`, `v = (z - origin_z) / scale`
- **Pixel Conversion**: `px = u * 1024`, `py = (1 - v) * 1024` (Y is flipped for image space).

## Tech Stack & Choices
- **Streamlit**: Chosen for rapid interactive UI development.
- **Plotly**: Provides high-performance interactive layers with zoom and hover support.
- **PyArrow**: Used for fast, low-memory reading of Parquet files.
- **Pillow**: Handles minimap image loading and metadata.

## Assumptions & Tradeoffs
- **Fixed Resolution**: Assumes all minimaps are 1024x1024 (as verified in map config).
- **Match Aggregation**: Assumes a match can be fully reconstructed by grouping all files with the same `match_id`.
