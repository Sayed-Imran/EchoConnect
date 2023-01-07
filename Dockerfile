FROM node:18.12.1 as app-build
WORKDIR /app

COPY . .
RUN npm ci --force --legacy-peer-deps && npm run build

FROM nginx:alpine
COPY --from=app-build /app/dist/echo-connect/ /usr/share/nginx/html
EXPOSE 80
