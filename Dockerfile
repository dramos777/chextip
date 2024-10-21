FROM python:3.10-alpine3.19

# DB VARIABLES
ENV MYSQL_HOST="127.0.0.1"
ENV MYSQL_USER="admin"
ENV MYSQL_PASSWORD="admin"
ENV MYSQL_DATABASE="condominios_db"

#SSH RB
ENV SSH_USER="admin"
ENV SSH_PORT="22"
ENV SSH_PASSWORD="admin"

#Telnet variables
ENV TELNET_PORT="23"
ENV TELNET_PASSWORD="admin"

#Http variables
ENV HTTP_USER="admin"
ENV HTTP_PASSWORD="admin"

#APP
ENV DIRLOG="/var/log"
ENV PREFIXIP="192.168."

COPY ./app /app

WORKDIR /app

RUN apk update \
    && apk add --no-cache firefox bash inetutils-telnet sshpass mariadb-client \
    && pip install --no-cache-dir -r requirements.txt \
    && addgroup -S chextip && adduser -S chextip -G chextip \
    && mkdir -p /var/log/chextip \
    && touch "/var/log/chextip/web_chextip_access.log" \
    && touch "/var/log/chextip/web_chextip_audit.log" \
    && chown -R chextip:chextip /app \
    && chown -R chextip:chextip /var/log/chextip \
    && chmod +x /app/entrypoint.sh

USER chextip
    
EXPOSE 5000

CMD ["/app/entrypoint.sh"]

