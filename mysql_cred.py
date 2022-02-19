import mysql.connector

# Multicraft Cred
mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)
mycursor = mydb.cursor()

# WHMCS Cred

mydb_whmcs = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)
mycursor_whmcs = mydb_whmcs.cursor()
