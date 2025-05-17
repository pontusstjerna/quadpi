#!/bin/bash

# Wait for WiFi to try
sleep 30

# Did we get IP from configured WiFi?
if ! nmcli -t -f WIFI g | grep -q 'enabled'; then
    echo "WiFi disabled!"
    exit 1
fi

if nmcli -t -f STATE g | grep -q 'connected'; then
    echo "WiFi connected - not starting access point!"
else
    echo "WiFi not found - starting access point (hotspot)"
    nmcli device wifi hotspod ssid QuadPi password ostronkoala
fi
