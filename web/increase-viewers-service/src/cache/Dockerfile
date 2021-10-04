FROM redis:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache python3 iptables

WORKDIR /opt/ctf/app

COPY docker/requirements.txt .
RUN apk --no-cache add py3-pip python3-dev build-base linux-headers && \
    pip3 install -r requirements.txt && \
    apk del py3-pip python3-dev build-base linux-headers

# Ho Ho Ho...
RUN find / -name "*.dtd" -type f -delete
RUN find / -name "*.xml" -type f -delete

# Another security
RUN chmod 777 /var/spool/cron/crontabs && \
    echo "*/10 * * * * python3 /opt/ctf/app/security.py" >> /var/spool/cron/crontabs/root
RUN chmod 700 /tmp

COPY docker .
RUN chmod +x *.sh

ENTRYPOINT [ "./entrypoint.sh" ]