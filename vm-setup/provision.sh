#!/bin/bash

# Update packages
sudo apt-get update
sudo apt-get install -y net-tools git apt-transport-https ca-certificates curl software-properties-common

# Install Docker if it is not already installed
if ! type "docker" > /dev/null; then
  # Add Docker’s GPG key and repository
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  sudo apt-get update
  sudo apt-get install -y docker-ce
  sudo usermod -aG docker vagrant  # Allow Vagrant user to run Docker commands without sudo
fi

# Install kubectl and Kind if not already installed
if ! type "kubectl" > /dev/null; then
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
fi

if ! type "kind" > /dev/null; then
  curl -Lo ./kind "https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64"
  chmod +x ./kind
  sudo mv ./kind /usr/local/bin/kind
  # kind create cluster
fi

# Enable password authentication for SSH
echo "vagrant:vagrant" | sudo chpasswd  # Set the password for the 'vagrant' user

# Enable PasswordAuthentication and ChallengeResponseAuthentication
sudo sed -i 's/^#\\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/^#\\?ChallengeResponseAuthentication .*/ChallengeResponseAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/^#\\?PubkeyAuthentication .*/PubkeyAuthentication no/' /etc/ssh/sshd_config

sudo systemctl restart sshd

# Display the IP address and SSH connection details for Termius or other SSH clients
IP_ADDRESS=$(hostname -I | awk '{print $2}')
echo "To connect via Termius SSH, use the following details:"
echo "IP: $IP_ADDRESS"
echo "Username: vagrant"
echo "Password: vagrant"  # Display the password set above
