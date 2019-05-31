# saltd

Create environments automatically for salt development and testing.

## Requirement

* `Python >= 3.5`
* `Ubuntu >= 18.04`
* `salt-master` (same version as `salt-minion` that is installed on container(s))

## Install

* Run `./setup.sh`

Using vagrant

* `vagrant up`

## Usage

* Copy public key from `$HOME/.ssh/id_rsa` and add it `lxd/default-profile.yml` file
* Run `pipenv run invoke setup --lxd` for update the default profile (containers profile)
* Change `settings.yml` and `salt/minion.conf` files as you want
* Run `pipenv run ./run.py`

## Parameters (settings.yml)

| Parameter | Description | Example | Default |
|-----------|-------------|---------|---------|
| `create` | Create/Destroy all containers | `yes`/`no` | |
| `container_config` | Containers are created based on this file | `container_config.json` | |
| `containers` | Number of containers you want to create | | `1` |
| `salt_setup` | Enbale salt setup for containers | `yes`/`no` | `no` |
| `salt_version` | What version for salt you want to use | `2017.7.2` | `2018.3.2` |
| `ssh_user` | SSH user | | `ubuntu` |
| `ssh_private_key` | SSH private key | | `/root/.ssh/id_rsa` |
| `os_version` | OS version number | | `18.04` |
| `os_codename` | OS code name | | `bionic` |

Note: Container OS is `Ubuntu 16.04`

## Authors

* [Marius Stanca](mailto:me@marius.xyz)
