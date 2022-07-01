FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y squid-openssl && \
    rm -rf /var/lib/apt/lists/*

RUN /usr/lib/squid/security_file_certgen -c -s /var/spool/squid/ssl_db -M 4MB

USER 13:13
EXPOSE 3128/tcp
CMD ["squid", "-N"]
