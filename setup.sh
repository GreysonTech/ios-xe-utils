#!/bin/bash


# Simple shell script used by Vagrant to provision Ubuntu 18.04 LTS server
# as a development environment.
#
# The provisioning flow was adapted from Cisco's DevNet setup of a local
# development environment to use while following their Learning Labs.
# https://developer.cisco.com/learning-labs/setup/
#
# Included is the initial setup of YangExplorer,
# based on their installation instructions.
# https://github.com/CiscoDevNet/yang-explorer


echo ""
echo " ***** Begin shell provisioning script ***** "
echo ""

# Update system and install utilities
sudo apt-get update -y
sudo apt-get install curl -y
sudo apt-get install libssl-dev -y
sudo apt-get install build-essential -y
sudo apt-get install moreutils -y
sudo apt-get install git -y
sudo apt-get install python2.7 -y

# Add Python 2.7 alias to the bash shell
echo "" >> ~/.bashrc
echo "# aliases added during vagrant provisioning" >> ~/.bashrc
echo "alias python2='python2.7'" >> ~/.bashrc
source ~/.bashrc

# Install pip for Python 2.7
sudo apt-get install python-pip -y

# Install pip for Python 3.X
sudo apt-get install python3-pip -y

# Install virtualenv
pip install virtualenv
pip install --upgrade pip
pip3 install --upgrade pip
sudo apt-get install python3-venv -y

# Create default virtual environments
cd /home/vagrant
python2 -m virtualenv py2-venv
python3 -m venv py3-venv

# Install Node
sudo apt-get install nodejs -y
sudo apt-get install npm -y

# Install Docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt update -y
sudo apt install docker-ce -y
sudo usermod -aG docker $USER

# Install Ansible
echo "" >> /etc/apt/sources.list
echo "# ansible ppa" >> /etc/apt/sources.list
echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu bionic main" >> /etc/apt/sources.list

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
sudo apt update -y
sudo apt install ansible -y

# Install YANG Explorer dependencies
sudo apt-get install graphviz -y
sudo apt-get install libxml2-dev libxslt1-dev python-dev zlib1g-dev -y

# Clone Yang Explorer repository
cd /home/vagrant
git clone https://github.com/CiscoDevNet/yang-explorer.git

# Activate Python 2 venv and start YANG Explorer setup script
cd yang-explorer
python2 -m virtualenv yang-venv
source yang-venv/bin/activate
bash setup.sh -y
sudo sed -i "s/'localhost'/\$(ifdata -pa enp0s3)/" start.sh

echo ""
echo " ***** Provisioning script complete ***** "
echo ""