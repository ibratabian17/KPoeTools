import os, sys, json
import shutil, pathlib
import tkinter as tk
from tkinter import filedialog
anu = True

def main_menu():
    print("Welcome To KPoeTools")
    print("Created By Ibratabian17")
    print("Only for KPoe. If You want to use for another game, credit me")
    print("============================")
    print("1) Extract TTML from Apple Music Syllable Response")
    print("2) Convert ELRC to JSON FORMAT")
    print("3) Convert TTML to JSON FORMAT")
    print("4) Fix Backing Vocal Lyrics Issue on older KPoe")
    print("5) Romanize Lyrics For Non-English Songs")
    print("")
    print("16) Exit bestie")
    print("============================")
    option = input("Hey Bestie? What Should I Do Today?: ")

    if option == '1':
        root = tk.Tk()
        root.title('')
        file_path = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select the Response", filetypes=[("Response JSON", ".json")])
        root.destroy()
        run_script(f"src/SyllableExtractor.py \"{file_path}\"")
    elif option == '2':
        root = tk.Tk()
        root.title('')
        file_path = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Choose the LyricsFiles", filetypes=[("Lyrics Files/Enhanced Lyrics Files", ".lrc/.elrc")])
        root.destroy()
        run_script(f"src/ELRCtoJSON.py \"{file_path}\" {offset}")
    elif option == '3':
        root = tk.Tk()
        root.title('')
        file_path = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Choose the TTML", filetypes=[("Timed Text Markup Language", ".ttml")])
        offset = input('Do you want to use offset? ignore if no. (miliseconds): ')
        separate = input('Do you want to put space as different word? (yes/no): ')
        root.destroy()
        run_script(f"src/TTMLtoJSON.py \"{file_path}\" {offset} {separate}")
    elif option == '4':
        root = tk.Tk()
        root.title('')
        file_path = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select the Lyrics", filetypes=[("Lyrics JSON", ".json")])
        root.destroy()
        run_script(f"src/Compability.py \"{file_path}\"")
    elif option == '5':
        root = tk.Tk()
        root.title('')
        file_path = filedialog.askopenfilename(initialdir=str(pathlib.Path().absolute()), title="Select the Lyrics", filetypes=[("Lyrics JSON", ".json")])
        print('Available Languages:\n* kr = Korean   * zh = Chinese   * jp = Japan\n* ar = Arabic   * heb = Hebrew   * sy = Syiria   * gr = Greek')
        lang = input('Which language do you want to romanize? (regioncode): ')
        root.destroy()
        run_script(f"src/Romanizer.py \"{file_path}\" {lang}")
    elif option == '16':
        sys.exit(0)
    else:
        print("Invalid option. Please select 1 or 2.")
        input('Press enter to continue (ENTER):')

def run_script(a, pause=True):
    print(f"Runnning {a}")
    # Replace the following command with the actual command to run mapConverter.py
    os.system(f"python {a}")
    if pause: input('Press enter to continue (ENTER):')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    while(anu):
     clear_terminal()
     main_menu()

