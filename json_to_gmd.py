import json
import zlib
import base64

def escape_str(s):
    return s.replace(',', '\\,').replace(':', '\\:')

def create_gmd_string(level):
    meta = []
    meta.append(f'kS1:{escape_str(level["name"])}')                  # Level name
    meta.append(f'kS2:{escape_str(level.get("desc", ""))}')          # Description
    meta.append(f'kS3:{escape_str(level.get("author", "Unknown"))}') # Author
    meta.append(f'kS4:{level.get("version", "1")}')                  # Version
    meta.append(f'kS5:{level.get("song", 0)}')                       # Newgrounds song ID
    meta.append(f'kS6:{escape_str(level.get("bg", "#000000"))}')     # Background color
    meta.append(f'kS7:{escape_str(level.get("gnd", "#ffffff"))}')    # Ground color
    meta.append(f'kS8:{level.get("length", "5000")}')                # Level length in px
    meta.append(f'kS9:{level.get("difficulty", "5")}')               # Difficulty 1-10
    meta.append(f'kS10:{level.get("secretCoins", "0")}')             # Secret coins count
    meta.append(f'kS11:{level.get("featured", "0")}')                # Featured flag
    meta.append(f'kS12:{level.get("official", "0")}')                # Official flag
    meta.append(f'kS13:{level.get("creatorID", "0")}')               # Creator user ID
    meta.append(f'kS14:{level.get("songVolume", "100")}')            # Song volume
    meta.append(f'kS15:{level.get("reserved", "0")}')                # Reserved (usually 0)

    objs = level["level"]

    # Prepare arrays for object data
    kA1 = []   # Object IDs
    kA2 = []   # Color channels
    kA3 = []   # X positions
    kA4 = []   # Y positions
    kA5 = []   # Group IDs (-1 if none)
    kA6 = []   # Editor layers
    kA7 = []   # Extras flags (pipe-separated)
    kA8 = []   # Rotation (degrees)
    kA9 = []   # Scale
    kA10 = []  # Move X speed
    kA11 = []  # Move Y speed
    kA12 = []  # Move duration
    kA13 = []  # Move type
    kA14 = []  # Move delay
    kA15 = []  # Unknown/reserved (0)

    for o in objs:
        kA1.append(str(o.get("id", 0)))
        kA2.append(str(o.get("col", 0)))
        pos = o.get("pos", [0, 0])
        kA3.append(str(pos[0]))
        kA4.append(str(pos[1]))
        gid = o.get("gid", -1)
        # Accept empty string or None as -1 (no group)
        if gid == "" or gid is None:
            gid = -1
        kA5.append(str(gid))
        kA6.append(str(o.get("lay", 1)))

        ext_str = o.get("ext", "")
        if ext_str:
            ext_str = ext_str.replace(",", "|")
        kA7.append(ext_str)

        kA8.append(str(o.get("rot", 0)))
        kA9.append(str(o.get("scale", 1)))
        kA10.append(str(o.get("movx", 0)))
        kA11.append(str(o.get("movy", 0)))
        kA12.append(str(o.get("movd", 0)))
        kA13.append(str(o.get("movt", 0)))
        kA14.append(str(o.get("movdelay", 0)))
        kA15.append("0")

    meta.append("kA1:" + ",".join(kA1))
    meta.append("kA2:" + ",".join(kA2))
    meta.append("kA3:" + ",".join(kA3))
    meta.append("kA4:" + ",".join(kA4))
    meta.append("kA5:" + ",".join(kA5))
    meta.append("kA6:" + ",".join(kA6))
    meta.append("kA7:" + ",".join(kA7))
    meta.append("kA8:" + ",".join(kA8))
    meta.append("kA9:" + ",".join(kA9))
    meta.append("kA10:" + ",".join(kA10))
    meta.append("kA11:" + ",".join(kA11))
    meta.append("kA12:" + ",".join(kA12))
    meta.append("kA13:" + ",".join(kA13))
    meta.append("kA14:" + ",".join(kA14))
    meta.append("kA15:" + ",".join(kA15))

    return ",".join(meta)

def compress_and_encode(gmd_str):
    compressed = zlib.compress(gmd_str.encode("utf-8"))
    encoded = base64.b64encode(compressed).decode("utf-8")
    return encoded

def main():
    # Load level.json (make sure it has all required fields)
    with open("level.json", "r") as f:
        level = json.load(f)

    # Fill missing placeholders with defaults if not present
    placeholders = {
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
    for key, val in placeholders.items():
        if key not in level:
            level[key] = val

    gmd_str = create_gmd_string(level)
    gmd_encoded = compress_and_encode(gmd_str)

    with open("level.gmd", "w") as f:
        f.write(gmd_encoded)

    print("✅ level.gmd successfully created!")

if __name__ == "__main__":
    main()
