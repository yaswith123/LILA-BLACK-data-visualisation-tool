import os
import pyarrow.parquet as pq

path = os.path.join('player_data', 'February_10')
files = [f for f in os.listdir(path) if not f.startswith('.')]
f = files[0]

# Filename pattern: {user_id}_{match_id}
# Example: f4e072fa-b7af-4761-b567-1d95b7ad0108_b71aaad8-aa62-4b3a-8534-927d4de18f22.nakama-0
parts = f.split('_')
user_id_fn = parts[0]
match_id_fn = parts[1]

df = pq.read_table(os.path.join(path, f), columns=['user_id', 'match_id']).to_pandas()
user_id_int = df['user_id'].iloc[0]
match_id_int = df['match_id'].iloc[0]

print(f"File: {f}")
print(f"User ID - Filename: {user_id_fn}, Internal: {user_id_int}")
print(f"Match ID - Filename: {match_id_fn}, Internal: {match_id_int}")
