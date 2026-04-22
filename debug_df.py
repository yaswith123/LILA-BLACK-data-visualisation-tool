from utils import scan_data, load_match_data
import pandas as pd

index = scan_data('player_data')
# Pick a match with multiple files
date = 'February_12'
map_id = 'AmbroseValley'
match_id = list(index[date][map_id].keys())[0]
files = index[date][map_id][match_id]

print(f"Loading match {match_id} with {len(files)} files")
df = load_match_data(files)

print("Columns:", df.columns.tolist())
print("Types:\n", df.dtypes)
print("Row count:", len(df))
print("Unique users:", df['user_id'].nunique())
print("Bot count:", df['is_bot'].sum())
print("Rel_ts head:\n", df['rel_ts'].head())
print("Rel_ts max:", df['rel_ts'].max())
