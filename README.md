# saltd

Create environments automatically for salt development and testing.

## Requirement

* `Python >= 3.5`
* `Ubuntu >= 18.04`
* `salt-master`, this must have the same version as `salt-minion` that is installed on container(s)

## Install

* `pip install pipenv`
* `pipenv install`

## Usage

* Run `pipenv run invoke install`, this install `lxd/lxc` and create default SSH key
* Add created public key (ex.`$HOME/.ssh/id_rsa.pub`) in `lxd/default-profile.yml`
* Run `pipenv run invoke setup` for update the default profile (containers profile)
* Change `settings.yml` and `salt/minion.conf` file as you want
* Run `pipenv run ./run.py`

## Parameters (settings.yaml)

| Parameter | Description | Example | Default |
|-----------|-------------|---------|---------|
| create | Create/Destroy all containers | `yes`/`no` | |
| container_config | Containers are created based on this file | `container_config.json` | |
| containers | Number of containers you want to create | | `1` |
| salt_setup | Enbale salt setup for containers | `yes`/`no` | `no` |
| salt_version | What version for salt you want to use | `2017.7.2` | `2018.3.2` |
| ssh_user | SSH user | | `ubuntu` |
| ssh_private_key| SSH private key | `/root/.ssh/id_rsa` | |

Note: Container OS is `Ubuntu 16.04`

## Authors

* [Marius Stanca](mailto:me@marius.xyz)
