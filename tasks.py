import os.path
from invoke import task
from time import sleep
import yaml

from run import validate_settings_file

settings = validate_settings_file('settings.yml')


@task
def clean(c):
    patterns = [
            'build',
            'dist',
            '__pycache__',
            '*.pyc',
            '*.egg-info'
            ]
    print("Cleaning up...")
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))


@task
def install(c, lxd=False, salt=False):
    salt_version = settings.get('salt_version', '2018.3.2')
    os_version = settings.get('os_version', '18.04')
    os_codename = settings.get('os_codename', 'bionic')

    if lxd:
        print("Installing LXD...")
        c.run("sudo apt-get update")
        # Install LXD >= 3.0
        c.run("sudo apt-get install -y lxd lxd-client")
        # Generate test SSH keys
        c.run("ssh-keygen -t rsa -N '' -f $HOME/.ssh/id_rsa")
    if salt:
        print("Installing salt-master...")
        master_config_file = 'salt/master/base.conf'

        c.run("wget -O - https://repo.saltstack.com/apt/ubuntu/{}/amd64/archive/{}/SALTSTACK-GPG-KEY.pub | sudo apt-key add -".format(os_version, salt_version))
        c.run("sudo echo deb http://repo.saltstack.com/apt/ubuntu/{}/amd64/archive/{} {} main > /etc/apt/sources.list.d/saltstack.list".format(os_version,
                                                                                                                                               salt_version,
                                                                                                                                               os_codename))
        c.run("sudo apt-get update")
        c.run("sudo apt-get install -y salt-master")
        c.run("sudo mkdir -p /srv/salt")
        c.run("sudo mkdir -p /srv/pillar")
        if os.path.isfile(master_config_file):
            c.run("sudo cp {} /etc/salt/master.d/".format(master_config_file))
            c.run("sudo systemctl restart salt-master.service")
        else:
            print('There is not salt master config file. Please take a look at {}'.format(master_config_file))

    c.run("sudo apt-get autoremove -y")


@task
def remove(c, lxd=False, salt=False):
    if lxd:
        print("Removing LXD...")
        c.run("sudo apt-get remove -y lxd lxc lxd-client")
        c.run("sudo apt-get purge -y lxd lxc lxd-client")
    if salt:
        print("Removing salt-master...")
        c.run("sudo apt-get remove -y salt-master")
        c.run("sudo apt-get puge -y salt")
    c.run("sudo apt-get autoremove -y")


@task
def setup(c, lxd=False, salt=False):
    if lxd:
        init = "lxd/lxd-init.yml"
        default = "lxd/default-profile.yml"

        print('Setup...')
        c.run("lxd init --auto")

        if os.path.isfile(init):
            c.run("lxd init --preseed < {}".format(init))

        if os.path.isfile(default):
            sleep(5)
            c.run("lxc profile edit default < {}".format(default))
    if salt:
        pass
