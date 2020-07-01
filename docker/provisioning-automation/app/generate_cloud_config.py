from jinja2 import Environment, FileSystemLoader
from os import path, makedirs

# Separate out name and UUID from hostname_generator
def parse_hostname_list(host_ids):
    new_host_dict = {}
    for x in host_ids:
        new_host_dict[x['name']] = x['id'].replace('-', '')

    return new_host_dict

# Generate the cloud-config templates
def generate_cloud_config(new_host_dict, region, registration_url):
    file_loader = FileSystemLoader('/app/templates')
    env = Environment(loader=file_loader)
    for key in new_host_dict.keys():
        template = env.get_template('cloud-config.tmpl')
        registration_url = registration_url
        crate_hostname = key
        crate_region = regions[region]
        crate_uuid = new_host_dict[key] + '.crate.cisco.com'
        output = template.render(registration_url=registration_url, crate_hostname=crate_hostname,
                                 crate_region=crate_region)
        if not path.isdir(f'/app/assets/config/hostname/{crate_uuid}/'):
            makedirs(f'/app/assets/config/hostname/{crate_uuid}/')
        with open(f'/app/assets/config/hostname/{crate_uuid}/cloud-config.yml', 'w') as config:
            config.write(output)
    return

# Set variables for cloud-config region
regions = {
    "RTP": "csc-us-east-rtp5-2",
    "SJC" : "csc-us-west-sjck-1",
    "GPK" : "csc-eu-west-gpk-1",
    "BGL" : "csc-sa-west-bgl11-1"
}

