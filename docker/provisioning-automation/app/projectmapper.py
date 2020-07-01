import requests

# Return a dictionary of environmentId: environmentName so that we can dynamically return the Add Host Command
def get_rancher_projects(rancher_url, rancher_auth, verify_ssl):
    projects = {}
    session = requests.session()
    response = session.get(f'{rancher_url}/projects/', auth=rancher_auth, verify=verify_ssl)
    for project in response.json()["data"]:
        if project["state"] is "inactive":
            pass
        else:
            projects[project["name"]] = project["id"]

    return projects

# Return the registration URL from the Rancher API to add hosts
def get_registration_url(rancher_url, rancher_auth, verify_ssl, projects, environment):
    projects = projects
    environment_id = projects[environment]
    session = requests.session()
    response = session.get(f'{rancher_url}/projects/{environment_id}/registrationtokens', auth=rancher_auth, verify=verify_ssl)
    data = {}
    # The needed information from the API is returned in a list format, we need to convert it to a dictionary
    for key in response.json()["data"]:
        data['credential_map'] = key

    # print(data['credential_map']['registrationUrl'])
    return data['credential_map']['registrationUrl']
