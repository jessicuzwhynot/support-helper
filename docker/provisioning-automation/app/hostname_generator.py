import requests

# Post the generated payload to the Hostname Service API
def generate_hostnames(rancher_environment, number_of_hosts_to_create):
    rancher_environment = rancher_environment
    hostname_url = f'http://hostname-service.hostname-service:9000/env/{rancher_environment}/hostname'
    response = requests.post(hostname_url, json={"amount": number_of_hosts_to_create})

    return response.json()
