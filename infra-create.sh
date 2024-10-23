#!/usr/bin/env bash

# Nginx variables
CERTDIR="./etc/nginx/certs/"
NGINXDIR="./etc/nginx/"
NGINXCONF_F="./etc/nginx/nginx.conf"
KEYNAME="privkey.pem"
CERTNAME="fullchain.pem"
DHNAME="dhparam.pem"
VALID="1095"

# Functions
# Create certs function
Cert_and_dhparam_create() {
    # Generate private key and testened certificate
    if openssl req -newkey rsa:2048 -nodes -keyout "certs/${KEYNAME}" -x509 -days "${VALID}" -out "certs/${CERTNAME}"; then
        echo "Chave privada e certificado autoassinado gerados com sucesso."
    else
        echo "Erro ao gerar chave privada e certificado autoassinado."
        return 1
    fi

    # Generate parameters Diffie-Hellman
    if openssl dhparam -out "certs/${DHNAME}" 2048; then
        echo "Parâmetro Diffie-Hellman gerado com sucesso."
    else
        echo "Erro ao gerar parâmetro Diffie-Hellman!"
        return 1
    fi

    echo "Certificado e parâmetro Diffie-Hellman gerados com sucesso."
    return 0
}

# Generate nginx.conf file
Nginx_conf () {
	cat << EOF > "$NGINXCONF_F"
user                 nginx;
pid                  /var/run/nginx.pid;
worker_processes     auto;
worker_rlimit_nofile 65535;

events {
    multi_accept       on;
    worker_connections 65535;
}
 
http {
    charset                utf-8;
    sendfile               on;
    tcp_nopush             on;
    tcp_nodelay            on;
    server_tokens          off;
    log_not_found          off;
    types_hash_max_size    2048;
    types_hash_bucket_size 64;
    client_max_body_size   16M;

    # Logging
    access_log             /var/log/nginx/access.log;
    error_log              /var/log/nginx/error.log warn;

    # SSL
    ssl_session_timeout    1d;
    ssl_session_cache      shared:SSL:10m;
    ssl_session_tickets    off;

    # Diffie-Hellman parameter for DHE ciphersuites
    ssl_dhparam            /etc/nginx/dhparam.pem;

    # Mozilla Intermediate configuration
    ssl_protocols          TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers            EECDH+AESGCM:EDH+AESGCM;
    ssl_ecdh_curve secp384r1;

    # OCSP Stapling
    ssl_stapling           on;
    ssl_stapling_verify    on;

    resolver 1.1.1.1 valid=300s;
    resolver_timeout 5s;

# Disable strict transport security for now. You can uncomment the following
# line if you understand the implications.
#add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";

    # Load balancing configuration
    upstream chextip {
        server chextip:5000;
    }

    # NGINX server block for HTTP
    server {
        listen *:80;
        location / {
            proxy_pass http://chextip;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        # Redirect all HTTP traffic to HTTPS
        return 301 https://\$host\$request_uri;
    }

    # NGINX server block for HTTPS
    server {
        listen 443 ssl;

        ssl_certificate     /etc/nginx/certs/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/privkey.pem;

        location / {
            proxy_pass http://chextip;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}

EOF

}

# Main script logic
main() {
    # Ensure directories exist or create them
    if [ ! -d "certs" ]; then
        mkdir -p "certs" || { echo "Erro ao criar diretório: ./certs"; exit 1; }
    fi

    if [ ! -d "$CERTDIR" ]; then
        mkdir -p "$CERTDIR" || { echo "Erro ao criar diretório: $CERTDIR"; exit 1; }
    fi

    if [ ! -d "$NGINXDIR" ]; then
        mkdir -p "$NGINXDIR" || { echo "Erro ao criar diretório: $NGINXDIR"; exit 1; }
    fi

    # Generate certificates and nginx.conf
    Cert_and_dhparam_create || { echo "Erro ao gerar certificados e parâmetros"; exit 1; }
    Nginx_conf || { echo "Erro ao gerar nginx.conf"; exit 1; }

    # Set permissions
    chmod -w $PWD/certs/* || { echo "Erro ao definir permissões em ./certs/"; exit 1; }
    cp -R $PWD/certs/$DHNAME $NGINXDIR \
    &&  cp -R $PWD/certs/* $CERTDIR \
    && rm -rfi $PWD/certs/

    echo "Script concluído com sucesso!"
}

# Run main function
main

