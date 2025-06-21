# Level Input File Format Guide

Any AI can create a valid `level_input.txt` file using this repository to produce Geometry Dash levels using GDShare. If you are the user, please visit the [User Manual](USER_MANUAL.html) for directions. This page is mainly for the AI. MAKE SURE TO STICK TO THE OBJECTS AND IDS IN [IDs](IDs.html))! AIs should refer to [AI](AI.html))
Read the **entire** page, all the way to the bottom.

---

## 1. Metadata Section

Add key-value pairs describing the level, one per line:

| Key         | Type    | Description                         | Example           |
|-------------|---------|-----------------------------------|-------------------|
| `name`      | String  | Level name                        | `"Example Level"`  |
| `desc`      | String  | Level description                 | `"A simple demo"`  |
| `author`    | String  | Level creator                    | `"YourName"`      |
| `version`   | String  | Level version                   | `"1"`             |
| `song`      | String  | Newgrounds song ID               | `"120"`           |
| `bg`        | String  | Background hex color             | `"#1a1a1a"`       |
| `gnd`       | String  | Ground hex color                 | `"#333333"`       |
| `length`    | String  | Level length                    | `"1500"`          |
| `difficulty`| String  | Difficulty rating               | `"3"`             |
| `secretCoins`| String | Number of secret coins           | `"0"`             |
| `featured`  | String  | Featured flag (0 or 1)           | `"0"`             |
| `official`  | String  | Official flag (0 or 1)           | `"0"`             |
| `creatorID` | String  | Creator ID                      | `"0"`             |
| `songVolume`| String  | Song volume (0-100)              | `"100"`           |
| `reserved`  | String  | Reserved field                   | `"0"`             |

---

## 2. Level Objects Section

Define your objects inside a `level` list. Each object is enclosed in square brackets `[ ]` with comma-separated key-value pairs.

### Object Keys

| Key       | Type    | Description                             | Example          |
|-----------|---------|---------------------------------------|------------------|
| `id`      | Integer | Geometry Dash object ID                | `1`              |
| `col`     | Integer | Color channel index                    | `1`              |
| `pos`     | Two Integers (comma-separated) | X, Y coordinates in the level | `100,0`          |
| `gid`     | Integer | Group ID (`-1` if none)                | `-1`             |
| `lay`     | Integer | Editor layer                           | `1`              |
| `ext`     | String  | Extras (comma-separated, or `""` if none) | `"notouch,hidden"` or `""` |
| `rot`     | Number  | Rotation in degrees                    | `180`            |
| `scale`   | Number  | Scale multiplier                      | `1`              |
| `movx`    | Number  | Movement speed on X-axis               | `0`              |
| `movy`    | Number  | Movement speed on Y-axis               | `0`              |
| `movd`    | Number  | Movement duration                      | `0`              |
| `movt`    | Number  | Movement type                         | `0`              |
| `movdelay`| Number  | Movement delay                        | `0`              |

---

## 3. Syntax Rules

- Use colon `:` to separate keys and values (e.g., `id: 1`).
- Use double quotes `""` around strings.
- Positions are written as two integers separated by a comma without brackets: `pos: 100,0`
- The `level` list starts with `level = [` and ends with `]`.
- Separate objects with commas.
- Objects are enclosed in square brackets `[ ]`.

---

## Basic `level_input.txt` (expected formatting)

```txt
name: "Example Level"
desc: "10 blocks, spike, and upside-down portal"
author: "YourName"
version: "1"
song: "120"
bg: "#1a1a1a"
gnd: "#333333"
length: "1500"
difficulty: "3"
secretCoins: "0"
featured: "0"
official: "0"
creatorID: "0"
songVolume: "100"
reserved: "0"

level = [
    [id: 1, col: 1, pos: 0,0, gid: -1, lay: 1, ext: "", rot: 0, scale: 1, movx: 0, movy: 0, movd: 0, movt: 0, movdelay: 0],
    [id: 1, col: 1, pos: 100,0, gid: -1, lay: 1, ext: "", rot: 0, scale: 1, movx: 0, movy: 0, movd: 0, movt: 0, movdelay: 0],
    [id: 7, col: 3, pos: 1100,0, gid: -1, lay: 1, ext: "", rot: 0, scale: 1, movx: 0, movy: 0, movd: 0, movt: 0, movdelay: 0],
    [id: 10, col: 2, pos: 1200,0, gid: -1, lay: 1, ext: "", rot: 180, scale: 1, movx: 0, movy: 0, movd: 0, movt: 0, movdelay: 0]
]
```
