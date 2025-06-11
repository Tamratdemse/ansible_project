Ansible 3-Tier Application Deployment
This Ansible project automates the provisioning and deployment of a 3-tier application infrastructure across multiple Virtual Machines (VMs). It sets up a dedicated frontend server, a backend web server (Node.js + Nginx), and a MongoDB database server.

🚀 Project Overview
This repository contains Ansible playbooks and roles designed to:

Provision a Frontend Server: Install Git and clone a specified frontend application repository.

Provision a Web Server: Install Nginx, set up a Node.js runtime environment, and clone the backend application.

Provision a Database Server: Install and configure MongoDB (version 4.4) for data storage.

The project leverages dotenv and Jinja2 templating to manage sensitive information (like VM IPs, usernames, and your control machine's IP) securely and dynamically, separating them from the main Ansible inventory file. Firewall rules (ufw) are also configured to secure inter-VM communication and restrict SSH access to only your control machine.

🏛️ Architecture
The deployment consists of three distinct Virtual Machines:

Frontend VM:

Purpose: Hosts the static or client-side application code.

Components: Git (for cloning the frontend repository), UFW (firewall).

Access: SSH allowed only from Control Machine.

Webserver VM:

Purpose: Hosts the backend API or server-side application logic.

Components: Nginx (as a reverse proxy or static file server), Node.js (runtime environment), Git (for cloning backend repo), UFW (firewall).

Access: SSH allowed only from Control Machine. HTTP/HTTPS allowed from Anywhere.

Database Server VM:

Purpose: Stores application data.

Components: MongoDB (version 4.4), UFW (firewall).

Access: SSH allowed only from Control Machine. MongoDB (port 27017) allowed only from Webserver VM.

Control Machine: Your local machine (DESKTOP-HDSMIOK in our context) where Ansible and Python are installed, and from where the playbooks are executed. Your control machine's IP (172.17.188.60) is used in firewall rules to allow SSH access.


3 Linux VMs:

One for Webserver (e.g., Ubuntu Server 20.04 LTS or 22.04 LTS).

One for DB Server (e.g., Ubuntu Server 20.04 LTS or 22.04 LTS).

One for Frontend Server (e.g., Ubuntu Server 20.04 LTS or 22.04 LTS).

Network Configuration: All VMs should be configured with a network adapter (e.g., NAT or Bridged) that allows them to receive SSH connections from your control machine and access the internet (for package downloads).

User Accounts: On each VM, create a non-root user (e.g., tamrat, tamrat2, tamrat3) with sudo privileges.

SSH Key-based Authentication: Crucially, set up passwordless SSH login from your control machine to each VM using ssh-copy-id.

⚙️ Setup and Deployment
1. Control Machine Setup
a. Clone the Repository
git clone https://github.com/your-username/your-ansible-project.git # Replace with your repo URL
cd your-ansible-project

b. Create a Python Virtual Environment (Recommended)
python3 -m venv venv
source venv/bin/activate

c. Install Python Dependencies
pip install ansible python-dotenv Jinja2

d. Create the .env file
This file will store your VM IPs and usernames. Do NOT commit this file to Git.
Create a file named .env in the root of your ansible_project directory:

Your Webserver VM's IP
Your Webserver VM's username
Your DB Server VM's IP
Your DB Server VM's username
Your Frontend Server VM's IP
Your Frontend Server VM's username

e. Ensure inventory/hosts.ini.j2 is Correct
This template uses the variables from your .env file. Confirm its content:

[webservers]
{{ webserver_ip }} ansible_user={{ webserver_user }}

[dbservers]
{{ dbserver_ip }} ansible_user={{ dbserver_user }}

[frontend]
{{ frontend_ip }} ansible_user={{ frontend_user }}

[all:vars]
ansible_python_interpreter={{ python_path }}
control_machine_ip={{ CONTROL_MACHINE_IP }}

f. Generate inventory/hosts.ini
Run the provided Python script to generate your Ansible inventory file:

python generate_hosts.py

This will create (or overwrite) inventory/hosts.ini.



🧩 Ansible Roles
webserver:

Updates apt cache.

Installs Nginx.

Installs curl (prerequisite for NodeSource).

Downloads and runs the Node.js 18.x setup script from NodeSource.

Installs Node.js and npm.

Clones the IOT-Back-End repository to /opt/iot_backend_app.

Firewall: Installs UFW, resets rules, sets default policies (deny incoming, allow outgoing), allows SSH (port 22) ONLY from control_machine_ip, allows HTTP (80) and HTTPS (443) from anywhere, then enables UFW.

dbserver:

Updates apt cache.

Installs gnupg and curl.

Imports the MongoDB 4.4 public GPG key.

Adds the MongoDB 4.4 repository.

Installs mongodb-org (MongoDB 4.4 server and associated tools).

Enables and starts the mongod service.

Firewall: Installs UFW, resets rules, sets default policies (deny incoming, allow outgoing), allows SSH (port 22) ONLY from control_machine_ip, allows MongoDB (port 27017) ONLY from the Webserver VM (192.168.236.117), then enables UFW.

frontend:

Updates apt cache.

Installs git.

Clones your frontend application repository (replace placeholder URL) into /var/www/frontend_app.

Firewall: Installs UFW, resets rules, sets default policies (deny incoming, allow outgoing), allows SSH (port 22) ONLY from control_machine_ip, then enables UFW.
NOTE: If your frontend application needs to be served via HTTP/HTTPS, you will need to add explicit ufw allow rules for ports 80/443 (or other ports) as needed.

✅ Verification
After the playbook completes, you can log into each VM and verify the deployments:

Webserver VM (192.168.236.117):

ssh tamrat@192.168.236.117
sudo systemctl status nginx
node -v
npm -v
ls -l /opt/iot_backend_app # Verify cloned backend files
sudo ufw status verbose # Check firewall rules
exit

DB Server VM (192.168.236.12):

ssh tamrat2@192.168.236.12
sudo systemctl status mongod
mongosh # To enter MongoDB shell, type 'exit' to leave
sudo ufw status verbose # Check firewall rules
exit

Frontend Server VM (192.168.236.13):

ssh tamrat3@192.168.236.13
git --version
ls -l /var/www/frontend_app # Verify cloned frontend files
sudo ufw status verbose # Check firewall rules
exit
