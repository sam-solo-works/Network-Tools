import socket
import struct
import ipaddress
import os

# get the IP of the NIC
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
nic_ip = s.getsockname()[0]

# get the subnet mask
nic_info = socket.gethostbyaddr(nic_ip)[2]
nic_mask = socket.inet_ntoa(struct.pack("!I", (1 << 32) - (1 << 32 >> nic_info[0])))

# get the network ID
nic_network = ipaddress.IPv4Network((nic_ip, nic_mask), strict=False)
network_id = nic_network.network_address

# ping all IPs within the network
for ip in nic_network:
    response = os.system("ping -c 1 " + str(ip))

    if response == 0:
        # get the MAC address associated with the IP
        mac_address = os.popen("arp -a " + str(ip)).read()
        print(str(ip) + " is reachable, MAC address: " + mac_address)
    else:
        print(str(ip) + " is not reachable")