# KPoeTools - Syllable
# https://github.com/ibratabian17/KPoeTools
# Credit Me if u going to use this tools on non-KPoe Games

import os
import json
import sys

# Check if the command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python script_name.py your_json_file.json")
    sys.exit(1)

# Get the JSON file name from the command-line argument
json_name = sys.argv[1]

# Load the JSON file
with open(json_name, 'r', encoding="utf-8") as file:
    data = json.load(file)

# Create the output directory if it doesn't exist
output_dir = os.path.join('output/', os.path.splitext(os.path.basename(json_name))[0])
os.makedirs(output_dir, exist_ok=True)


# Iterate through each array in the data field
for offset, item in enumerate(data['data']):
    # Generate the output file path
    output_file = os.path.join(output_dir, f'lyrics-data{offset}.ttml')

    # Get the ttml attribute and write it to the output file
    with open(output_file, 'w', encoding="utf-8") as outfile:
        outfile.write(item['attributes']['ttml'])
        print(f"TTML Extracted. Saved to lyrics-data{offset}.ttml")