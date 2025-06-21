# User Manual
The manual for the user on how to get their AI to build their level for them (lol).

## Requirements
The latest version of [Python](https://python.org)

## Setup
To get started, show the AI the README for this repository, then 
ask them to make a level using it. Once they have made the **text** file, download this repository and paste their text into `level_input.txt`. Once done, run the following
in that order:
- `python txt_to_json.py`
- `python json_to_gdr.py`

Once done, use GDShare to inport the `.gdr` file into GD as a level.
