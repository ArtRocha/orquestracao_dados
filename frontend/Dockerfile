FROM node:18

WORKDIR /app

RUN npm init -y && echo '<h1>Frontend pronto 🚀</h1>' > index.html

CMD ["npx", "http-server", ".", "-p", "5173"]
