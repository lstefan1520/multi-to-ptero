from mysql_cred import *

def get_multi_server(mc_daemon, mc_server):
    get_server = "SELECT * FROM server WHERE daemon_id = %s AND id = %s"
    mycursor.execute(get_server, (mc_daemon, mc_server))
    result = mycursor.fetchall()
    if mycursor.rowcount == 0 or mycursor.rowcount > 2:
        exit("No server found")
    return result

def get_multi_email(mc_server):
    get_user_id = "SELECT * FROM user_server WHERE server_id = %s"
    mycursor.execute(get_user_id, (mc_server,))
    result = mycursor.fetchall()
    if mycursor.rowcount == 0 or mycursor.rowcount > 2:
        exit("No user ID found from server ID")
    user_id = result[0][0]

    # get email address with user id
    get_email = "SELECT * FROM user WHERE id = %s"
    mycursor.execute(get_email, (user_id,))
    result = mycursor.fetchall()
    if mycursor.rowcount == 0 or mycursor.rowcount > 2:
        exit("No email address from user ID")
    user_email = result[0][3]
    return user_email

def get_multi_db(mc_server):
    get_multi_db = "select * from mysql_db where server_id = %s"
    mycursor.execute(get_multi_db, (mc_server,))
    result = mycursor.fetchall()
    if mycursor.rowcount == 0:
        return "0"
    elif mycursor.rowcount == 1:
        return result[0][1], result[0][2]
    else:
        exit("Unknown error at database")
