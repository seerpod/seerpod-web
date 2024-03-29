Running the Seerpod 
====================================
It depends on MySQL, you need to set up MySQL and the database schema for the demo to run.


1. Install prerequisites and build tornado

   See http://www.tornadoweb.org/ for installation instructions. If you can
   run the "helloworld" example application, your environment is set up
   correctly.

2. Install MySQL if needed

   Consult the documentation for your platform. Under Ubuntu Linux you
   can run "apt-get install mysql". Under OS X you can download the
   MySQL PKG file from http://dev.mysql.com/downloads/mysql/

3. Install Python prerequisites

   Install the packages MySQL-python, torndb, and markdown (e.g. using pip or
   easy_install). Note that these packages currently only work on
   Python 2. Tornado supports Python 3, but this seerpod demo does not.

3. Connect to MySQL and create a database and user for the seerpod.

   Connect to MySQL as a user that can create databases and users:
   mysql -u root

   Create a database named "seerpod":
   mysql> CREATE DATABASE seerpod;

   Allow the "seerpod" user to connect with the password "seerpod":
   mysql> GRANT ALL PRIVILEGES ON seerpod.* TO 'seerpod'@'localhost' IDENTIFIED BY 'seerpod';
  
   Set this export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/


4. Create the tables in your new database.

   You can use the provided schema.sql file by running this command:
   mysql --user=seerpod --password=Datadr1ven --database=seerpod < schema.sql

   You can run the above command again later if you want to delete the
   contents of the seerpod and start over after testing.

5. Run the seerpod example

   With the default user, password, and database you can just run:
   ./seerpod.py
 
   visit the site at localhost:8888

#### Dependency
<pre>
sudo apt-get update
sudo apt-get -y install git 
sudo apt-get -y install python-pip python-dev build-essential memcached python-memcache
sudo pip install tornado
sudo pip install torndb
sudo apt-get -y install python-mysqldb
sudo pip install simplejson
sudo apt-get -y install mysql-client
sudo pip install tornado-redis
</pre>

#### Start server
<pre>
sudo python main.py --port=80
</pre>

#### Start listener
<pre>
python listerner.py
</pre>

#### How does web sockets work
* Every time a user comes to the search page. A Hashset entry is setup with key = store_id and value = user_id.
* The user is also subscribed to the channel with name user_id.
* The listener is subscribed to the channel with the store_id's.
* The listener publishes to the userid channels whenever it reads any entry in the store channel.

http://stackoverflow.com/questions/4852702/do-html-websockets-maintain-an-open-connection-for-each-client-does-this-scale

