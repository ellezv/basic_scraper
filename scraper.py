"""A simple scraper for food safety inspection data."""

import requests
from bs4 import BeautifulSoup
import sys
import re

INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    "Output": "W",
    "Business_Name": "",
    "Business_Address": "",
    "Longitude": "",
    "Latitude": "",
    "City": "",
    "Zip_Code": "",
    "Inspection_Type": "All",
    "Inspection_Start": "",
    "Inspection_End": "",
    "Inspection_Closed_Business": "A",
    "Violation_Points": "",
    "Violation_Red_Points": "",
    "Violation_Descr": "",
    "Fuzzy_Search": "N",
    "Sort": "B",
}

query = {
    "Business_Name": "Tango",
    "Business_Address": "1100%20Pike%20St",
    "City": "Seattle",
    "Zip_Code": "98101"
}

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

HEADERS = {'User-Agent': UA}


def get_inspection_page(**kwargs):
    """Return inspection information for given search."""
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    resp = requests.get(url, params=params, headers=HEADERS, stream=True)
    resp.raise_for_status()
    return resp.content, resp.encoding


def load_inspection_page():
    """Load response from inspection_page."""
    with open('inspection_page.html', 'r') as f:
        content = f.read()
        encoding = 'utf-8'
    return content, encoding


def write_results(results):
    """Write results of search to file."""
    with open('inspection_page.html', 'w') as f:
        f.write(results)


def parse_source(html, encoding='utf-8'):
    """Set up HTML as DOM nodes for scraping."""
    soup = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    return soup


def extract_data_listings(html):
    """Extract container with data."""
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


def has_two_tds(elem):
    """."""
    is_tr = elem.name == 'tr'
    td_children = elem.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two


def clean_data(td):
    """Clean the cells to remove whitespace when printing."""
    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


def extract_restaurant_metadata(elem):
    """Extract the restaurant metadata, clean it and return it."""
    metadata_rows = elem.find('tbody').find_all(
        has_two_tds, recursive=False
    )
    rdata = {}
    current_label = ''
    for row in metadata_rows:
        key_cell, val_cell = row.find_all('td', recursive=False)
        new_label = clean_data(key_cell)
        current_label = new_label if new_label else current_label
        rdata.setdefault(current_label, []).append(clean_data(val_cell))
    return rdata


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page()
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    print(type(doc))
    listings = extract_data_listings(doc)
    for listing in listings[:5]:
        metadata = extract_restaurant_metadata(listing)
        print(metadata)
        print()  # prints extra line between each restaurant info.
