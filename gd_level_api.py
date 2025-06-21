import re
import json
from typing import List, Dict, Optional, Tuple

class GDLevel:
    def __init__(self, name: str, desc: str, song: int, bg: str, gnd: str):
        self.name = name
        self.desc = desc
        self.song = song
        self.bg = bg
        self.gnd = gnd
        self.level_objects: List[Dict] = []
    
    def place_object(self, id: int, col: int, pos: Tuple[int,int],
                     gid: Optional[int]=None, lay: int=1, ext: Optional[str]=None):
        self.level_objects.append(
            {
                "id": id,
                "col": col,
                "pos": list(pos),
                "gid": gid if gid is not None else "",
                "lay": lay,
                "ext": ext if ext else ""
            }
        )
    
    def to_json(self) -> str:
        return json.dumps(
            {
                "name": self.name,
                "desc": self.desc,
                "song": self.song,
                "bg": self.bg,
                "gnd": self.gnd,
                "level": self.level_objects
            },
            indent=2
        )

def parse_level_file(filepath: str) -> GDLevel:
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse metadata
    name_match = re.search(r'name:\s*"(.*?)"', content)
    desc_match = re.search(r'desc:\s*"(.*?)"', content)
    song_match = re.search(r'song:\s*"(.*?)"', content)
    bg_match = re.search(r'bg:\s*"(.*?)"', content)
    gnd_match = re.search(r'gnd:\s*"(.*?)"', content)

    if not (name_match and desc_match and song_match and bg_match and gnd_match):
        raise ValueError("Missing required metadata (name, desc, song, bg, gnd)")

    level = GDLevel(
        name=name_match.group(1),
        desc=desc_match.group(1),
        song=int(song_match.group(1)),
        bg=bg_match.group(1),
        gnd=gnd_match.group(1)
    )

    # Parse level objects
    level_lines = re.findall(
        r'id:\s*"(.*?)",\s*col:\s*"(.*?)",\s*pos:\s*"(.*?)",\s*gid:\s*"(.*?)",\s*lay:\s*"(.*?)",\s*ext:\s*"(.*?)"',
        content
    )
    for id_, col, pos, gid, lay, ext in level_lines:
        pos_tuple = tuple(map(int, pos.split(',')))
        gid_int = int(gid) if gid.isdigit() else None
        level.place_object(
            id=int(id_),
            col=int(col),
            pos=pos_tuple,
            gid=gid_int,
            lay=int(lay),
            ext=ext
        )
    return level

if __name__ == "__main__":
    # Parse level_input.txt and output level.json
    level = parse_level_file('level_input.txt')
    with open('level.json', 'w') as f:
        f.write(level.to_json())
    print("✅ Generated level.json successfully!")
