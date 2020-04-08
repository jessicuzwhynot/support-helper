import requests
from os import getenv


def get_rancher_projects(rancher_url, rancher_auth, verify_ssl):
    projects = {}
    session = requests.session()
    response = session.get(f'{rancher_url}/projects/', auth=rancher_auth, verify=verify_ssl)
    for project in response.json()["data"]:
        if project["state"] is "inactive":
            pass
        else:
            projects[project["id"]] = {"env": project["name"], "hosts": {}}

    return projects


def get_rancher_hosts (rancher_url, rancher_auth, verify_ssl, limit):
    session = requests.session()
    response = session.get(f'{rancher_url}/hosts?limit={limit}', auth=rancher_auth, verify=verify_ssl)

    return response.json()["data"]


def map_rancher_hosts_to_project (hosts, projects):
    for host in hosts:
        if host["state"] == 'active':
            pass
        else:
            project = host["accountId"]
            host_id = host["id"]
            hostname = host["data"]["fields"]["hostname"]
            state = host["state"]

            if "crate.region" in host["data"]["fields"]["labels"]:
                region = host["data"]["fields"]["labels"]["crate.region"]
            else:
                region = "NotFound"
            if "crate.host.name" in host["data"]["fields"]["labels"]:
                short_name = host["data"]["fields"]["labels"]["crate.host.name"]
            else:
                short_name = "NotFound"
            if state == 'disconnected':
                projects[project]["hosts"][host_id] = {
                    "hostname"  : hostname,
                    "region"    : region,
                    "short_name": short_name,
                    "state"     : state
                }
            else:
                pass
    return projects


def disconnected_hosts_list(disconnected_hosts):
    disconnects = {}
    hosts = []
    for project in disconnected_hosts:
        if disconnected_hosts[project]['hosts'] == {}:
            pass
        else:
            disconnects[project] = disconnected_hosts[project]
            disconnects[project]['hosts'] = disconnected_hosts[project]['hosts']
            for host in disconnects[project]['hosts']:
                hosts.append(f"{disconnects[project]['hosts'][host]['short_name']}({disconnects[project]['env']}) in "
                             f"{disconnects[project]['hosts'][host]['region']}")
    return hosts


def send_slack_notification(webhook_url, slack_channel, slack_user, disconnected_hosts):
    channel = slack_channel
    webhook = webhook_url
    user = slack_user
    flattened_list = ", ".join(map(str, disconnected_hosts))
    text = f"The following hosts are disconnected: `{flattened_list}`"
    payload = {
        "channel": channel,
        "username": user,
        "text": text
    }
    session = requests.session()
    if flattened_list == '':
        return
    else:
        response = session.post(webhook, json=payload)
        return response



if __name__ == '__main__':
    rancher_url = getenv('RANCHER_URL', 'https://console.ciscocrate.com/v2-beta')
    rancher_access_key = getenv('RANCHER_ACCESS_KEY')
    rancher_secret_key = getenv('RANCHER_SECRET_KEY')
    rancher_auth = (rancher_access_key, rancher_secret_key)
    verify_ssl = True
    limit = 1500
    slack_channel = getenv('SLACK_CHANNEL', '#notify-ops')
    webhook_url = getenv('SLACK_WEBHOOK_URL')
    slack_user = 'Disconnected Host Notifier'

    projects = get_rancher_projects(rancher_url, rancher_auth, verify_ssl)
    rancher_hosts = get_rancher_hosts(rancher_url, rancher_auth, verify_ssl, limit)
    disconnected_host_map = map_rancher_hosts_to_project(rancher_hosts, projects)
    disconnected_list = disconnected_hosts_list(disconnected_host_map)
    send_slack_notification(webhook_url, slack_channel, slack_user, disconnected_list)
