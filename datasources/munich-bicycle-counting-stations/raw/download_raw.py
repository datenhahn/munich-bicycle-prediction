"""
Script to download the raw data of the bicycle counting stations from the munich opendata project.

https://opendata.muenchen.de/dataset/raddauerzaehlstellen-muenchen

WARNING: The data of the different years and files has certain continuity issues and should be
         cleaned before usage.

         A jupyter notebook for data cleaning can be found in the parent folder.

Usage:
  python3 download_raw.py

Result:
  Will download all csv files into the current folder, and create metadata.json files with the
  information from the api.

== Bicycle counting stations

Recent traffic counts over the last few years have shown a significant increase in bicycle traffic
in Munich. However, since the data was mostly collected on individual days as a "snapshot", random
influences such as differing weather conditions could not be ruled out during comparisons.
Therefore, for the first time in 2008, permanent bicycle counting stations were set up for bicycle
traffic in Munich. These counting stations allow for the continuous observation of the development
of bicycle traffic volume.
"""

import json
import logging
import os

import requests

def write_file(file_name, bytes):
    """Writes bytes to a file, but skips existing files."""

    # script must be idempotent
    if os.path.exists(file_name):
        logging.info("The resource file already exists, not overwriting: " + file_name)
    else:
        with open(file_name, 'wb') as file:
            file.write(bytes)

# Searches for all data associated with the "Bicycle Counting Stations". Setting the result rows to 1000
# to not have to paginate through the results.
API_URL = "https://opendata.muenchen.de/api/3/action/package_search?q=Raddauerz%C3%A4hlstellen&rows=1000"
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# STEP 1: Download list of available datasets.
logging.info("Downloading available data from " + API_URL)
api_response = requests.get(API_URL)
api_response.raise_for_status()
response_body = api_response.json()
response_results = response_body['result']['results']

logging.info(f"Found {len(response_results)} datasets")

# STEP 2: Download CSV of each dataset and save the metadata for potential later usage.
for result in response_results:

    # STEP 2a: Save Metadata.
    file_base = f"{result['name']}-{result['id']}"
    file_name = f"{SCRIPT_DIR}/{file_base}-metadata.json"
    logging.info("Writing metadata for " + file_name)
    write_file(file_name, json.dumps(result, indent=4).encode('utf-8'))

    # STEP 2b: Download data CSVs.
    for resource in result['resources']:

        # there is bug in the api data, sometimes the url field is names original_url, sometimes url
        if 'original_url' in resource:
            unified_url = resource['original_url']
        else:
            unified_url = resource['url']
            
        resource_file_name = SCRIPT_DIR + "/" + file_base + "-" + os.path.basename(unified_url)

        logging.info("Checking resource: " + resource_file_name)

        # check if we already have downloaded the file before and skip otherwise the download
        # directly to save time and bandwidth
        if not os.path.exists(resource_file_name):
            logging.info("Downloading resource: " + resource_file_name)
            csv_response = requests.get(unified_url)
            csv_response.raise_for_status()
            csv = csv_response.content
            resource_file_name = SCRIPT_DIR + "/" + file_base + "-" + os.path.basename(unified_url)
            write_file(resource_file_name, csv)
        else:
            logging.info("Resource already exists, skipping: " + resource_file_name)