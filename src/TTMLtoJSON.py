# KPoeTools - TTML2JSON
# https://github.com/ibratabian17/KPoeTools
# Credit Me if u going to use this tools on non-KPoe Games

import xml.etree.ElementTree as ET
import json
import sys
import os

def parse_ttml(file_path, offset=0):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {
        'tt': 'http://www.w3.org/ns/ttml',
        'itunes': 'http://music.apple.com/lyric-ttml-internal',
        'ttm': 'http://www.w3.org/ns/ttml#metadata'
    }
    timing_mode = root.attrib.get('{http://music.apple.com/lyric-ttml-internal}timing', 'Word')
    if timing_mode == "Line":
        print('[WARNING] This TTML are not Synced Word-by-Word')
    
    lyrics = []
    
    for div in root.findall('.//tt:div', namespace):
        for p in div.findall('.//tt:p', namespace):
            if timing_mode == "Line":
                p_text = p.text or ""
                p_begin = time_to_ms(p.attrib['begin'])
                p_end = time_to_ms(p.attrib['end'])
                p_duration = p_end - p_begin
                
                lyrics.append({
                    "time": p_begin + offset,
                    "duration": p_duration,
                    "text": p_text,
                    "isLineEnding": 1
                })
            else:
                spans = p.findall('.//tt:span', namespace)
                text = ""
                for i, span in enumerate(spans):
                    if isinstance(span.text, str):
                        span_text = span.text
                        span_begin = time_to_ms(span.attrib['begin'])
                        span_end = time_to_ms(span.attrib['end'])
                        span_duration = span_end - span_begin
                    
                        text += span_text
                        if isinstance(spans[i].tail, str):
                            text += spans[i].tail
                    
                        lyrics.append({
                            "time": span_begin + offset,
                            "duration": span_duration,
                            "text": text,
                            "isLineEnding": 1 if i == len(spans) - 1 else 0
                        })
                        text = ""
                    else:
                        print(f'[WARNING] Skipping Offset {i} after {lyrics[-1]['text']}')
    return lyrics

def time_to_ms(time_str):
    parts = time_str.split(':')
    
    if len(parts) == 3:  # Format: "HH:MM:SS.sss"
        hours, minutes, seconds = parts
        hours = int(hours)
        minutes = int(minutes)
    elif len(parts) == 2:  # Format: "MM:SS.sss"
        hours = 0
        minutes, seconds = parts
        minutes = int(minutes)
    elif len(parts) == 1 and '.' in parts[0]:  # Format: "SS.sss"
        hours = 0
        minutes = 0
        seconds = parts[0]
    else:
        raise ValueError(f"Unexpected time format: {time_str}")

    seconds, milliseconds = map(int, seconds.split('.'))
    total_ms = hours * 60 * 60 * 1000 + minutes * 60 * 1000 + seconds * 1000 + milliseconds
    return total_ms


# Example usage:
if len(sys.argv) < 2:
    print("Usage: python script_name.py your_json_file.json offset")
    sys.exit(1)

# Get the JSON file name from the command-line argument
file_path = sys.argv[1]
output_file_path = 'output/lyrics.json'
offset = 0
if len(sys.argv) >= 3:
    offset = int(sys.argv[2])
    print(f'Starting Lyrics At {offset}ms')
lyrics_json = parse_ttml(file_path, offset)

# Write the output to a JSON file
input_file = sys.argv[1]
input_filename = os.path.splitext(os.path.basename(input_file))[0]
with open(f"output/{input_filename}.json", "w", encoding="utf-8") as f:
        json.dump(lyrics_json, f, indent=4)

print(f"JSON Generated. Saved to {output_file_path}")
