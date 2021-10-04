#!/usr/bin/env sh
# Run NGINX
nginx

# Test socket folder
echo "Starting $GUNICORN_NAME as `whoami`"
RUNDIR=$(dirname $GUNICORN_SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start gunicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
cd /opt/ctf/app && \
  gunicorn ${GUNICORN_WSGI_MODULE} \
    --name $GUNICORN_NAME \
    --user=$GUNICORN_USER --group=$GUNICORN_GROUP \
    --bind=unix:$GUNICORN_SOCKFILE \
    --log-level=debug \
    --log-file=- \
    -c /gunicorn.conf.py