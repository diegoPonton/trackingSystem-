import csv
import os

def append_positions_to_csv(trajectories, filename):
    """
    trajectories: dict {marker_id: [(x1,y1), (x2,y2), ...]}
    Format: 1,2,3
            x1,y1;x2,y2;x3,y3
            x1,y1;x2,y2;x3,y3
    """
    if not trajectories:
        print("WARNING: No trajectories to write!")
        return
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Get sorted marker IDs
    marker_ids = sorted(trajectories.keys())
    
    # Find max trajectory length
    max_length = max(len(trajectories[mid]) for mid in marker_ids) if marker_ids else 0
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        
        # Write header with marker IDs
        header = [f"{mid}" for mid in marker_ids]
        f.write(",".join(header) + "\n")
        
        # Write position rows
        for i in range(max_length):
            row = []
            for mid in marker_ids:
                if i < len(trajectories[mid]):
                    x, y = trajectories[mid][i]
                    row.append(f"{int(x)},{int(y)}")
                else:
                    row.append("")
            f.write(";".join(row) + "\n")
    
    print(f"CSV written successfully to: {filename}")