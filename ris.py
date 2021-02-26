import io
import sys
import re
import csv
import json

def get_parts(ris_file_text):
    ris_text_parts = re.split(r'\nER  -( |\n|$)', ris_file_text)
    if len(ris_text_parts) == 1:
        ris_text_parts = re.split(r'\r?\n\r?\n', ris_file_text)
    if len(ris_text_parts) == 1:
        ris_file_text = ris_file_text.replace('\r', '\n')
        ris_text_parts = re.split(r'\n\n\n', ris_file_text)
    return [doc.strip() for doc in ris_text_parts if doc.strip()]


def get_ris_attributes(ris_part_text):
    data = {}
    current_tag = None
    end_position = 0
    current_tag = None
    sep = "-"
    regex = re.compile(r'^\s*[A-Z][A-Z0-9]{1,3}\s*[-]', re.MULTILINE)
    if len(re.split(regex, ris_part_text)) < 4:
        regex = re.compile(r'^\s*[A-Z][A-Z0-9]{1,3}\s*[:]', re.MULTILINE)
        sep = ":"
        if len(re.split(regex, ris_part_text)) < 4:
            sep = ""
            regex = re.compile(r'^[A-Z][A-Z0-9]{1,3}\s*', re.MULTILINE)
    sep_size = len(sep)
    for iteration_match in regex.finditer(ris_part_text):
        current_text = ris_part_text[end_position:iteration_match.start()].strip()
        if current_tag in data.keys():
            data[current_tag].append(current_text)
        elif current_tag:
            data[current_tag] = [current_text]
        current_tag = ris_part_text[iteration_match.start():iteration_match.end()-1].strip()
        end_position = iteration_match.end() + sep_size
    # GET last one
    current_text = ris_part_text[end_position:].strip()
    if current_tag in data.keys():
        data[current_tag].append(current_text)
    elif current_tag:
        data[current_tag] = [current_text]
    return data

def get_known_tags():
    return [
        'title',
        'year',
        'document_type',
        'authors',
        'abstract',
        'doi',
        'pubmed',
        'keywords',
        'volume_number',
        'issue_number',
        'page_number',
        'ISBN_ISSN',
        'url'
    ]

def parse_known_tags(ris_attributes, join_separtor=' '):
    know_tags = {
        'document_type': ['TY'],
        'year': ['Y1', 'PY', 'YR'],
        'title': ['T1', 'TI', 'CT', 'BT', 'TT'],
        'doi': ['DOI', 'DO', 'DI'],
        'pubmed': ['PMID'],
        'keywords': ['KW', 'DE'],
        'abstract': ['AB', 'N2'],
        'authors': ['AU', 'A1'],
        'volume_number': ['VL', 'VI', 'SV'],
        'issue_number': ['IS'],
        'page_number': ['SP', 'PG'],
        'ISBN_ISSN': ['SN'],
        'url': ['UR']
    }
    return_data = dict(
        [
            (header, '')
            for header in get_known_tags()
        ]
    )
    for target_name in know_tags:
        sep = ""
        for tag in know_tags[target_name]:
            found_values = ris_attributes.get(tag) or []
            if len(found_values) == 0:
                continue
            text = join_separtor.join(found_values)
            return_data[target_name] += sep + text.strip()
            sep = join_separtor
    return return_data



def parse_ris(ris_file_text, use_known=False):
    for ris_part_text in get_parts(ris_file_text):
        if use_known:
            yield parse_known_tags(get_ris_attributes(ris_part_text))
        else:
            yield get_ris_attributes(ris_part_text)