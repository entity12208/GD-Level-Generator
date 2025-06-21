import zlib
import base64
import json

def unescape_str(s):
    return s.replace('\\,', ',').replace('\\:', ':')

def parse_gmd_string(gmd_str):
    parts = gmd_str.split(",")
    data = {}
    arrays = {}

    for part in parts:
        if ':' not in part:
            continue
        key, val = part.split(":", 1)
        if key.startswith("kS"):  # metadata fields
            data_key = {
                "kS1": "name",
                "kS2": "desc",
                "kS3": "author",
                "kS4": "version",
                "kS5": "song",
                "kS6": "bg",
                "kS7": "gnd",
                "kS8": "length",
                "kS9": "difficulty",
                "kS10": "secretCoins",
                "kS11": "featured",
                "kS12": "official",
                "kS13": "creatorID",
                "kS14": "songVolume",
                "kS15": "reserved",
            }.get(key, key)
            data[data_key] = unescape_str(val)

        elif key.startswith("kA"):  # arrays for objects
            arrays[key] = val.split(",")

    # Build list of objects from arrays
    objs = []
    if arrays:
        length = len(next(iter(arrays.values())))
        for i in range(length):
            obj = {
                "id": int(arrays.get("kA1", ["0"])[i]),
                "col": int(arrays.get("kA2", ["0"])[i]),
                "pos": [float(arrays.get("kA3", ["0"])[i]), float(arrays.get("kA4", ["0"])[i])],
                "gid": int(arrays.get("kA5", ["-1"])[i]),
                "lay": int(arrays.get("kA6", ["1"])[i]),
                "ext": arrays.get("kA7", [""])[i].replace("|", ","),
                "rot": float(arrays.get("kA8", ["0"])[i]),
                "scale": float(arrays.get("kA9", ["1"])[i]),
                "movx": float(arrays.get("kA10", ["0"])[i]),
                "movy": float(arrays.get("kA11", ["0"])[i]),
                "movd": float(arrays.get("kA12", ["0"])[i]),
                "movt": int(arrays.get("kA13", ["0"])[i]),
                "movdelay": float(arrays.get("kA14", ["0"])[i]),
            }
            objs.append(obj)

    data["level"] = objs
    return data

def main():
    with open("level.gmd", "r") as f:
        gmd_encoded = f.read().strip()

    decoded = base64.b64decode(gmd_encoded)
    decompressed = zlib.decompress(decoded).decode("utf-8")

    level_data = parse_gmd_string(decompressed)

    with open("level_out.json", "w") as f:
        json.dump(level_data, f, indent=4)

    print("✅ level_out.json created from level.gmd")

if __name__ == "__main__":
    main()
