# KPoeTools - Romanizer
# https://github.com/ibratabian17/KPoeTools
# Credit Me if u going to use this tools on non-KPoe Games

import sys
import os
import json

def romanize_text(text, lang):
    if lang == "kr":
        from korean_romanizer.romanizer import Romanizer
        r = Romanizer(text)
        return r.romanize()
    elif lang == "cn":
        import pinyin
        import unidecode
        return unidecode.unidecode(pinyin.get(text, format="strip", delimiter=" "))
    elif lang == "jp":
        import pykakasi
        kakasi = pykakasi.kakasi()
        result = kakasi.convert(text)
        return " ".join([item['hepburn'] for item in result])
    elif lang == "ar":
        # Add your Arabic romanization logic here
        pass
    else:
        raise ValueError("Unsupported language")

def romanify(file_path, lang):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    for item in data:
        if isinstance(item['text'], str):
            item['text'] = romanize_text(item['text'], lang)
    
    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python romanize.py <input_file> [<lang>]")
        sys.exit(1)

    file_path = sys.argv[1]
    lang = ""  # default language
    if len(sys.argv) >= 3:
        lang = sys.argv[2]
        print(f'Romanizing {lang}')
    
    lyrics_json = romanify(file_path, lang)

    input_file = sys.argv[1]
    input_filename = os.path.splitext(os.path.basename(input_file))[0]
    output_file_path = f"output/{input_filename}-romanized.json"
    
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(lyrics_json, f, indent=4)

    print(f"JSON Generated. Saved to {output_file_path}")
