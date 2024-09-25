# multi-to-ptero
A project to help easily migrate servers from Multicraft to Pterodactyl Panel

! Use this script at YOUR own risk. We have heavily tested everything here, however I can not guarantee anything. 

## Features of this script
- Migrate server data (user accounts, server files, allocation/ip assignment, server databases) 
- Update WHMCS info with new data (For hosting providers, can be disabled)

## How to use
- Install mysql, python3, mysql cli, pip3
- Update all variables within main.py & mysql_cred.py. (ie mysql info, ptero api, multi server ids, etc.)
- Disable WHMCS features if need be, you can simply comment out the lines in the main.py file
- Ensure that you have created the pterodactyl node on pterodactyl, using the same exact ID as the Multicraft Node ID
- Make modifications as needed.
