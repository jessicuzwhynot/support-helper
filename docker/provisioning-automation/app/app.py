import logging
from os import getenv

from generate_cloud_config import parse_hostname_list, generate_cloud_config
from hostname_generator import generate_hostnames
from projectmapper import get_rancher_projects, get_registration_url
from vmdeploy import generate_vm_deploy_command, execute_vm_deploy_command

if __name__ == "__main__":
    # Logging
    if getenv('DEBUG') == "True":
        logging.basicConfig(level=10)
    # Define variables
    # for generating host names
    number_of_hosts = getenv('NUMBER_OF_NEW_HOSTS')
    rancher_environment = getenv('RANCHER_ENVIRONMENT')
    rancher_auth = (getenv('RANCHER_ACCESS_KEY'), getenv('RANCHER_SECRET_KEY'))
    rancher_url = getenv('RANCHER_URL', 'https://console.ciscocrate.com/v2-beta')
    verify_ssl = True

    # For cloud-configs and commands
    region = getenv('NEW_HOST_REGION')
    ram = getenv('NEW_HOST_RAM')
    cpu = getenv('NEW_HOST_CPU')
    hdd = getenv('NEW_HOST_HDD')

    # VM Deploy Credentials
    vm_user = getenv('VMDEPLOY_USER')
    vm_pass = getenv('VMDEPLOY_PASS')

    # Generate the Hostnames

    # generate_hostnames(<name of environment>, <number of hosts to create>)
    host_ids = generate_hostnames(rancher_environment, number_of_hosts)

    # Return the Registration URL

    # get_rancher_projects(<Rancher API endpoint>, <Rancher_Api_Keys as tuple>, <use_ssl? true/false>)
    projects = get_rancher_projects(rancher_url, rancher_auth, verify_ssl)
    registration_url = get_registration_url(rancher_url, rancher_auth, verify_ssl, projects, rancher_environment)

    # Pass in the generated list of Hostname and UUID's
    new_host_dictionary = parse_hostname_list(host_ids)

    # Create the cloud-configs
    generate_cloud_config(new_host_dictionary, region, registration_url)

    # Build the VM Deploy Commands
    generate_vm_deploy_command(new_host_dictionary, region, rancher_environment, ram, cpu, hdd, vm_user,
                               vm_pass)

    # Execute the VM Deploy commands
    print("~~~~~executing VM Deploy commands~~~~")
    execute_vm_deploy_command(base_directory='/app/vmdeploy/commands/', file_match='*/vmdeploy.sh')
