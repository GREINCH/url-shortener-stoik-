# Virtual Machine Setup and FastAPI Cluster Deployment using Kind
This README provides step-by-step instructions on setting up a virtual machine (VM) in VirtualBox, configuring networking, and deploying a FastAPI application using Kind in different configurations (NodePort, Port Forwarding, and Ingress).

## Prerequisites
* VirtualBox installed on your host machine.
* Ubuntu Server (Live Server) ISO image.
* Host machine with internet access.
## 1. Create the VM in VirtualBox
####  System Specifications
* RAM: 4096 MB
* CPU: 2 cores
* Disk: Minimum 25 GB
#### Installation Steps
* Download Ubuntu Server ISO: Ensure you use the Live Server version (not Desktop) for better performance.
* Create a new VM: In VirtualBox, create a new VM and select the downloaded Ubuntu ISO as the boot medium.
* Network Configuration: Set the network adapter to 'Bridged Adapter'. This configuration makes the VM act as an isolated entity within your LAN, similar to a production environment setup.
* For Ethernet, choose enx or enp0.
* For Wi-Fi, choose wlp0.
## 2. Ubuntu Installation
* Install Minimal Ubuntu: During the installation process, select only the OpenSSH server and exclude additional software to conserve disk space. Snap packages, if not necessary, should be avoided as they consume significant space.
* Start VM in Headless Mode: Once the installation is complete, run the VM in headless mode for better performance and resource management.
## 3. Configuration on Host Machine
#### Identify IP Addresses:

* Use ifconfig or ip a on your host to identify its IP address.
* Similarly, identify the VM's IP address; it usually starts with enx....
#### SSH into the VM:
* Ensure OpenSSH server is installed on your host.
* Use an SSH client like Termius to connect to the VM using its IP, username, password, and port 22.
## 4. Software Installation on VM
#### Install Necessary Tools:
* Docker
* Git
* Kind
* kubectl
#### Setup GitHub SSH Keys:
* Generate an SSH key and add it to your GitHub account settings.
   ```
    ssh-keygen -t ed25519 -C "kxierg@gmail.com"
   ```
* Verify the connection using:
   ```
    ssh -T git@github.com.
   ```
#### Clone and Deploy FastAPI Application:
* Clone your repository (e.g., git clone git@github.com:GREINCH/url-shortener-stoik-.git).
* Follow the project-specific README to build the Docker image and run the Docker container.
## 5. Accessing FastAPI Application
Example: http://192.168.1.21/docs

