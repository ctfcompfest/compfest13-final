FROM nginx:alpine

RUN apk update && apk upgrade
RUN apk --no-cache add python3 \
    py3-greenlet py3-gevent py3-gunicorn libcurl iptables py3-lxml

ENV PYCURL_SSL_LIBRARY=openssl
ENV PRODUCTION=true
ENV GUNICORN_WSGI_MODULE=main:app
ENV GUNICORN_NAME=ctf GUNICORN_SOCKFILE=/run/gunicorn.sock
ENV GUNICORN_USER=nobody GUNICORN_GROUP=nobody

WORKDIR /opt/ctf/app

# Installing server requirements
COPY docker/server-req.txt /server-req.txt
RUN apk --no-cache add py3-pip python3-dev && \
    pip3 install -r /server-req.txt && rm /server-req.txt && \
    apk del py3-pip python3-dev

# Installing app requirements
COPY web/requirements.txt .
RUN apk --no-cache add py3-pip python3-dev g++ gcc libxslt-dev build-base curl-dev && \
    pip3 install -r requirements.txt && \
    apk del py3-pip python3-dev g++ gcc libxslt-dev build-base curl-dev

# Ho Ho Ho...
RUN find / -name "*.dtd" -type f -delete
RUN find / -name "*.xml" -type f -delete

# create a flag
RUN echo -n 'COMPFEST13-this_is_not_the_flag' > /etc/flag

RUN chmod 600 /tmp

COPY docker /
RUN chmod +x /*.sh && \
    mv /nginx.conf /etc/nginx/nginx.conf

COPY web .
COPY web/static /var/www/html/static

CMD ["/entrypoint.sh"]