seerpod-web
===========

Web interface for users

## Dependecies

#### Pythonic libraries


## Setup Supervisord and Nginx

#### References
1. [Blog post](http://chase.io/post/17197274701/)
2. [Github Repo](https://github.com/chaselee/tornado-linode)

#### Install supervisord
<pre>
sudo apt-get install nginx
sudo pip install supervisor
</pre>

#### Create nginx user
<pre>
adduser --system --no-create-home --disabled-login --disabled-password --group nginx
</pre>

#### Start Supervisord
<pre>
supervisord -n -c supervisord/suoervisord.conf
</pre>

#### Start Nginx
<pre>
/etc/init.d/nginx start -c nginx/nginx.conf
</pre>

#### Dependency
<pre>
sudo apt-get update
sudo apt-get -y install git 
git clone https://github.com/dan-boa/riyu-fetch.git
sudo apt-get -y install python-pip python-dev build-essential memcached python-memcache
sudo pip install tornado
sudo pip install torndb
sudo apt-get -y install python-mysqldb
sudo pip install simplejson
sudo apt-get -y install mysql-server
sudo pip install tornado-redis
#Create database sp
</pre>

<pre>
cd /home/ubuntu/seerpod-web
sudo python main.py --port=80
</pre>

Update
-----
curl -X GET 127.0.0.1/update/1/1
