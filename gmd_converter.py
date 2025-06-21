import json
import zlib
import base64

def escape_str(s):
    # Escape commas, colons, and other GD special chars
    return s.replace(',', '\\,').replace(':', '\\:')

def create_gmd_string(level):
    # Build the key-value string following GD format
    # Note: This is simplified and only covers basic metadata + object placement

    meta = []
    meta.append(f'kS1:{escape_str(level["name"])}')
    meta.append(f'kS2:{escape_str(level.get("desc", ""))}')
    meta.append(f'kS3:{escape_str(level.get("author", "Unknown"))}')
    meta.append(f'kS4:{level.get("version", "1")}')
    meta.append(f'kS5:{level.get("song", 0)}')
    meta.append(f'kS6:{escape_str(level.get("bg", "#000000"))}')
    meta.append(f'kS7:{escape_str(level.get("gnd", "#ffffff"))}')
    meta.append(f'kS8:{level.get("length", "5000")}')
    meta.append(f'kS9:{level.get("difficulty", "5")}')
    meta.append(f'kS10:{level.get("secretCoins", "0")}')
    meta.append(f'kS11:{level.get("featured", "0")}')
    meta.append(f'kS12:{level.get("official", "0")}')

    # Start objects array
    # GD stores objects as arrays like kA1:, kA2:, kA3: ... each represents a property list
    # We will build object arrays for these keys:
    # id (kA1), col (kA2), x (kA3), y (kA4), gid (kA5), lay (kA6), ext (kA7)

    objs = level["level"]

    def safe_int(val):
        try:
            return int(val)
        except:
            return 0

    kA1 = []  # id
    kA2 = []  # color channel
    kA3 = []  # x position
    kA4 = []  # y position
    kA5 = []  # group id (use -1 if empty)
    kA6 = []  # layer
    kA7 = []  # ext flags (strings, joined with | or empty)

    for o in objs:
        kA1.append(str(safe_int(o.get("id", 0))))
        kA2.append(str(safe_int(o.get("col", 0))))
        kA3.append(str(o.get("pos", [0,0])[0]))
        kA4.append(str(o.get("pos", [0,0])[1]))
        gid_val = o.get("gid", "")
        kA5.append(str(safe_int(gid_val)) if gid_val != "" else "-1")
        kA6.append(str(safe_int(o.get("lay", 1))))
        # Convert ext flags like "notouch,hidden" → "notouch|hidden"
        ext_str = o.get("ext", "")
        if ext_str:
            ext_str = ext_str.replace(",", "|")
        kA7.append(ext_str)

    # Join arrays with commas
    meta.append("kA1:" + ",".join(kA1))
    meta.append("kA2:" + ",".join(kA2))
    meta.append("kA3:" + ",".join(kA3))
    meta.append("kA4:" + ",".join(kA4))
    meta.append("kA5:" + ",".join(kA5))
    meta.append("kA6:" + ",".join(kA6))
    meta.append("kA7:" + ",".join(kA7))

    # Join everything with commas, this is the raw GMD string before compression+encoding
    gmd_str = ",".join(meta)
    return gmd_str

def compress_and_encode(gmd_str):
    compressed = zlib.compress(gmd_str.encode("utf-8"))
    encoded = base64.b64encode(compressed).decode("utf-8")
    return encoded

def main():
    with open("level.json", "r") as f:
        level = json.load(f)

    # Add placeholders if missing
    placeholders = {
        "author": "Unknown",
        "version": "1",
        "length": "5000",
        "difficulty": "5",
        "secretCoins": "0",
        "featured": "0",
        "official": "0"
    }
    for key, val in placeholders.items():
        if key not in level:
            level[key] = val

    gmd_str = create_gmd_string(level)
    gmd_encoded = compress_and_encode(gmd_str)

    with open("level.gmd", "w") as f:
        f.write(gmd_encoded)

    print("✅ level.gmd created! You can now import this into GDShare.")

if __name__ == "__main__":
    main()
