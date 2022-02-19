import mysql.connector
from mysql_cred import *

def get_whmcs_name(email):
    name = "SELECT * FROM tblclients WHERE email = %s"
    mycursor_whmcs.execute(name,(email,))
    result = mycursor_whmcs.fetchall()
    name_list = []
    if mycursor_whmcs.rowcount == 0 or mycursor_whmcs.rowcount > 2:
        print("[WARN] No user found, assuming data...")
        name_list.append("Migrated")
        name_list.append("User")
    else:
        name_list.append(result[0][2])
        name_list.append(result[0][3])

    return name_list

def get_whmcs_user_id(email):
    user_id = "SELECT * FROM tblclients WHERE email = %s"
    mycursor_whmcs.execute(user_id,(email,))
    result = mycursor_whmcs.fetchall()
    user_id = result[0][0]
    
    if mycursor_whmcs.rowcount == 0:
        print("[WARN] No WHMCS User account found for this service. Assuming no account exists. Skipping WHMCS Update...")
        return "skip"
    else:
        return user_id

def whmcs_service_id(user_id, multi_server_ip):
    whmcs_service_id = "SELECT * FROM tblhosting WHERE userid = %s AND dedicatedip = %s"
    mycursor_whmcs.execute(whmcs_service_id, (user_id, multi_server_ip))
    result = mycursor_whmcs.fetchall()
    if mycursor_whmcs.rowcount == 0 or mycursor_whmcs.rowcount > 2:
        print("[ERROR] No WHMCS service ID found for this service")
        print("[ERROR] Return to this after migration!")
        return "error"
    else:
        return result[0][0]

def whmcs_product_id(service_id):
    whmcs_product_id = "SELECT * FROM tblhosting WHERE id = %s"
    mycursor_whmcs.execute(whmcs_product_id, (service_id,))
    result = mycursor_whmcs.fetchall()
    if mycursor_whmcs.rowcount == 0 or mycursor_whmcs.rowcount > 2:
        print("[ERROR] No WHMCS product ID found for this service")
        print("[ERROR] Return to this after migration!")
        return "error"
    else:
        return result[0][3]

def update_whmcs_product_id(service_id, new_product_id):
    update_service_id = "UPDATE tblhosting SET packageid = %s WHERE id = %s"
    mycursor_whmcs.execute(update_service_id, (new_product_id, service_id))
    mydb.commit()
    
def update_whmcs_domain(service_id, full_ip, server_id, old_multicraft_id):
    update_whmcs_domain_field = "UPDATE tblhosting SET domain = %s WHERE id = %s"
    domain_field = str(server_id) + " - " + str(full_ip)
    mycursor_whmcs.execute(update_whmcs_domain_field, (domain_field, service_id))

    update_whmcs_notes = "UPDATE tblhosting SET notes = %s WHERE id = %s"
    domain_field = "Migrated from Multicraft to Pterodactyl:\n Multicraft ID: " + str(old_multicraft_id) + "\nPterodactyl ID: " + str(server_id)
    mycursor_whmcs.execute(update_whmcs_notes, (domain_field, service_id))
    mydb.commit()
