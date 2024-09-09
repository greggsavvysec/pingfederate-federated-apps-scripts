#This Python Script scrips sensitive JSON data from a list of SAML connections exported from the PingFederate Administrative API
#SAML Connection details can be gathered from the either the PingFederate Administrative API Documentation Portal or REST Interface:
### REST: GET https://<pf-admin-url>:<pf-admin-port>/pf-admin-api/v1/idp/spConnections
### WEB:  https://<pf-admin-url>:<pf-admin-port>/pf-admin-api/api-docs/#/idp/spConnections/getConnections > Try it Out > Execute
#Note: You may need to utilize API paging to gather the entire list of SAML Connections
#Update the input_file_path to match the location of the JSON exported from the step outlined above

import json
import csv
from urllib.parse import urlparse

# Define file paths
input_json_path = 'PingFederate-SAML-Output.json'
output_csv_with_duplicates_path = 'Connections-SAML-With-Duplicate-URLs.csv'
output_csv_without_duplicates_path = 'Connections-SAML-Without-Duplicate-URLs.csv'

# Step 1: Parse the SAML JSON data and prepare data for CSV
# Read the JSON data from the input file
with open(input_json_path, 'r') as file:
    data = json.load(file)

# Lists to hold data for CSV files
all_entries = []
unique_entries = []
unique_endpoints = set()

# Extract the required fields
for item in data['items']:
    # Prepare base data
    name = item['name']
    entityId = item['entityId']
    
    # Process ssoServiceEndpoints
    for endpoint in item.get('spBrowserSso', {}).get('ssoServiceEndpoints', []):
        url = endpoint['url']
        # Prepend baseUrl if url does not start with 'http'
        if not url.startswith('http'):
            # Use baseUrl from the item if it exists
            base_url = item.get('baseUrl', '')
            url = f"{base_url}{url}" if base_url else url
        
        # Parse the URL to get the base domain and port
        parsed_url = urlparse(url)
        base_domain_port = (parsed_url.hostname, parsed_url.port)
        
        # Create a row for the current entry
        row = [
            name,
            entityId,
            endpoint['binding'],
            url,
            endpoint['isDefault'],
            endpoint['index']
        ]
        
        # Add to all entries (including duplicates)
        all_entries.append(row)
        
        # Check for unique entries
        if base_domain_port not in unique_endpoints:
            unique_endpoints.add(base_domain_port)
            unique_entries.append(row)

# Step 2: Write the CSV files
# Write all entries (including duplicates) to the first CSV
with open(output_csv_with_duplicates_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header
    writer.writerow(['name', 'entityId', 'binding', 'url', 'isDefault', 'index'])
    # Write all entries
    writer.writerows(all_entries)

print(f"SAML data with duplicates has been written to {output_csv_with_duplicates_path}")

# Write unique entries to the second CSV
with open(output_csv_without_duplicates_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header
    writer.writerow(['name', 'entityId', 'binding', 'url', 'isDefault', 'index'])
    # Write unique entries
    writer.writerows(unique_entries)

print(f"SAML data without duplicates has been written to {output_csv_without_duplicates_path}")
