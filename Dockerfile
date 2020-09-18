FROM node:13-alpine

WORKDIR /app
COPY . .
RUN yarn

ENTRYPOINT NODE_ENV=live node --max-old-space-size=1024 index.js