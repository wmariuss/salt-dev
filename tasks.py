import os.path
from invoke import task
from time import sleep

package_name = 'tests-env'


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
def install(c):
    c.run("sudo apt-get update")
    # Install LXD >= 3.0
    c.run("sudo apt-get install -y lxd lxd-client")
    # Generate test SSH keys
    c.run("ssh-keygen -t rsa -N '' -f $HOME/.ssh/id_rsa")


@task
def remove(c):
    c.run("sudo apt remove -y lxd lxc lxd-client")
    c.run("sudo apt purge -y lxd lxc lxd-client")
    c.run("sudo apt autoremove -y")


@task
def setup(c):
    init = "lxd/lxd-init.yml"
    default = "lxd/default-profile.yml"

    print('Setup...')
    c.run("lxd init --auto")

    if os.path.isfile(init):
        c.run("lxd init --preseed < {}".format(init))

    if os.path.isfile(default):
        sleep(5)
        c.run("lxc profile edit default < {}".format(default))
