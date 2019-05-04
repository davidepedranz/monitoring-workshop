FROM node:12.0.0-alpine AS builder
COPY package.json .
COPY yarn.lock .
RUN yarn install
COPY . .
ARG REACT_APP_API_BASE_URL
RUN yarn build

FROM nginx:1.16.0-alpine
COPY --from=builder build /usr/share/nginx/html
