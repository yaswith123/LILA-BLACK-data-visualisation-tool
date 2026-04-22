from utils import scan_data
import os

index = scan_data('player_data')
found_multi = False
for date in index:
    print(f"Date: {date}")
    for map_id in index[date]:
        for match_id, files in index[date][map_id].items():
            if len(files) > 1:
                print(f"  Match {match_id[:8]} on {map_id}: {len(files)} files")
                found_multi = True

if not found_multi:
    print("NO MATCHES WITH MULTIPLE FILES FOUND!")
    # Let's inspect some filenames vs internal match_ids
    date_path = os.path.join('player_data', 'February_10')
    files = os.listdir(date_path)
    for f in files[:5]:
        if f.startswith('.'): continue
        print(f"File: {f}")
        # The filename structure: {user_id}_{match_id}.nakama-0
        # Let's check if the filename match_id matches the internal match_id
