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
    if lxd:
        print("Installing LXD...")
        c.run("sudo apt-get update")
        # Install LXD >= 3.0
        c.run("sudo apt-get install -y lxd lxd-client")
        # Generate test SSH keys
        c.run("ssh-keygen -t rsa -N '' -f $HOME/.ssh/id_rsa")
    if salt:
        print("Installing salt...")
        python_version = 'python3.6'
        salt_version = settings.get('salt_version', '2018.3.4')
        salt_bootstrap = 'https://bootstrap.saltstack.com'
        master_config_file = 'salt/master/base.conf'
        minion_config_file = 'salt/minion.conf'

        # Install salt-master and minion
        c.run("curl -L {} -o install_salt.sh".format(salt_bootstrap))
        c.run("sudo sh install_salt.sh -M -x {} stable {}".format(python_version, salt_version))
        c.run("sudo rm install_salt.sh")

        # Configure salt
        c.run("sudo mkdir -p /srv/salt")
        c.run("sudo mkdir -p /srv/pillar")

        if os.path.isfile(master_config_file):
            c.run("sudo cp {} /etc/salt/master.d/".format(master_config_file))
            c.run("sudo systemctl restart salt-master.service")

            if os.path.isfile(minion_config_file):
                c.run("sudo cp {} /etc/salt/minion.d/".format(minion_config_file))
                c.run("sudo systemctl restart salt-minion.service")
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
def setup(c, lxd=False):
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
