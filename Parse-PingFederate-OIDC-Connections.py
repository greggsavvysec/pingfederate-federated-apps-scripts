#This Python Script scrips sensitive JSON data from a list of OIDC Clients exported from the PingFederate Administrative API
#OIDC Connection details can be gathered from the either the PingFederate Administrative API Documentation Portal or REST Interface:
### REST: GET https://<pf-admin-url>:<pf-admin-port>/pf-admin-api/v1/oauth/clients
### WEB:  https://<pf-admin-url>:<pf-admin-port>/pf-admin-api/api-docs/#/oauth/clients/getClients > Try it Out > Execute
#Note: You may need to utilize API paging to gather the entire list of OIDC Clients

#Update the input_file_path to match the location of the JSON exported from the step outlined above

import json
import csv
from urllib.parse import urlparse

# Define file paths
input_json_file_path = 'PingFederate-OIDC-Output.json'
output_csv_file_path_with_duplicates = 'Connections-OIDC-With-Duplicate-URLs.csv'
output_csv_file_path_without_duplicates = 'Connections-OIDC-Without-Duplicate-URLs.csv'

# Step 1: Read the OIDC JSON data
# Read the JSON data from the input file
with open(input_json_file_path, 'r') as file:
    data = json.load(file)

# Step 2: Open the CSV file for writing with duplicates
with open(output_csv_file_path_with_duplicates, 'w', newline='') as csv_file_with_duplicates:
    writer_with_duplicates = csv.writer(csv_file_with_duplicates)
    
    # Write the header
    writer_with_duplicates.writerow(['clientId', 'redirectUri', 'name'])
    
    # Step 3: Open the CSV file for writing without duplicates
    with open(output_csv_file_path_without_duplicates, 'w', newline='') as csv_file_without_duplicates:
        writer_without_duplicates = csv.writer(csv_file_without_duplicates)
        
        # Write the header
        writer_without_duplicates.writerow(['clientId', 'redirectUri', 'name'])
        
        # Set to track unique base domain and port combinations
        unique_redirects = set()
        
        # Step 4: Extract the required fields and write to both CSVs
        for item in data['items']:
            client_id = item['clientId']
            name = item['name']
            
            for redirect_uri in item['redirectUris']:
                # Write to the CSV with duplicates
                writer_with_duplicates.writerow([
                    client_id,
                    redirect_uri,
                    name
                ])
                
                # Parse the redirect URI to get the base domain and port
                parsed_uri = urlparse(redirect_uri)
                base_domain_port = parsed_uri.netloc  # This includes domain and port
                
                # Check if the base domain and port combination is already in the set
                if base_domain_port not in unique_redirects:
                    unique_redirects.add(base_domain_port)  # Add to the set
                    # Write to the CSV without duplicates
                    writer_without_duplicates.writerow([
                        client_id,
                        redirect_uri,
                        name
                    ])

print(f"CSV with duplicates has been written to {output_csv_file_path_with_duplicates}")
print(f"Non-duplicate CSV has been written to {output_csv_file_path_without_duplicates}")
