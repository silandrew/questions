# RHCSA 9 Automated Practice Deployment

Vagrant lab for practising for the rhcsa 9. 

# How to use this lab
1. Install virtualbox (if needed)
2. Install vagrant (if needed)
3. Clone this repo
4. Download the rhel 9 dvd iso into the same directory (!this is not the latest version!) https://developers.redhat.com/content-gateway/file/rhel-baseos-9.0-x86_64-dvd.iso
5. Create python virtual env `virtualenv venv`, activate `source venv/bin/activate` and install requirements `pip install -r requirements.txt`.
6. Run `vagrant up` inside this directory
    
The vagrant script will set up three RHEL9.0 VMs: repo, server1 and server2. 
Repo will mount the dvd iso and use this for its own repo to use.
It will also run an Apache web server serving the BaseOS and AppStream repos which are used by the server1 and server2 VMs.

Execute one of the following commands to connect with the VMs:

`vagrant ssh repo`

`vagrant ssh server1`

`vagrant ssh server2`

## Lab Setup
The lab consists of three servers, all RHEL 9.0 minimal installations, which consist of one repo server and two exam servers. Once setup, the repo server should be left untouched, except for running a quick permissions reset on the NFS shares when resetting the lab.

Servers in my lab setup are on the following IPs:

- Repo: 192.168.99.9
- Server1: 192.168.99.10
- Server2: 192.168.99.11

Once the exam servers are setup, a VM snapshot should be taken. After running through the tasks in the task list, the VM snapshots can be rolled back to run through it all again.

### Yum repositories
The repositories are available at the following addresses:
- [BaseOS] (http://repo.rhcsa.example.com/BaseOS)
- [AppStream] (http://repo.rhcsa.example.com/AppStream)

### NFS share
The NFS share are available at the following address:
- repo.rhcsa.example.com:/user-homes/op01

Access granted to user with uid 1001 and gid 1001.
