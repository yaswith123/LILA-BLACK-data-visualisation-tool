import pandas as pd
import os
from utils import scan_data, load_match_data

def generate_insights():
    data_index = scan_data("player_data")
    
    # Let's analyze a few matches to find patterns
    all_events = []
    
    # Sample a few matches from different maps
    for date in list(data_index.keys())[:2]:
        for map_id in data_index[date]:
            match_ids = list(data_index[date][map_id].keys())[:2]
            for m_id in match_ids:
                df = load_match_data(data_index[date][map_id][m_id])
                all_events.append(df)
                
    full_df = pd.concat(all_events, ignore_index=True)
    
    print("--- Insight Analysis ---")
    
    # 1. Combat Density (Bots vs Humans)
    human_kills = len(full_df[full_df['event'] == 'Kill'])
    bot_kills = len(full_df[full_df['event'] == 'BotKill'])
    print(f"Human Kills: {human_kills}, Bot Kills: {bot_kills}")
    
    # 2. Storm Deaths
    storm_deaths = len(full_df[full_df['event'] == 'KilledByStorm'])
    print(f"Killed By Storm: {storm_deaths}")
    
    # 3. Loot Hotspots
    loot_counts = full_df[full_df['event'] == 'Loot'].groupby('map_id').size()
    print(f"Loot per map:\n{loot_counts}")
    
    # 4. Bot deaths
    bot_deaths = len(full_df[full_df['event'] == 'BotKilled'])
    print(f"Bot Deaths: {bot_deaths}")

if __name__ == "__main__":
    generate_insights()
