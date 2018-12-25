# chatter_app
The chatterbox app is a simple application to post and retrieve messages. The appliation exposes an Rest API to create users, post and retrieve messages.
The repo contains code for the application and ansible playbook to provision an ec2 instance on AWS and deploy the app in a Docker container in the ec2 instance.

## Requirements
### Control Machine Requirements
1. Ansible version 2.4 and later
2. python >= 2.6
3. boto python module

### EC2 Instance( Docker Host) Requirements
1. Ubuntu Server 18.04.1 LTS

### AWS VPC Requirements:
1. The VPC hosting the ec2 instance should have attributes enableDnsHostnames as true and enableDnsSupport as true (enables public dns assignment and resolution for the ec2 instance).

## Steps to build and deploy the app in a container
### Provision ec2 instance:
1. Clone the repository to the Ansible Control machine.
2. Set the following environment variables
```
aws_access_key_id = <your_access_key_here>
aws_secret_access_key = <your_secret_key_here>
```
3. Edit the provision/vars/ec2_vars.yml file to add your ec2 attributes
4. Switch to the provision/ folder and execute provison_ec2.yml
```ansible-playbook provison_ec2.yml```
5. Note the public ip/fqdn and instance details from the playbook output.

### Deploy application in a Docker container:
1. Edit the ansible inventory file provision/inventory/hosts to add the ec2 instance public_ip/fqdn.
2. The default port to access the app is 8080. Allow access for it in the AWS security group. Optionally, change the port by editing the docker_host_port variable in provision/deploy_app.yml
3. Switch to the provision/ folder and execute the deploy_app.yml with the ec2 private key file for the keypair used while provisioning the instance.
```ansible-playbook --private-key=</path/to/ec2_ppk_file>```

## Sequence Diagram

![image](https://drive.google.com/uc?export=view&id=1ci-Wq3uUjZdrcH5vEhSxI8NVRfo_raaY)

## API Documentation

[ Document Link ](https://documenter.getpostman.com/view/6237987/Rzn9rg1s)
