"""A simple scraper for food safety inspection data."""

import requests
from bs4 import BeautifulSoup
import sys
import re

DOMAIN = "http://info.kingcounty.gov/"
PATH = 'health/ehs/foodsafety/inspections/Results.aspx'
QUERY_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': 'Seattle',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'B',
}


def get_inspection_page(**kwargs):
    """Return inspection information for given search."""
    url = DOMAIN + PATH
    params = QUERY_PARAMS.copy()
    for key, val in kwargs.items():
        if key in QUERY_PARAMS:
            params[key] = val
    resp = requests.get(url, params=params, stream=True)
    resp.raise_for_status()
    return resp.content, resp.encoding


def load_inspection_page(file_path):
    """Load inspection_page."""
    with open(file_path, 'r') as f:
        content = f.read()
        encoding = "utf-8"
    return content, encoding


def parse_source(html, encoding='utf-8'):
    """Parse the html with beautifulsoup."""
    parsed = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    return parsed


def extract_data_listings(parsed_data):
    """Return a list of the restaurant listing container nodes."""
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    print(type(doc))
    listings = extract_data_listings(doc)
    print(len(listings))
    print(listings[0].prettify())
    # print(doc.prettify(encoding=encoding))
