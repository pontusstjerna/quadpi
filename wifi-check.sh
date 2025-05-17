#!/bin/bash

# Wait for WiFi to try
sleep 40

# Did we get IP from configured WiFi?
if ! /sbin/ifconfig wlan0 | grep -q "inet "; then
    echo "No WiFi found - starting access point!"
    systemctl start hostapd
    systemctl start dnsmasq
else
    echo "WiFi joined - not starting access point!"
    systemctl stop hostapd
    systemctl stop dnsmasq
fi
