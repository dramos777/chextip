FROM python:3.10.15-slim-bookworm

# DB VARIABLES
ENV MYSQL_HOST="127.0.0.1" \
    MYSQL_USER="admin" \
    MYSQL_PASSWORD="admin" \
    MYSQL_DATABASE="condominios_db" \
    SSH_USER="admin" \
    SSH_PORT="22" \
    SSH_PASSWORD="admin" \
    TELNET_PORT="23" \
    TELNET_PASSWORD="admin" \
    HTTP_USER="admin" \
    HTTP_PASSWORD="admin" \
    HTTP_XPE3200_PASS="admin" \
    HTTP_SS3530_PASS="admin" \
    HTTP_SS3532_PASS="admin" \
    DIRLOG="/var/log" \
    PREFIXIP="192.168."

COPY ./app /app

WORKDIR /app

RUN apt update \
    && apt install -y --no-install-recommends build-essential python3-dev \
       wget bzip2 telnet sshpass mariadb-client openssh-client iputils-ping firefox-esr \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.35.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm -rf geckodriver-v0.35.0-linux64.tar.gz \
    && apt remove --purge build-essential python3-dev wget bzip2 pip -y \
    && apt autoremove -y \
    && apt clean \
    && addgroup --system chextip || true \
    && adduser --system --no-create-home --gecos "" chextip || true \
    && mkdir -p /var/log/chextip \
    && touch "/var/log/chextip/web_chextip_access.log" \
    && touch "/var/log/chextip/web_chextip_audit.log" \
    && chown -R chextip:chextip /app \
    && chown -R chextip:chextip /var/log/chextip \
    && chown -R chextip:chextip /usr/local/bin/* \
    && chmod +x /app/entrypoint.sh

#USER chextip

EXPOSE 5000

CMD ["/app/entrypoint.sh"]

