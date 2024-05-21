import json
import sys
import os

def check_word_timings(data):
    incorrect_word_timing = []
    for i in range(len(data) - 1):
        if data[i + 1]['time'] < data[i]['time']:
            incorrect_word_timing.append(data[i + 1])
    return incorrect_word_timing

def strip_until_closing_parenthesis(data, incorrect_timing):
    stripped_data = []
    try:
     start_index = data.index(incorrect_timing)
     end_index = start_index
     while end_index < len(data) and (')' not in data[end_index]['text'] or not data[end_index]['isLineEnding'] == 1):
         end_index += 1
     if end_index < len(data) and (')' in data[end_index]['text'] or data[end_index]['isLineEnding'] == 1):
         end_index += 1  # Include the object with ')'
     stripped_data = data[:start_index] + data[end_index:]
     print(f'Stripped {start_index} until {end_index}')
     return stripped_data
    except Exception:
     print(f'Skipping {incorrect_timing['time']}')
     stripped_data = data
    
    return stripped_data
    

def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)
    
    incorrect_lines = check_word_timings(parsed_data)
    print(f'Total Error: {len(incorrect_lines)}')

    if incorrect_lines:
        for incorrect_timing in incorrect_lines:
            parsed_data = strip_until_closing_parenthesis(parsed_data, incorrect_timing)
    
    input_filename = os.path.splitext(os.path.basename(file_path))[0]
    output_file_path = f'output/{input_filename}-stripped.json'
    
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=4)

    print(f"JSON Generated. Saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py your_json_file.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    process_json_file(file_path)
