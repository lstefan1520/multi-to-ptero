from functions.ptero_api import *
from functions.whmcs_api import *
from functions.multi_api import *
import os

# Multicraft Daemon ID
mc_daemon = 
mc_server = # Multicraft server ID

# Multicraft & Pterodactyl Customer Database Info
# used for migrating dbs from multi -> ptero
multi_client_db = ""
# for now we are going to use the same database host
ptero_client_db = ""

# Product IDs, used for migrating product services on WHMCS
# Format: multicraft_product_id: pterodactyl_product_id
product_ids = {
  "2": "204", # Sand (1GB)	
  "3": "", # Dirt (1.5GB)
  "4": "", # Grass (2GB) 
  "5": "", # Cobblestone (2.5GB)
  "6": "", # Stone (3GB)
  "7": "", # Iron (4GB)
  "8": "", # Gold (5GB)
  "9": "", # Diamond (6GB)
  "10": "", # Quartz (7GB)
  "11": "", # Obsidian (8GB)
  "12": "", # Endstone (10GB)
  "13": "", # Bedrock (16GB)
}

# Pterodactyl API Information
ptero_api_host = "" # web URL for ptero. DO not include trailing slash
ptero_api_key = "" # API Token

# Egg information
ptero_nest_id = "1"
ptero_egg_id = "3"


## Start of code
# Get server info
mc_server_info = get_multi_server(mc_daemon, mc_server)

mc_id = mc_server_info[0][0]
mc_name = mc_server_info[0][1]
mc_ip = mc_server_info[0][2]
mc_port = mc_server_info[0][3]
mc_memory = mc_server_info[0][7]
mc_jar = mc_server_info[0][9]

print("-------------------------------------------------------")
print("Server ID: " + str(mc_id))
print("Server Name: " + mc_name)
print("Server IP: " + mc_ip)
print("Server Port: " + str(mc_port))
print("Server Memory: " + str(mc_memory))
print("Server Jar: " + mc_jar)
print("-------------------------------------------------------" + "\n")
print("Starting Migration..." + "\n")


# Create server on Pterodactyl

## Create allocation on node
con_create_allocation(ptero_api_host, ptero_api_key, "2", mc_ip, str(mc_port))
## Get allocation ID for newly created server
alloc_id = con_get_allocation_id(ptero_api_host, ptero_api_key, "2", mc_ip, str(mc_port))
print("[INFO] Allocation ID for Ptero IP: " + str(alloc_id))

## Get email address from MC server
user_email = get_multi_email(str(mc_id))
print("[INFO] Found multicraft user email: " + user_email)

## Get user's first & last name from WHMCS
first_last = get_whmcs_name(user_email)
print("[INFO] User's full name: " + first_last[0] + " " + first_last[1] + "\n")

## Create pterodactyl user
con_user_create(ptero_api_host, ptero_api_key, user_email, first_last[0], first_last[1])
# TODO: Check if password reset sends

## Get pterodactyl user ID
ptero_user_id = con_get_user_id(ptero_api_host, ptero_api_key, user_email)

## Create pterodactyl server
pteroId = con_create_server(ptero_api_host, ptero_api_key, mc_name, ptero_user_id, ptero_nest_id, ptero_egg_id, mc_memory, "1024", "0", "500", "0", "3", "3", "3", alloc_id)

## Migrate server files
print("\nThe server files are about to be migrated. Please ensure the following parameters are correct.\n")
print("Migrating Server ID: " + str(mc_server) + " to Ptero ID" + str(pteroId[0]))
print("Migration Command: cd /home/minecraft/multicraft/servers/server" + str(mc_server) + " && mv * /var/lib/pterodactyl/volumes/" + str(pteroId[0]))
q1 = input("\nConfirm this command with yes or no: ")
if q1 != "yes":
    exit("Exiting per request")

# Migrate files
os.popen("mv /home/minecraft/multicraft/servers/server" + str(mc_server) + "/* /var/lib/pterodactyl/volumes/" + str(pteroId[0]))
print("\n[INFO] Migrated server files succesfully!")

## Migrate created databases
# check if server has database on multicraft
print("[INFO] Checking if server has any databases...")
dbs = get_multi_db(mc_server)
if dbs != 0:
    print("\n[INFO] Creating new database on pterodactyl")
    db_info = create_ptero_db(ptero_api_host, ptero_api_key, dbs[0], pteroId[2], "2")

    # Dump database from multi host
    os.popen("mysqldump --column-statistics=0 -h " + multi_client_db + " -u " + dbs[0] + " -p'" + dbs[1] + "' " + dbs[0] + " > " + dbs[0] + ".sql").read()

    # Import into ptero host
    os.system("./import_db.sh " + str(db_info[1]) + " " + str(ptero_client_db) + " " + "'" + str(db_info[2]) + "'" + " " + str(db_info[0]) + " " + str(dbs[0]) + ".sql")

    # clean up
    os.popen("rm -f " + dbs[0] + ".sql")
    print("\n[INFO] Imported database data for " + dbs[0] + " succesfully!")

# Update WHMCS Information
print("\n[INFO] Updating WHMCS information...")
whmcs_user_id = get_whmcs_user_id(user_email)
if whmcs_user_id == "skip":
    print("[INFO] Skipping WHMCS product update...")
else:
    full_ip = str(mc_ip) + ":" + str(mc_port)
    whmcs_service_id = whmcs_service_id(whmcs_user_id, full_ip)
    whmcs_product_id = whmcs_product_id(whmcs_service_id)
    if whmcs_service_id != "error":
        # Get new product ID from dict
        match = "false"
        new_product_id = ""
        for key, value in product_ids.items():
            if str(key) == str(whmcs_product_id):
                new_product_id = value
                match = "true"
                break
        if match != "true":
            print("[ERROR] Could not find new product ID for server " + str(mc_server))
        else: 
            # Update WHMCS product
            update_whmcs_product_id(whmcs_service_id, new_product_id)
            # Update domain field on WHMCS (PloxHost Specific)
            update_whmcs_domain(whmcs_service_id, full_ip, pteroId[3], mc_server)
            print("[INFO] Updated WHMCS product succesfully!")

print("-------------------------------------------------------")
print("Migration Complete! Summary:")
print("Server ID: " + str(mc_server) + " -> " + str(pteroId[0]))
print("Service IP: " + str(mc_ip) + ":" + str(mc_port))
print("-------------------------------------------------------")
