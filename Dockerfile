FROM registry.gitlab.com/pages/hugo/hugo_extended:0.101.0 as builder
WORKDIR /site
COPY . /site
RUN hugo

FROM nginx:alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /site/public /usr/share/nginx/html