# salt-dev

Create environments automatically for salt development and testing.

## Requirement

* `Python 2.7`

## Install

1. Clone the repository
2. `pip install -r requirements.txt`

## Usage

* `invoke install` - Install LXD/LXC and create default SSH key
* Add public key (`$HOME/.ssh/id_rsa.pub`) in `lxd/default-profile.yml` and then run `invoke setup` for update the default profile (containers profile)
* Change `settings.yml` and `salt/minion.conf` file as you want and then run `./run.py`

## Parameters

* create - 'yes' create containers, 'no' destroy all containers
* container_config - based on this file, containers are created
* containers - how many containers to create
* salt_setup - enbale salt setup for containers
* salt_version - salt minor release version
* ssh_user - SSH user

## Authors

Marius Stanca - <me@marius.xyz>