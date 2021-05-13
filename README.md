# Platops CSV Erollment Validation

A python script that would verify the port status, BMC access and mac address matching from the csv generated file to the physical hardware NIC mac address.

## Prerequisites

* Python 3 installed
* Packet admin-vpn access

## Installation

1. Clone the repo 
```sh
git@github.com:packethost/platops-csv-validation.git
```
2. Install requirements, I highly suggest creating a python virtual env
```sh 
   pip install -r requirements
```
3. Create an ssh config in `~/.ssh/config` with below format
   ```
   Host *.packet.net
      User <username_accessing_switch> # dpinggoy
      IdentityFile ~/.ssh/id_rsa       # where your private key located
      StrictHostKeyChecking no
      TCPKeepAlive yes
      ServerAliveInterval 120
      ServerAliveCountMax 5
      UserKnownHostsFile /dev/null
      NoHostAuthenticationForLocalhost yes 
   ```
4. The script will run in this format with arguments.
```sh
    python3 plat-csv-validate.py -f "/path/file.csv" -v vendor
```
The vendor it could be `dell` this is still work in progress so we'll add more vendor along the way.