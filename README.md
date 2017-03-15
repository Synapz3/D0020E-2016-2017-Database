# Database for D0020E (Group 1) 2016/2017
This file will instruct you how to install and apply the solution for the database. We ran Debian 8.7 as our database server.
Instructions by: Synapz3
# update to latest version
```shell
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y
```
# Install the database (MariaDB)
```shell
sudo apt-get install software-properties-common
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
sudo add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://ftp.ddg.lth.se/mariadb/repo/10.1/debian jessie main'
sudo apt-get update
sudo apt-get install mariadb-server
```
Or follow [this link.](https://downloads.mariadb.org/mariadb/repositories/#mirror=lund&distro=Debian&distro_release=jessie--jessie&version=10.1)
Save the user that were created during setup. Flask will need this.

# install flask
Follow [this tutorial](http://flask.pocoo.org/docs/0.12/installation/) to install flask.
This is our script for installing flask with WSGI and python-connector:
```shell
sudo yum install epel-release
sudo yum install python-pip python-devel gcc nginx
sudo pip install virtualenv
vitualenv venv
source venv/bin/activate
pip install flask
pip install mysql-connector
pip install uwsgi
deactivate
chmod u+x start
```
The start file is a shortcut to activate venv and start flask. This also prints out any error that could occur.
# Setup uwsgi ini
1. Rename/copy uwsgi_config.ini.template to uwsgi_config.ini
2. Change the varibles bellow to suitable values in the ini file.
```
uid = [USER]
gid = [WEB-user]
```

# Run app on localhost
```
./start
```
# Install and point nginx to socket

Install and configure Nginx:
```shell
sudo apt-get isntall nginx -y
sudo vim /etc/nginx/sites-enabled/default
```
The file should look like this:
```shell
server {
    lsiten [PORTNUMBER]
    server_name _;
    
    location / {
        include uwsgi_params;
        uwsgi_pass unix:///<project dir>/main.sock;
    }
}
```
Restart the server once (or the services flask, wsgi and nginx).
```shell
sudo reboot
```

# Connect flask to MariaDB.
```shell
vim connect-to-database
```
Edit the file to use the user configured at the installation. For example:
```shell
mysql -u <MariaDB username> -p -h 127.0.0.1
```
Now go edit dbconnector.py in modules dir.
```shell
cd /modules
vim dbconnector.py
```
It should look something like this:
```shell
import mysql.connector as mariadb
#import MySQLdb as mariadb
db_user = '<username>'
db_passwd = '<password>'
db_name = '<database_table>'
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
```

# Remote connection to MariaDB
If you want to enable remote connections to the database, follow [this guide](https://mariadb.com/kb/en/mariadb/configuring-mariadb-for-remote-client-access/). This could make it easier to manage the database and apply the tables remotely.

# DONE!
The server is now fully installed and runs by executing .start in the terminal.

Now use git to clone the project.
```shell
git clone https://github.com/Synapz3/D0020E-2016-2017-Database
```
