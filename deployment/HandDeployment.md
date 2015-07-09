
1. Install PIP

sudo easy_install pip

2. Install virtualenv

sudo pip install virtualenv

3. Install node.js

a. sudo su (or somehow become root)
b. curl -sL https://rpm.nodesource.com/setup | bash -
c. yum install -y nodejs


4. Optional: install build tools
d. yum install gcc-c++ make


5. Install bower

sudo npm install -g bower

6. Install grunt CLI

sudo npm install -g grunt-cli


7. Install LESS

sudo npm install -g less


8. Install nginx

sudo yum update
sudo vi /etc/yum.repos.d/nginx.repo
paste this in:

[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/rhel/7/$basearch/
gpgcheck=0
enabled=1

sudo yum install nginx



9. Install uWSGI globally

sudo yum install python-devel
sudo pip install uwsgi



10. Install supervisord

sudo pip install supervisor
create a default config (just for testing):
sudo su
/usr/bin/echo_supervisord_conf > /etc/supervisord.conf
exit


11. Deploy source for web app.
to... /opt/app/
git clone https://swilliams@stash.twistbioscience.com/scm/tcfw/sample_movement_tracker.git
now...
/opt/app/sample_movement_tracker


12. npm install the node packages (such as grunt)
cd /opt/app/sample_movement_tracker
npm install


13. Create a virtual environment.
virtualenv --no-site-packages venv


14. Get into the virtual environment
source venv/bin/activate

15. Install pg_config:
sudo yum install postgresql-devel

16. Install (to this local virtual env) all the stuff in requirements.txt
pip install -r requirements.txt

17. Now run grunt to run bower and copy files and such...
grunt

18. Make sure the database is up to date.
python manage.py db upgrade

19. Make an "uploads" directory...

cd /opt/app/sample_movement_tracker/app/static
mkdir uploads

///////////////// NOW TRY TO RUN THE SERVER WITHOUT NGINX /////////////////////

20.
sudo venv/bin/python runserver.py

///////////////// NOW DO THE OTHER STUFF /////////////////////



21. Assuming you've installed the web app at /opt/app/sample_movement_tracker, make these config file changes.

cd /opt/app/sample_movement_tracker/operations_configs/supervisord/supervisord.d

22.a. Change nginx.conf to look like this:

[program:nginx]
command = /usr/sbin/nginx -c  /opt/app/sample_movement_tracker/operations_configs/nginx/nginx.conf
user = root
autostart = true
stdout_logfile=/var/log/nginx.log
redirect_stderr=true

22.b. Change uwsgi.conf to look like this:

[program:uwsgi]

;
; THIS CAUSES uWSGI TO LISTEN ON AN HTTP PORT RATHER THAN A LOCAL SOCKET. IT MIGHT BE SLOWER THAN THE WAY
; BELOW. BUT THE ADVANTAGE IS YOU CAN ACCESS THE WEBSITE AS YOU DO DEV BY GOING DIRECTLY TO http://localhost:9090 THUS
; BYPASSING "nginx".
command = /opt/app/sample_movement_tracker/venv/bin/uwsgi --http :9090 -w app:app -H /opt/app/sample_movement_tracker/venv --master --processes 4 --threads 2



;
; THIS MIGHT BE FASTER. SHOULD PROLLY CONSIDER THIS ONCE WE SCALE UP. WITH THIS CONFIG, THE ONLY WAY TO GET TO THE
; APP IS THRU "nginx" - WHICH MIGHT JUST BE FINE.
;
;command = /usr/local/bin/uwsgi --socket :3031 -w app:app -H /opt/app/sample_movement_tracker/venv --master --processes 4 --threads 2


directory = /opt/app/sample_movement_tracker/
user = root
stopsignal=QUIT
autostart=true
autorestart=true
stdout_logfile=/var/log/uwsgi.log
redirect_stderr=true


23. Start the web app
cd /opt/app/sample_movement_tracker/operations_scripts/supervisord

sudo ./start 

To stop: sudo ./stop










