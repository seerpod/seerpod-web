seerpod
=======

Machine learning based octo

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
sudo apt-get -y install got python-setuptools git python-dev build-essential mysql-server python-mysqldb
sudo easy_install tornado
sudo easy_install torndb
git clone https://github.com/dan-boa/seerpod.git
#Create database riyusaki
#Create database riyusaki_warm
</pre>

<pre>
cd /home/ubuntu/seerpod
sudo python main.py --port=80
</pre>
