FROM node:16-alpine

RUN apk update && apk upgrade

WORKDIR /opt/ctf/app
COPY server/package.json .
RUN npm install

COPY server .
RUN mkdir -p /into-the-wood && \
    mv flag.txt /into-the-wood/youFoundMe
EXPOSE 3000

CMD ["node", "app.js"]