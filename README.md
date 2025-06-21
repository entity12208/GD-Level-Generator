#GD-Level-Generator

A toolkit to create and convert custom Geometry Dash levels from a human-readable text format into GD-compatible JSON and .gmd files.

### Overview
This project enables you to design Geometry Dash levels using a simple, editable text file (level_input.txt) describing level metadata and individual objects block-by-block.From this input, it generates:
- `level.json` — A structured JSON representation of your level.
- `level.gmd` — A compressed, encoded Geometry Dash level file that can be imported using the GDShare mod.

### Getting Started
**1. Prepare your level description**
Edit level_input.txt using the following format (example):
```
name: "My Amazing GD Level"
desc: "A challenging level with jump orbs and portals
"author: "YourName
"version: "1
"song: "123456"
bg: "#000000"
gnd: "#ffffff"
length: "5000"
difficulty: "5"
secretCoins: "3"
featured: "0"
official: "0"

level = [id: "1", col: "1", pos: "0,0", gid: "", lay: "1", ext: "notouch"
id: "2", col: "2", pos: "10,5", gid: "", lay: "1", ext: "passable"
id: "3", col: "3", pos: "20,10", gid: "5", lay: "2", ext: ""]
```
**2. Generate level.json**
Run the Python parser:
```bash
python gd_level_api.py
```
This will create level.json with a structured representation of your level.
**3. Convert to .gmd for GDShare import**
Run the converter script:
```bash
python json_to_gmd.py
```
This generates level.gmd — a file you can import directly in Geometry Dash using the GDShare mod.
