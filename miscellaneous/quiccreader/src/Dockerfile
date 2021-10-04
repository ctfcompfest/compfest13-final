FROM nginx:alpine

RUN apk update && apk upgrade
RUN apk --no-cache add python3 \
    py3-greenlet py3-gevent py3-gunicorn

COPY docker .
RUN apk --no-cache add py3-pip python3-dev && \
    pip3 install -r server-req.txt && rm server-req.txt && \
    apk del py3-pip python3-dev
RUN chmod +x *.sh && \
    mv nginx.conf /etc/nginx/nginx.conf

WORKDIR /opt/ctf/app
COPY django/requirements.txt .
RUN apk --no-cache add py3-pip python3-dev && \
    pip3 install -r requirements.txt && \
    apk del py3-pip python3-dev

RUN apk --no-cache add libc6-compat 

COPY django .
RUN python3 manage.py collectstatic

RUN mkdir -p /sandbox && \
    chmod 777 /sandbox
COPY files /sandbox
RUN chmod 400 /tmp && \
    chmod 400 /sandbox/flag.txt && \
    chmod 755 /sandbox/admin_reader && \
    chmod u+s /sandbox/admin_reader

ENV PRODUCTION=true
ENV GUNICORN_WSGI_MODULE=quiccreader.wsgi:application
ENV GUNICORN_NAME=ctf GUNICORN_SOCKFILE=/run/gunicorn.sock
ENV GUNICORN_USER=nobody GUNICORN_GROUP=nobody
ENV SANDBOX_FOLDER=/sandbox

CMD ["/entrypoint.sh"]
