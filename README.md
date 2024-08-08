# Industry Reference Keyword Search Tool

## Overview
The Industry Reference Keyword Search Tool is a desktop application built using Python and Tkinter. It allows users to search for Industry Specific keywords within a set of reference documents and provides an interface to display and manage the search results.

## Features
- **Default Dark Theme:** The application natively uses dark theme, so your eyes dont burn late at night.
- **Quick Copy to Markdown:** Users can copy the search results to the clipboard in Markdown.
- **Easy Export to Word:** Search results can be exported to a Word document.
- **Create your own References:** Easily create your own industry standards for your personal use using the template (no template et but will add soon).

## Requirements
- Python 3.12.x
- Required packages (listed in `requirements.txt`):
  - `beautifulsoup4`
  - `markdown2`
  - `python-docx`
  - `pywinstyles`
  - `sv-ttk`

## Installation
1. Download [Python](https://www.python.org/downloads/)
2. Clone or Download the Repository.
3. Install the required packages using `pip install -r requirements.txt`. *Note: File path will need to be attached to the `requirements.txt` unless ran in an virtual environment.*
4. Run the application using `python main.py`

## Usage
1. **Enter Keywords:** Entering all the keywords you are interested in into the box on the left hand side with them being seperated by a newline. *Note: The program does do partial matches!*
2. **Press Analyze:** Pressing the ANALYZE button below the keyword entry will then use all the keywords you provided and search all json files within the references folder.
3. **Copy or Export Results:** Looking at the results in detail wither in the output textarea for a quick view for copying or export it to Word.
4. **Rinse and Repeat:** Use it as much as you need!

## How to Add Additional/Custom Industry References
1. **Create a JSON File:** Create a json file within the `/references` directory.
2. **Define the Structure:** Use the `template.json` file as a templaye or use the structure below:
```json
{
    "name": "Your Industry Reference Name",
    "prefix": "Your Prefix",
    "controls": [
        {
            "id": "Unique Control ID",
            "name": "Control Name",
            "url": "URL to the Control",
            "control": "Description of the Control",
            "keywords": ["keyword1", "keyword2", "keyword3"]
        },
        {
            "id": "Another Unique Control ID",
            "name": "Another Control Name",
            "url": "URL to the Control",
            "control": "Description of the Control",
            "keywords": ["keyword1", "keyword2", "keyword3"]
        }
    ]
}
```
3. **Fill the JSON File:** Fill in each of the fields in what ever way you see fit, look at `cis.json` and `nist800-53.json` for example.
4. **Validate JSON Format:** Using a file editor with linting for JSON is useful. Additionally [this website](https://jsonpathfinder.com/) can be used to help validate the format.
5. **Save the JSON File:** Save the file with a unique name with the `.json` extension.  

## Known Bugs/Issues & Planned Features
- I Currently have **0 (ZERO)** Error handling so its possible that issues within a json file could cause the program to crash as I dont have any internal checks (for the time being).
- I plan to export it to an executable for easier use in the future.
- I plan to add error handling.
- I also plan to make a quick website for easy creation of indstry references!
