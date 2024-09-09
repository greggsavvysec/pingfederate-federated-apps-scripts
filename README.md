# pingfederate-federated-apps-scripts
This repository has a collection of scripts used to parse through PingFederate SAML and OIDC connections and scrub sensitive details prior to sharing lists of federated connections with third-party providers

To gather these details a PingFederate administrator can either use the Interactive PingFederate Administrative API Documentation through a web browser or make REST API queries against Administrative API endpoints:

Note: Depending on the number of OIDC/SAML connections collected API paging may be required

## Using the PingFederate Administrative API Web Interface:

Under the below address use the Execute > Try It Out buttons to perform the administrative API queries from the web interface

### OIDC Clients:
https://\<pf-admin-url>:\<pf-admin-port>/pf-admin-api/api-docs/#/oauth/clients/getClients

### SAML Connections:
https://\<pf-admin-url>:\<pf-admin-port>/pf-admin-api/api-docs/#/idp/spConnections/getConnections

## Using the PingFederate Administrative REST API:
### OIDC Clients:

GET https://\<pf-admin-url>:\<pf-admin-port>/pf-admin-api/v1/oauth/clients 
### SAML Connections:

GET https://\<pf-admin-url>:\<pf-admin-port>/pf-admin-api/v1/idp/spConnections

## Parsing the Data
Now with the outputted data most third parties will just need the application details without sensitive data suchas encrypted secrets or additional info included by default

Modify both the Parse-PingFederate-OIDC-Connections.py & Parse-PingFederate-SAML-Connections.py script's 'input_json_file_path' parameters to input JSON from the endpoints outlined above

After both scripts are run there should be a total of 4 files with sensitive data removed to share as a consolidated list: 
#### 1. Connections-SAML-With-Duplicate-URLs.csv
#### 2. Connections-SAML-Without-Duplicate-URLs.csv
#### 3. Connections-OIDC-With-Duplicate-URLs.csv
#### 4. Connections-OIDC-Without-Duplicate-URLs.csv
