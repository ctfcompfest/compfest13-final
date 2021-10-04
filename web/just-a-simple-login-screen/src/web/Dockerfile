FROM nginx:alpine

RUN apk update && apk upgrade && \
    apk --no-cache add php7 php7-fpm php7-opcache php7-mysqli php7-json

COPY src/web/docker /
RUN chmod +x /*.sh && \
    mv /nginx.conf /etc/nginx/nginx.conf && \
    mv /php.ini /etc/php7/php.ini
RUN chmod 555 flag.txt

ENV MYSQL_DBPORT=0
COPY src/web/db /db
RUN /mysql-alpine.sh

WORKDIR /var/www/html
COPY src/web/server .
RUN chmod 555 -R .

CMD [ "/entrypoint.sh" ]
