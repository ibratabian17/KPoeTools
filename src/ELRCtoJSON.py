# KPoeTools - ELRC2JSON
# https://github.com/ibratabian17/KPoeTools
# Credit Me if u going to use this tools on non-KPoe Games


import json
import sys
import os

def parse_line(line):
    line = line.strip()
    if not line or line[0] != "[":
        return None

    parts = line.split(":")
    key = parts[0][1:]
    value = parts[-1].replace("]", "").strip()
    return key, value

def parse_time(time_str):
    minute, second, millisecond = map(int, time_str.split(":"))
    return minute * 60000 + second * 1000 + millisecond * 10

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py input_file")
        return

    input_file = sys.argv[1]
    output_json = []

    with open(input_file, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        parsed = parse_line(line)
        if parsed:
            key, value = parsed
            if key == "ti":
                name = value
            elif key == "ar":
                artist = value
            elif key == "la":
                language = value
            elif key == "re":
                creator = value
            elif key == "ve":
                version = value
        else:
            words = line.split("  ")
            for word in words:
                time_text = word[:8]
                text = word[8:].split("]")[-1] if "]" in word else word[8:].split(">")[-1]
                final_time = parse_time(time_text)
                try:
                    duration = final_time - output_json[-1]["time"]
                except IndexError:
                    duration = 0
                is_line_ending = 1 if word == words[-1] else 0
                if "]" in word:
                    is_line_ending = 1 if word.endswith("]") else 0
                lyric = {
                    "time": final_time,
                    "duration": duration,
                    "text": text,
                    "isLineEnding": is_line_ending
                }
                output_json.append(lyric)

    input_filename = os.path.splitext(os.path.basename(input_file))[0]
    with open(f"output/{input_filename}.json", "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=4)
        print(f"JSON Generated. Saved to {input_filename}.json")

if __name__ == "__main__":
    main()
