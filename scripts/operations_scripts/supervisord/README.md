# Operations shell scripts for supervisord

### The scripts and what they do

```bash

  start - this starts up supervisord (on a Mac). On a linux box it would already have been started by the server.

  stop - this stops the supervisord daemon (on a Mac). You might not want to do this on a linux box.

  status - this runs "supervisorctl status" so you can see what apps supervisor is currently running. You should see "nginx" and "uwsgi" in the STARTING or RUNNING state.

```
