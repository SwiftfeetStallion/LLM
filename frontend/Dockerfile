FROM node:24

ENV PORT=3000

EXPOSE 3000

WORKDIR /home/my-app

COPY my-app .
RUN npm install

ENTRYPOINT ["npm", "start"]