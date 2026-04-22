import os
import pandas as pd
import pyarrow.parquet as pq

# --- Official Map Configuration (from README.md) ---
MAP_CONFIG = {
    "AmbroseValley": {
        "image": "AmbroseValley_Minimap.png",
        "origin_x": -370.0,
        "origin_z": -473.0,
        "scale": 900.0
    },
    "GrandRift": {
        "image": "GrandRift_Minimap.png",
        "origin_x": -290.0,
        "origin_z": -290.0,
        "scale": 581.0
    },
    "Lockdown": {
        "image": "Lockdown_Minimap.jpg",
        "origin_x": -500.0,
        "origin_z": -500.0,
        "scale": 1000.0
    }
}

def world_to_pixel(world_x, world_z, map_id):
    """
    World-to-Minimap Conversion logic adjusted for Plotly.
    Plotly uses a Bottom-Up coordinate system (0 is bottom).
    """
    if map_id not in MAP_CONFIG:
        return 0, 0
        
    cfg = MAP_CONFIG[map_id]
    
    # Step 1: Convert world coords to UV (0-1 range)
    u = (world_x - cfg["origin_x"]) / cfg["scale"]
    v = (world_z - cfg["origin_z"]) / cfg["scale"]
    
    # Step 2: Convert UV to Plotly pixel coords
    # We use v * 1024 (Bottom-Up) instead of (1-v) * 1024 (Top-Down)
    # to match Plotly's Cartesian coordinate system.
    pixel_x = u * 1024
    pixel_y = v * 1024 
    
    return pixel_x, pixel_y

def scan_data(base_path):
    """Indexes files by Date -> Map -> MatchID"""
    data_index = {}
    if not os.path.exists(base_path):
        return data_index
        
    for date_folder in os.listdir(base_path):
        date_path = os.path.join(base_path, date_folder)
        if not os.path.isdir(date_path) or date_folder == "minimaps":
            continue
            
        data_index[date_folder] = {}
        
        for filename in os.listdir(date_path):
            if filename.startswith('.') or not filename.endswith('.nakama-0'):
                continue
                
            file_path = os.path.join(date_path, filename)
            parts = filename.split('_')
            if len(parts) < 2: continue
            
            match_id = parts[1]
            
            try:
                # Optimized: Peek at map_id
                table = pq.read_table(file_path, columns=['map_id'])
                map_id = table['map_id'][0].as_py()
                
                if map_id not in data_index[date_folder]:
                    data_index[date_folder][map_id] = {}
                if match_id not in data_index[date_folder][map_id]:
                    data_index[date_folder][map_id][match_id] = []
                    
                data_index[date_folder][map_id][match_id].append(file_path)
            except:
                continue
    return data_index

def load_match_data(file_paths):
    """Loads and aggregates all players for a single match."""
    frames = []
    for path in file_paths:
        try:
            table = pq.read_table(path)
            df = table.to_pandas()
            df['event'] = df['event'].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
            df['is_bot'] = df['user_id'].apply(lambda x: len(str(x)) < 10)
            
            # Use the corrected world_to_pixel logic
            map_id = df['map_id'].iloc[0]
            df['pixel_x'], df['pixel_y'] = zip(*df.apply(lambda r: world_to_pixel(r['x'], r['z'], map_id), axis=1))
            
            frames.append(df)
        except:
            continue
            
    if not frames: return pd.DataFrame()
    combined_df = pd.concat(frames, ignore_index=True)
    combined_df = combined_df.sort_values('ts')
    start_ts = combined_df['ts'].min()
    combined_df['rel_ts'] = (combined_df['ts'] - start_ts).dt.total_seconds()
    return combined_df
