#!/bin/bash

set -e

export DEBIAN_FRONTEND=noninteractive

PYTHON_VERSION='python3.6'
PIP_VERSION='pip3'
VAGRANT_PROJECT_DIR='/opt/saltd'

# Install global dependencies
sudo apt-get update
sudo apt-get install -y python3-pip

# Make python 3.6 as default one
sudo ln -sfn /usr/bin/${PYTHON_VERSION} /usr/bin/python
sudo ln -sfn /usr/bin/${PIP_VERSION} /usr/bin/pip

# Be sure we have python 3.6
sudo update-alternatives --install /usr/bin/python python /usr/bin/${PYTHON_VERSION} 1

# Install pip dependencies
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
