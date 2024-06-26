# Use Alpine Linux as base image
FROM alpine:3.9 as alpine-systemd

# # Install Nginx
RUN apk update && apk add nginx
RUN apk add --no-cache python3

COPY nginx-config/nginx.conf /etc/nginx
# Expose port 22
EXPOSE 22

ENTRYPOINT ["/sbin/init"]


FROM alpine-systemd as alpine-sshd

RUN apk update && \
    apk add bash git openssh rsync augeas shadow && \
    deluser $(getent passwd 33 | cut -d: -f1) && \
    delgroup $(getent group 33 | cut -d: -f1) 2>/dev/null || true && \
    mkdir -p ~root/.ssh /etc/authorized_keys && chmod 700 ~root/.ssh/ && \
    augtool 'set /files/etc/ssh/sshd_config/AuthorizedKeysFile ".ssh/authorized_keys /etc/authorized_keys/%u"' && \
    echo -e "Port 22\n" >> /etc/ssh/sshd_config && \
    cp -a /etc/ssh /etc/ssh.cache && \
    rm -rf /var/cache/apk/*


COPY docker-entrypoint.sh /entry.sh
RUN chmod a+x /entry.sh
ENTRYPOINT ["/entry.sh"]

CMD ["/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config"]

