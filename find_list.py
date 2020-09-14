from scapy.all import *
import nmap
import netifaces
from netaddr import IPAddress
import subprocess
import os
import re


def ipv4_to_int(ipv4_str):
    num = ipv4_str.split(".")
    ipv4_int = 0
    for i in range(4):
        ipv4_int = ipv4_int + int(num[3 - i]) * (2 ** (i * 8))
    return ipv4_int


def ipv4_to_str(ipv4_int):
    num = []
    for i in range(4):
        tmp = ipv4_int // (2 ** ((3 - i) * 8))
        num.append(str(tmp))
        ipv4_int = ipv4_int - tmp * (2 ** ((3 - i) * 8))
    return ".".join(num)


def find_network_id(ip, netmask):
    ipv4_int = ipv4_to_int(ip)
    mask = 2 ** 32 - 2 ** (32 - netmask)
    network_id_int = ipv4_int & mask
    return ipv4_to_str(network_id_int)


def refresh():
    tmp = read_routes()
    gateway = ""
    my_ip = ""
    ethernet_name = ""

    for i in tmp:
        if not (i[0] or i[1]):
            gateway = i[2]
            ethernet_name = i[3]
            my_ip = i[4]
    ## find gateway

    addr = netifaces.ifaddresses(ethernet_name)
    netmask = addr[netifaces.AF_INET][0]['netmask']
    netmask_num = IPAddress(netmask).netmask_bits()
    ## find subnet mask

    gateway_int = ipv4_to_int(gateway)
    nm = nmap.nmap.PortScanner()
    network_id = find_network_id(gateway, netmask_num)
    host = network_id + '/' + str(netmask_num)
    nm.scan(hosts=host, arguments='-sn')
    ## ping sweep

    arp_list = []

    f = open("arptmp.txt","w")
    data = subprocess.check_output(["arp", "-a"]).decode('utf-8')
    f.write(data)
    f.close()

    f = open("arptmp.txt","r")
    arp_tmp = ""
    ip_re = re.compile("\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}")
    mac_re = re.compile(
        "\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}")
    cnt = 0
    while True:
        arp_tmp = f.readline()
        if not arp_tmp:
            break
        find_ip = ip_re.search(arp_tmp)
        find_mac = mac_re.search(arp_tmp)
        if find_ip and find_mac and not find_mac.group() == "ff:ff:ff:ff:ff:ff":
            mac_tmp = str(find_mac.group()).split(":")
            for i in range(len(mac_tmp)):
                if len(mac_tmp[i]) == 1:
                    mac_tmp[i] = "0" + mac_tmp[i]
            mac_tmp = ":".join(mac_tmp).upper()
            tmp_list = [find_ip.group(), mac_tmp]
            arp_list.append(tmp_list)

    f.close()
    os.remove("./arptmp.txt")

    return arp_list
## find arp list
