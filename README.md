## Access point script

I have put together a VERY ugly python script that runs all the commands needed to setup a mobile access point, so you only have to run the script to fire the access point and start hacking.

## Architecture

![architecture](https://user-images.githubusercontent.com/63660458/214725174-af79b824-aa1c-4277-9576-14cb91c1f1d1.png)

## Requirements

### Packages

- dnsmasq: Will act as DHCP for the network.
- airmon-ng: Used to disable unwanted services.
- hostapd: Software Wifi access point.
- iptables: To control network flow and redirections.
- xterm: Used to keep hostapd running on display.

### Hardware

- This soft access point has been created to run on Kali/Debian machines.
- A USB Wifi adapter compatible with AP mode, such as the Alfa Network AWUS036NHA.

### Usage

```text
sudo python3 AP.py
```

### Quick setup guide

- Enable IP Forwarding
- Update dnsmasq configuration file (/etc/dnsmasq.conf)
- Update hostapd configuration file (/etc/hostapd/hostapd.conf)

## Troubleshooting

- Sometimes the eth0 interface looses its IP configuration. To solve this you can set the valid_lft parameter on the network card to *forever*. Here is an example command:

```text
ip addr change [ETH0_IP_ADDRESS] dev eth0 valid_lft forever preferred_lift forever
```

## Detailed guide

### Enable IP Forwarding

Your machine is going act as a router, so you need to activate IP Forwarding to allow traffic going through your machine.

```text
echo 1 > /proc/sys/net/ipv4/ip_forward
```

### Dnsmasq

Dnsmasq will provide DHCP service on the network. Install dnsmasq on your machine:
 
```text 
sudo apt-get install dnsmasq
```

And use the configuration file here: https://github.com/ldubarry-BF/AP/blob/main/dnsmasq.conf

You will need to update the domain name *[YOUR_DOMAIN_NAME]* to your local domain (can be anything really) and the DNS *[YOUR_DNS_SERVER_IP]* to your local DNS IP.

The network carasteristics are as follow:

- Network: 192.168.200.0/24
- DHCP range: 192.168.200.10-192.168.200.50
- Router: 192.168.200.1 (Basically your USB network card IP address)


```text
# global options
domain-needed
bogus-priv
no-resolv
filterwin2k
expand-hosts
domain=[YOUR_DOMAIN_NAME]
local=[YOUR_DOMAIN_NAME]
listen-address=127.0.0.1
listen-address=192.168.200.1

# DHCP range
log-dhcp
log-facility=/var/log/dnsmasq.log
dhcp-range=192.168.200.10,192.168.200.50,12h
dhcp-lease-max=25
dhcp-option=option:netmask,255.255.255.0
dhcp-option=option:router,192.168.200.1
dhcp-option=option:dns-server,[YOUR_DNS_SERVER_IP]
dhcp-option=option:domain-name,[YOUR_DOMAIN_NAME]
```

### Airmon-ng

Airmon-ng is only used to disable services that could interfere with the access point, such as Network Manager and dhclient.

It can be installed by installing aircrack-ng suite: 
```text 
apt-get install aircrack-ng
```

Run the following command to disable unwanted services:

```text
sudo airmon-ng check kill
```

### Hostapd

Hostapd is a software access point that will turn the USB Wifi adapter into an actually access point.

It can be installed with apt as follow: 
```text 
sudo apt-get install hostapd
```

Use the configuration file provided here: https://github.com/ldubarry-BF/AP/blob/main/hostapd_MAA.conf

You will have to update the SSID [SSID] and the PSK [PSK] for your Wifi network.

```text
interface=wlan0
hw_mode=g
channel=1
country_code=FR

ssid=[SSID]
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=TKIP
wpa_pairwise=CCMP
#rsn_pairwise=CCMP
wpa_passphrase=[PSK]
wpa_group_rekey=86400
```


### Assign IP address

The USB Wifi interface needs to have its IP address setup manually. This will be the gateway IP on the Wifi network.

```text
ip addr add 192.168.200.1/24 dev wlan0
```

### Iptables

Iptables rules need to be set to allow traffic from the USB Wifi interface to the machine's eth0 outgoing interface.

```text
#FLUSHING PREVIOUS RULES
/sbin/iptables --flush;
/sbin/iptables --table nat --flush;
/sbin/iptables --delete-chain;
/sbin/iptables --table nat --delete-chain;

#ALLOWING OUTGOING TRAFFIC
/sbin/iptables -A POSTROUTING -t nat -o eth0 -j MASQUERADE;

#ALLOWING TRAFFIC TO GO THROUGH THE INTERFACE
/sbin/iptables -A FORWARD --in-interface wlan0 -j ACCEPT;
