import socket
import ipaddress
import os
import requests
from bs4 import BeautifulSoup

# get the IP of the NIC
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
nic_ip = s.getsockname()[0]

# get the network ID and subnet mask
nic_network = ipaddress.IPv4Network(nic_ip)
network_id = nic_network.network_address
nic_mask = nic_network.netmask
# list to store the information for each device
device_list = []

# ping all IPs within the network
for ip in nic_network:
    response = os.system("ping -c 1 " + str(ip))

    if response == 0:
        # get the MAC address associated with the IP
        mac_address = os.popen("arp -a " + str(ip)).read()
        # check the MAC address on the website
        url = "https://maclookup.app/api/v1/macs/" + mac_address
        response = requests.get(url)
        data = response.json()

        # get the information for the device from the response
        vendor = data["vendor"]["name"]
        model = data["model"]["name"]
        name = data["model"]["name"]

        # add the information for the device to the list
        device_list.append()
        
# print the information for each device
for device in device_list:
    print("IP: " + device["IP"])
    print("MAC: " + device["MAC"])
    print("Vendor: " + device["Vendor"])
    print("Model: " + device["Model"])
    print("Name: " + device["Name"])
    print()