#!/usr/bin/env sh
echo "Set default policy to 'DROP'"
iptables -P INPUT   DROP
iptables -P FORWARD DROP
iptables -P OUTPUT  DROP

echo "Allowing connections from/to localhost"
iptables -A INPUT -s 127.0.0.1 -j ACCEPT
iptables -A OUTPUT -d 127.0.0.1 -j ACCEPT

echo "Allowing incoming connections from app container"
iptables -A INPUT -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED -j ACCEPT

