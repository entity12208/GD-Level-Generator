import re
import json

def parse_level_input_txt(filepath="level_input.txt"):
    level = {
        "level": []
    }
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    # Match `key: value` where value can be quoted or unquoted
    meta_pattern = re.compile(r'^(\w+):\s*(?:"([^"]*)"|(.*))$')
    level_array_started = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("level = ["):
            level_array_started = True
            continue
        if level_array_started:
            if line == "]":
                level_array_started = False
                continue

            # Parse object lines like [id: 1, pos: 60,80], etc.
            obj = {
                "id": 0,
                "col": 0,
                "pos": [0, 0],
                "gid": -1,
                "lay": 1,
                "ext": "",
                "rot": 0,
                "scale": 1,
                "movx": 0,
                "movy": 0,
                "movd": 0,
                "movt": 0,
                "movdelay": 0
            }

            parts = [p.strip() for p in line.split(",")]
            for part in parts:
                if not part or ":" not in part:
                    continue
                key, val = part.split(":", 1)
                key = key.strip()
                val = val.strip().strip('"')

                if key == "pos":
                    coords = val.split(",")
                    if len(coords) == 2:
                        try:
                            obj["pos"] = [float(coords[0]), float(coords[1])]
                        except:
                            obj["pos"] = [0, 0]
                elif key in ("id","col","lay","movt"):
                    obj[key] = int(val) if val.isdigit() else 0
                elif key == "gid":
                    obj[key] = int(val) if val.isdigit() else -1
                elif key in ("rot","scale","movx","movy","movd","movdelay"):
                    try:
                        obj[key] = float(val)
                    except:
                        obj[key] = 0
                else:
                    obj[key] = val

            level["level"].append(obj)

        else:
            m = meta_pattern.match(line)
            if m:
                key = m.group(1)
                val = m.group(2) if m.group(2) is not None else m.group(3)
                level[key] = val.strip()

    # Fill defaults for missing top-level properties
    defaults = {
        "name": "Untitled",
        "desc": "",
        "author": "Unknown",
        "version": "1",
        "length": "5000",
        "difficulty": "5",
        "secretCoins": "0",
        "featured": "0",
        "official": "0",
        "creatorID": "0",
        "songVolume": "100",
        "reserved": "0",
        "bg": "0",
        "gnd": "0",
        "song": "0"
    }
    for key, default_val in defaults.items():
        level.setdefault(key, default_val)

    return level

def main():
    level = parse_level_input_txt("level_input.txt")
    with open("level.json", "w") as f:
        json.dump(level, f, indent=4)
    print("✅ level.json created from level_input.txt")

if __name__ == "__main__":
    main()
