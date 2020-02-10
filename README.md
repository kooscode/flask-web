# flask-web

I used this basic Python Flask web service to enable
remote enable/disable of my modem and router.

- Python code to set Raspberry PI's GPIO pins
- Contained inside a Flask web site
- Startup flask using a systemctl .service

** Adjust script paths in .service file \
** Install the .service file in /etc/system.d/system/ \
** set permissions on .service file as 644 \
** follow directions in .service file to enable/start/etc. \
