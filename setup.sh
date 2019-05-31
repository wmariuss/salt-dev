#!/bin/bash

set -e

export DEBIAN_FRONTEND=noninteractive

VAGRANT_PROJECT_DIR='/opt/saltd'

# Install global dep
sudo apt-get update
sudo apt-get install -y python3-pip
sudo ln -sfn /usr/bin/python3.6 /usr/bin/python
sudo ln -sfn /usr/bin/pip3 /usr/bin/pip

pip install pipenv

# Install saltd dep
if [ -d $VAGRANT_PROJECT_DIR ];
then
    cd $VAGRANT_PROJECT_DIR
fi

pipenv install
pipenv run invoke install --lxd --salt

echo "========================================"
echo "Read the README doc for more information"
echo "========================================"

if [ -d $VAGRANT_PROJECT_DIR ];
then
    echo "Now type 'vagrant ssh'"
fi
