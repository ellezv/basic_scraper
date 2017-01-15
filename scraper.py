import requests

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


def load_inspection_page():
    """Load inspection_page."""
    with open('inspection_page.html', 'r') as f:
        content = f.read()
        encoding = "utf-8"
    return content, encoding
