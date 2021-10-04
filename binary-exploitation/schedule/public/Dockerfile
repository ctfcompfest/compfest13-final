FROM ubuntu:18.04
RUN apt-get update && \
    apt-get -y install socat patchelf tzdata --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/nobody
COPY src .
RUN chmod +x chall && \
    chmod 555 * /tmp && \
    patchelf --set-interpreter ld-2.27.so chall

ENV LD_PRELOAD=/home/nobody/libc-2.27.so
ENV TZ=Asia/Jakarta
ARG DEBIAN_FRONTEND=noninteractive

RUN echo $TZ > /etc/timezone && rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

USER nobody
EXPOSE 9999
CMD socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"./chall"