import os
import json
from markdown2 import markdown
from docx import Document
from bs4 import BeautifulSoup


def load_json_files(directory):
    json_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                json_files.append(json.load(file))
    return json_files

def extract_keywords(json_data):
    keywords = []
    for control in json_data.get('controls', []):
        keywords.extend(control.get('keywords', []))
    return keywords

def search_keywords(json_files, search_terms):
    matches = []
    for json_data in json_files:
        prefix = json_data.get('prefix', '')
        name = json_data.get('name', '')
        for control in json_data.get('controls', []):
            control_keywords = control.get('keywords', [])
            for term in search_terms:
                if any(term.lower() in keyword.lower() for keyword in control_keywords):
                    control_with_prefix = control.copy()
                    control_with_prefix['id'] = f"{prefix} {control['id']}"
                    matches.append((name, control_with_prefix))
                    break
    return matches

def keyword_search(directory, search_terms):
    json_files = load_json_files(directory)
    matches = search_keywords(json_files, search_terms)
    return matches

def convertMDtoWord(markdown_text):
    html_text = markdown(markdown_text)
    doc = Document()

    soup = BeautifulSoup(html_text, 'html.parser')

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul']):
        if element.name.startswith('h'):
            level = int(element.name[1]) - 1
            doc.add_heading(element.text, level)
        elif element.name == 'ul':
            for li in element.find_all('li'):
                doc.add_paragraph(li.text, style='List Bullet')

    return doc
