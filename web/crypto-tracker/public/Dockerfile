FROM node:16-alpine

RUN apk update && apk upgrade

WORKDIR /opt/ctf/app
COPY app/package.json .
RUN npm install

COPY app .
RUN mkdir -p /path && \
    mv flag.txt /path/redacted
EXPOSE 3000

CMD ["node", "app.js"]