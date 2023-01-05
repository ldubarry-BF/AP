import subprocess
import os, sys

if not os.geteuid()==0:
	sys.exit("[-] Please run as root")

print("[*] Starting Dnsmasq")
dnsmasq = subprocess.run("service dnsmasq restart", check=True, shell=True)
if dnsmasq.returncode == 0:
	print("[+] Dnsmasq service started")
else:
	print("[-] Dnsmasq service not started")


print("[*] Running Airmong-ng")
airmon = subprocess.run("airmon-ng check kill", check=True, shell=True)
if airmon.returncode == 0:
	print("[+] Airmon-ng done")
else:
	print("[-] Airmon-ng failed")

print("[*] Running hostapd in xterm")
hostapd = subprocess.Popen("xterm -e hostapd /etc/hostapd/hostapd.conf &>/dev/null &", shell=True)


print("[*] Setting ip address")
ip = subprocess.run("ip addr add 192.168.200.1/24 dev wlan0", shell=True, text=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if ip.returncode == 0:
	print("[+] IP address set up")
else:
	print("[-] IP already set")

print("[*] Starting eth0 for forwarding")
fwd = subprocess.run("ip link set eth0 up", shell=True)
if fwd.returncode == 0:
	print("[+] eth0 started")
else:
	print("[-] eth0 not started")


print("[*] Applying Iptables rules")
rules = open("rules.txt","r+")
for rule in rules:
	if rule!="\n":
		iptable=subprocess.run(rule, shell=True)
		if iptable.returncode ==0:
			print("[+] "+rule)
		else:
			print("[-] Rule not applied")


