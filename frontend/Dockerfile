FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --silent || npm i --silent
COPY . .
CMD ["npm", "run", "dev", "--", "--host"]
