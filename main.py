import json
import requests
from bs4 import BeautifulSoup
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

config = {
    'base_url': 'https://store.office.com/api/addins/search',
    'query_params': {
        'ad': 'US',
        'apiversion': '1.0',
        'client': 'Any_PowerBI',
        'top': '1000'
    },
    'output_file': 'parsed.json',
    'max_workers': 10 
}

def fetch_download_url(session, murl):
    try:
        res = session.get(murl)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, features="xml")
        url = soup.find("DefaultSettings").find("SourceLocation")["DefaultValue"]
        return url
    except requests.RequestException as e:
        logging.error(f'Error fetching download URL from {murl}: {e}')
        return 'n/a'
    except (AttributeError, TypeError) as e:
        logging.error(f'Error parsing the download URL from {murl}: {e}')
        return 'n/a'

def write_parsed_data(parsed, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(parsed, f, indent=4)
        logging.info(f'Parsed data written to {output_file}')
    except IOError as e:
        logging.error(f'Error writing parsed data to file: {e}')

def fetch_and_parse_item(session, ext):
    try:
        logging.info(f'Fetching download URL for {ext["Title"]}...')
        url = fetch_download_url(session, ext['ManifestUrl'])
        logging.info('Fetching download URL finished')
        return ext["Id"], {
            "title": ext["Title"],
            "url": url,
            "date_released": ext["DateReleased"],
            "last_updated": ext["LastUpdatedDate"],
            "icon_url": ext["IconUrl"],
            "votes": ext["NumberOfVotes"],
            "description": ext["ShortDescription"],
            "permissions": ext["Permissions"],
            "license": ext["LicenseTermsUrl"],
            "privacy": ext["PrivacyPolicyUrl"],
            "support": ext["SupportUrl"],
            "pid": ext["ProductId"],
            "version": ext["Version"],
            "rating": ext["Rating"],
            "categories": ext["Categories"],
        }
    except Exception as e:
        logging.error(f'An unexpected error occurred for {ext["Title"]}: {e}')
        return ext["Id"], None

def parse_response(response):
    data = response.json()
    total = data.get('TotalCount', 0)
    items = data.get('Values', [])
    parsed = {}
    
    logging.info('-------------------starting--------------------')
    
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=config['max_workers']) as executor:
            futures = {executor.submit(fetch_and_parse_item, session, ext): ext["Id"] for ext in items}
            for future in as_completed(futures):
                ext_id, result = future.result()
                if result:
                    parsed[ext_id] = result
                logging.info(f"------------------{len(parsed)}/{total}------------------")

    write_parsed_data(parsed, config['output_file'])
    logging.info('-------------------finished--------------------')

def main():
    try:
        response = requests.get(config['base_url'], params=config['query_params'])
        response.raise_for_status()
        parse_response(response)
    except requests.RequestException as e:
        logging.error(f'Error fetching data from store: {e}')

if __name__ == "__main__":
    main()
