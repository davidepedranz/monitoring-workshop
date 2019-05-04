FROM alpine:3.9.3

RUN apk add --no-cache curl jq
COPY bot.sh /

ENTRYPOINT ["sh", "bot.sh"]
