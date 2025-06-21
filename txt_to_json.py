import re
import json

def parse_level_input_txt(filepath="level_input.txt"):
    level = {
        "level": []
    }
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    meta_pattern = re.compile(r'^(\w+):\s*"(.*)"$')
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

            obj = {
                "id": 0, "col": 0, "pos": [0, 0], "gid": -1, "lay": 1, "ext": "",
                "rot": 0, "scale": 1, "movx": 0, "movy": 0, "movd": 0, "movt": 0, "movdelay": 0
            }

            # Remove brackets and trailing commas
            inner = line.lstrip('[').rstrip('],')

            # Regex to capture key:value pairs including pos which can have commas
            pairs = re.findall(r'(\w+):\s*([^,\]]+(?:,[^,\]]+)*)', inner)

            for key, val in pairs:
                key = key.strip()
                val = val.strip().strip('"').strip("'")

                if key == "pos":
                    parts = val.split(',')
                    if len(parts) == 2:
                        try:
                            obj["pos"] = [int(parts[0].strip()), int(parts[1].strip())]
                        except:
                            obj["pos"] = [0, 0]
                elif key in ("id", "col", "lay", "movt"):
                    obj[key] = int(val) if val.isdigit() else 0
                elif key == "gid":
                    obj[key] = int(val) if val.isdigit() else -1
                elif key in ("rot", "scale", "movx", "movy", "movd", "movdelay"):
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
                key, val = m.group(1), m.group(2)
                level[key] = val

    # Fill defaults if missing
    defaults = {
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
    }
    for key, val in defaults.items():
        if key not in level:
            level[key] = val

    return level

def main():
    level = parse_level_input_txt("level_input.txt")
    with open("level.json", "w") as f:
        json.dump(level, f, indent=4)
    print("✅ level.json created from level_input.txt")

if __name__ == "__main__":
    main()
