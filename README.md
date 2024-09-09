# pingfederate-federated-apps-scripts
This Repository has a collection of scripts used to parse through PingFederate SAML and OIDC connections and scrub sensitive details prior to sharing lists of federated connections with third-party providers

Running both python scripts will output 4 total files if run properly: 
1. Connections-SAML-With-Duplicate-URLs.csv
2. Connections-SAML-Without-Duplicate-URLs.csv
3. Connections-OIDC-With-Duplicate-URLs.csv
4. Connections-OIDC-Without-Duplicate-URLs.csv
