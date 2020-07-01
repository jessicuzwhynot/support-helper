from jinja2 import Environment, FileSystemLoader
from os import path, makedirs
from pathlib import Path
import subprocess

def generate_vm_deploy_command(new_host_dict, region, environment, ram, cpu, hdd, vm_user, vm_pass):
    ram = int(ram) * 1028
    file_loader = FileSystemLoader('/app/templates')
    env = Environment(loader=file_loader)
    for key in new_host_dict.keys():
        template = env.get_template('vmdeploy-command.tmpl')
        datacenter = datacenters[region]
        crate_hostname = key
        crate_uuid = new_host_dict[key]
        output = template.render(vm_user=vm_user, vm_pass=vm_pass, datacenter=datacenter, environment=environment,
                                 host_uuid=crate_uuid, host_name=crate_hostname, num_cpus=cpu, total_ram=ram,
                                 hdd_size=hdd)
        if not path.isdir(f'/app/vmdeploy/commands/{crate_uuid}/'):
            makedirs(f'/app/vmdeploy/commands/{crate_uuid}')
        with open(f'/app/vmdeploy/commands/{crate_uuid}/vmdeploy.sh', 'w') as command:
            command.write(output)
    return

# For each generated command, use subprocess.run to execute the VM deploy command
def execute_vm_deploy_command(base_directory, file_match):
    p = Path(base_directory).glob(file_match)

    for command in p:
        subprocess.check_call(f'sh {command}', shell=True)
    return

# Set variables for the vSphere datacenter
datacenters = {
    "RTP": "RTP5",
    "SJC" : "SJCK",
    "GPK" : "GPK",
    "BGL" : "BGL"
}