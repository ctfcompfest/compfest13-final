#!/usr/bin/env sh
sleep 3

CACHE_IP=$(nslookup -type=a cache | tail -2 | tr -d '\n' | sed -r 's/[A-Za-z \:]*//')
echo "$CACHE_IP cache" >> /etc/hosts

echo "Set default policy to 'DROP'"
iptables -P INPUT   DROP
iptables -P FORWARD DROP
iptables -P OUTPUT  DROP

echo "Allowing outgoing connections to cache container"
iptables -A OUTPUT -d cache -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -s cache -m state --state ESTABLISHED -j ACCEPT

echo "Allowing ingoing connections to port 80"
iptables -A INPUT  -p tcp -m multiport --dports 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -m multiport --sports 80 -m state --state ESTABLISHED     -j ACCEPT
