import mysql.connector as mariadb
#import MySQLdb as mariadb

db_user = '<username>'
db_passwd = '<password>'
db_name = 'd0020e'

def connect():
    con =  mariadb.connect(host="127.0.0.1",user=db_user,password=db_passwd,database=db_name)
    cur = con.cursor()
    return (con,cur)



#Make function to save any object?
'''
def save(obj):
    obj.save()
    con.commit()

'''
