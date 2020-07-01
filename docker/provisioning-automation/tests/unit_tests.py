#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import sys
import os
import mock
from requests import Session

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../app/'))

@mock.patch('requests.post')
def test_generate_hostnames(mocked_post):
    import hostname_generator

    json = [{'id': 'uuid-1'}]
    rancher_env = 'environment'
    number_of_hosts_to_create = 1

    mocked_post.return_value.json.return_value = json
    json_resp = hostname_generator.generate_hostnames(rancher_env, number_of_hosts_to_create)

    assert json_resp == json

@mock.patch.object(Session, 'get')
def test_get_rancher_projects(mocked_get):
    import projectmapper

    rancher_url = 'https://rancher.com'
    rancher_auth = ('key', 'pass')
    verify_ssl = True

    mocked_get.return_value.json.return_value = {'data': [{'name': 'project-1', 'id': 'project-id-1', 'state': 'active'}]}
    result = projectmapper.get_rancher_projects(rancher_url, rancher_auth, verify_ssl)

    assert result == {'project-1': 'project-id-1'}

@mock.patch.object(Session, 'get')
def test_get_registration_url(mocked_get):
    import projectmapper

    registration_url = 'http://registration.com'
    rancher_url = 'https://rancher.com'
    rancher_auth = ('key', 'pass')
    verify_ssl = True
    projects = {'project-1': 'project-id-1'}
    environment = 'project-1'

    mocked_get.return_value.json.return_value = {'data': [{'registrationUrl': registration_url}]}
    result = projectmapper.get_registration_url(rancher_url, rancher_auth, verify_ssl, projects, environment)

    assert result == registration_url

def test_parse_hostname_list():
    import uuid
    import generate_cloud_config

    name = 'project-1'
    id = str(uuid.uuid1())
    host_ids = [{'name': name, 'id': id}]

    result = generate_cloud_config.parse_hostname_list(host_ids)

    assert result[name] == id.replace('-', '')

def test_generate_cloud_config():
    import uuid
    from jinja2 import Environment, FileSystemLoader
    import generate_cloud_config

    name = 'project-1'
    id = str(uuid.uuid1()).replace('-', '')
    new_host_dict = {(name): id}
    region = 'RTP'
    registration_url = 'http://registration.com'
    file_loader = FileSystemLoader('/app/templates')
    env = Environment(loader=file_loader)
    template = env.get_template('cloud-config.tmpl')

    generate_cloud_config.generate_cloud_config(new_host_dict, region, registration_url)

    assert os.path.isfile(f'/app/assets/config/hostname/{id}.crate.cisco.com/cloud-config.yml')
    assert open(f'/app/assets/config/hostname/{id}.crate.cisco.com/cloud-config.yml', 'r').read() == template.render(registration_url=registration_url, crate_hostname=name,
                                              crate_region=generate_cloud_config.regions[region])

def test_generate_vm_deploy_command():
    import uuid
    from jinja2 import Environment, FileSystemLoader
    import vmdeploy

    name = 'project-1'
    id = str(uuid.uuid1()).replace('-', '')
    new_host_dict = {(name): id}
    region = 'RTP'
    environment = 'env'
    ram = 2
    cpu = 2
    hdd = 'hdd'
    vm_user = 'user'
    vm_pass = 'pass'
    file_loader = FileSystemLoader('/app/templates')
    env = Environment(loader=file_loader)
    template = env.get_template('vmdeploy-command.tmpl')

    vmdeploy.generate_vm_deploy_command(new_host_dict, region, environment, ram, cpu, hdd, vm_user, vm_pass)

    assert os.path.isfile(f'/app/vmdeploy/commands/{id}/vmdeploy.sh')
    assert open(f'/app/vmdeploy/commands/{id}/vmdeploy.sh').read() == template.render(vm_user=vm_user, vm_pass=vm_pass, datacenter=vmdeploy.datacenters[region], environment=environment,
                                                                                                       host_uuid=id, host_name=name, num_cpus=cpu, total_ram=ram * 1028,
                                                                                                       hdd_size=hdd)
@mock.patch('subprocess.check_call')
def test_execute_vm_deploy_command(mocked_check_call):
    import subprocess
    import uuid
    from pathlib import Path
    import vmdeploy

    id = str(uuid.uuid1()).replace('-', '')
    command = f'/app/vmdeploy/commands/{id}/vmdeploy.sh'
    os.makedirs(os.path.dirname(command))
    Path(command).touch()
    vmdeploy.execute_vm_deploy_command(base_directory='/app/vmdeploy/commands/', file_match='*/vmdeploy.sh')

    mocked_check_call.assert_called_with(f'sh {command}', shell=True)