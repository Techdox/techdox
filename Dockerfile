# ---- build ----
FROM alpine:3.20 AS build
RUN apk add --no-cache hugo git tzdata
WORKDIR /src
COPY . .
RUN hugo --gc --minify

# ---- serve ----
FROM nginx:1.27-alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/public /usr/share/nginx/html
