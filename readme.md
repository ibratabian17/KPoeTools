
# KPoeTools

KPoeTools is a collection of tools for managing and converting lyric formats into JSON format. These tools can be used for text extraction from various formats and converting them into JSON format according to the KPOE standard.

## Tool Overview

| Tool Name              | Description                                                                                 | How to Use                                                                                        |
|------------------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| SyllableExtractor      | Extracts text from Apple Music response in TTML format.                                      | Open `src/SyllableExtractor.py response.json` or `src/KpoeTools.py`                                              |
| TTMLtoJSON             | Converts lyrics in TTML format to JSON format according to the KPOE standard.                | Open `src/TTMLtoJSON.py input_file.ttml offset_in_ms` or `src/KpoeTools.py`                                                     |
| ELRCtoJSON             | Converts lyrics in ELRC format to JSON format according to the KPOE standard.                | Open `src/ELRCtoJSON.py input_file.lrc` or `src/KpoeTools.py`                                                     |

## Usage

Each tool can be used by running the corresponding file name.

### Example Usage of SyllableExtractor:

1. Open a terminal.
2. Navigate to the KPoeTools project directory.
3. Run the following command:
```bash
python src/KpoeTools.py input_file.json
```


### Example Usage of TTMLtoJSON:

1. Open a terminal.
2. Navigate to the KPoeTools project directory.
3. Run the following command:

```bash
python src/TTMLtoJSON.py input_file.ttml 0 #offset in ms
```

### Example Usage of ELRCtoJSON:

1. Open a terminal.
2. Navigate to the KPoeTools project directory.
3. Run the following command:

```bash
python src/ELRCtoJSON.py input_file.ttml
```

## Contribution

Contributions to this project are greatly appreciated. Please fork this repository and create a pull request with desired changes.

## License

This project is licensed under the Creative Commons License. See the [LICENSE](LICENSE) file for details.