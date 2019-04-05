#!/usr/bin/env python

import json
import yaml
from time import sleep
import ipaddress

from pssh.clients import ParallelSSHClient
from gevent import joinall
from pylxd import Client
from pylxd import exceptions


client = Client()

def validate_settings_file(file):
    settings = None
    with open(file, 'r') as paramters:
        try:
            settings = yaml.load(paramters)
        except yaml.YAMLError as err:
            raise err
    return settings


def list_containers():
    all_containers = client.containers.all()
    if all_containers:
        return [c.name for c in all_containers]
    return None


def get_info(container_name):
    container_info = None
    try:
        container_info = client.containers.get(container_name).state()
        if container_info:
            return container_info
    except exceptions.LXDAPIException as err:
        raise err


def get_ips():
    ipv4_list = []

    for container_name in list_containers():
        addresses = get_info(container_name).network
        print(addresses)
        interface = addresses['eth0']['addresses']

        if interface:
            for info in interface:
                if 'address' in info:
                    try:
                        ipaddress.IPv4Address(info['address'])
                        ipv4_list.append(info['address'])
                    except ipaddress.AddressValueError:
                        pass
    return ipv4_list


def validate_container_config(file):
    params = None

    with open(file, 'r') as stream:
        try:
            params = json.load(stream)
        except Exception as err:
            print(err)
    return params


def create_container(file, number):
    params = validate_settings_file(file)

    if params:
        name = params.get('name')

        for n in range(0, int(number)):
            new_name = {u'name': u'{}-{}'.format(name, n)}
            params.update(new_name)

            try:
                container = client.containers.create(params, wait=False)
                sleep(20)
                if list_containers():
                    container.start(wait=True)
            except exceptions.LXDAPIException as err:
                raise err


def delete_container(file):

    if list_containers():
        for c in list_containers():
            try:
                container = client.containers.get(c)
                if container:
                    container.stop()
                    sleep(10)
                    container.delete()
            except exceptions.LXDAPIException as err:
                raise err


def salt(setup, ssh_user, ssh_key, salt_version):
    hosts = get_ips()
    install_salt = ';'.join([
        'wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/archive/{}/SALTSTACK-GPG-KEY.pub | sudo apt-key add -'.format(salt_version),
        'echo deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/archive/{} xenial main > /etc/apt/sources.list.d/saltstack.list'.format(salt_version),
        'apt-get update',
        'apt-get install -y salt-minion',
        'apt-get autoremove -y',
        'cp /tmp/*.conf /etc/salt/minion.d/',
        'systemctl restart salt-minion.service'
    ])

    if setup.lower() == 'yes':
        sshc = ParallelSSHClient(hosts, user=ssh_user, pkey=ssh_key)
        cmd = sshc.run_command(install_salt, sudo=True)

        if len(hosts) >= 1:
            salt_conf_file = sshc.copy_file('salt', '/tmp', recurse=True)
            joinall(salt_conf_file, raise_error=True)

            for _, host_output in cmd.items():
                for line in host_output.stdout:
                    print(line)


if __name__ == '__main__':
    settings_file = 'settings.yml'
    settings = validate_settings_file(settings_file)

    if settings:
        create = settings.get('create')
        container_config = settings.get('container_config')
        number = settings.get('containers', 1)
        salt_setup = settings.get('salt_setup', 'no')
        ssh_user = settings.get('ssh_user', 'ubuntu')
        salt_version = settings.get('salt_version', '2018.3.2')
        ssh_key = settings.get('ssh_private_key')

        if create.lower() == 'yes':
            create_container(container_config, number)
            sleep(10)
            if ssh_key:
                salt(salt_setup, ssh_user, ssh_key, salt_version)
            else:
                print('Please specify ssh_private_key parameter in settings.yml file')
        else:
            delete_container(container_config)
