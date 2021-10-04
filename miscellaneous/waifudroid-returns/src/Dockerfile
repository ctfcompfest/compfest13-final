FROM node:16-alpine3.11

WORKDIR /usr/src/app
COPY ./package*.json ./
RUN npm install
COPY . .

CMD ["node", "app"]
