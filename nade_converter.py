import json
import sys
import os

id_to_map_name = {
    "472303159": "de_anubis",
    "1850914608": "de_overpass",
    "310946799": "de_italy",
    "3017110649": "de_ancient",
    "1165138098": "de_nuke",
    "2410686675": "de_dust2",
    "3722013375": "de_train",
    "2701214622": "de_inferno",
    "1162604407": "de_palais",
    "3260998844": "de_mirage",
    "3503655174": "de_basalt",
    "2176677845": "de_vertigo",
    "2360246505": "de_edin",
    "1318785012": "de_office",
}

def convert_json_to_text(json_file, text_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    
    # Log Loaded JSON structures
    print("Loaded JSON structure:")
    for map_id in data:
        print(f"Map {map_id} keys: {list(data[map_id].keys())}")
    
    output_lines = []

    throw_methods = {
        (False, False, False): "throw",
        (False, True, False): "duckthrow",
        (True, False, False): "jumpthrow",
        (False, False, True): "runthrow",
        (True, False, True): "runjumpthrow",
        (True, True, False): "duckjumpthrow",
        (False, True, True): "duckrunthrow"
    }

    for map_id, map_data in data.items():
        map_name = id_to_map_name.get(map_id, "unknown_map")
        
        # Check if grenades key exists
        if "grenades" not in map_data:
            print(f"Warning: Map {map_id} ({map_name}) doesn't have a 'grenades' key. Skipping.")
            continue
            
        for nade_id, nade_data in map_data["grenades"].items():
            grenade_type = nade_data["type"]
            if grenade_type == "smokegrenade":
                grenade_type = "smoke"
            name = nade_data.get("name", "unknown")
            pos = nade_data["position"]
            view = nade_data["view_angle"]

            movement = nade_data.get("movement_data", {})
            if isinstance(movement, list):
                movement = movement[0] if movement else {}

            jump = movement.get("jump", False)
            crouch = movement.get("crouch", False)
            move_ticks = movement.get("move_ticks", 0)

            method = throw_methods.get((jump, crouch, move_ticks > 0), "throw")
            delay = move_ticks * 0.05

            line = f"{map_name},{round(pos['x'], 2)},{round(pos['y'], 2)},{round(pos['z'], 2)},{name},0.00,0.20,{round(view['x'], 2)},{round(view['y'], 2)},0.00,{method},{grenade_type},{delay:.2f}"
            output_lines.append(line)

    with open(text_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))

    print(f"Conversion complete. Output saved to {text_file}")


input = f"{os.path.expanduser('~')}\\Downloads\\input.json"
output = f"{os.path.expanduser('~')}\\Downloads\\output.txt"

convert_json_to_text(input, output)
