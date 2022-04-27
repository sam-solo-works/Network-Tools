from ipaddress import ip_address
import os, sys, subprocess, pyuac # This is a module that is used to run the command line as an administrator.
from operator import index
from netifaces import interfaces, ifaddresses, AF_INET
from scapy.all import *

def checkAdmin():
    if not pyuac.isUserAdmin():
        return pyuac.runAsAdmin()
    else:
        main()

def main():
    networkRange, IPAddress = ask_network_pref(get_self_IP())
    IP_list = created_IP_list(networkRange, IPAddress)
    created_IP_list(networkRange, IPAddress)
    print(f"Searching for network devices in the same range as {IPAddress}. Please wait...")
    #print(f"Here is a list of all active IPs on your network.")
    print(ping_network_objects(IP_list))

#Class Network_Interface():
def get_self_IP():
        addresses = []
        for ifaceName in interfaces():
            ifaddresses_list = ifaddresses(ifaceName) # The 2 index of ifaddresses(ifaceName) is where the actual IP address is stored.
            possibilities = [i['addr'] for i in ifaddresses_list.setdefault(AF_INET, [{'addr': 'No IP addr'}])]
            for i in possibilities:
                if ifaddresses_list[2][0]['addr'] != "No IP addr": # The 0 index of ifaddresses(ifaceName) is where "No IP addr" is stored. This if statement excludes those entries from the list.
                    addresses.append(i)
        return addresses

def ask_network_pref(addresses):
        num = 0
        for i in addresses:
            num = int(num)
            if num <= len(addresses):
                num = num + 1
                num = str(num)
                print(f'{num}.)' , i)
        userChoice = input("Please enter the number of the IP address you would like to use: ")
        if userChoice.isdigit():
            userChoice = int(userChoice)
            if userChoice <= len(addresses):
                IPAddress = addresses[userChoice - 1]
                networkRange = IPAddress[:IPAddress.rfind('.') + 1] + '0' #Changes the users IP to the network ID.
                return networkRange, IPAddress
            else:
                print("Invalid choice. Please try again.")
                ask_network_pref(addresses)

def created_IP_list(networkRange, IPAddress):
        IP_list = []
        for i in range(1,256):
            networkRange = networkRange[:networkRange.rfind('.') + 1] + ''
            IP_list.append(networkRange + str(i))
        #IP_list.pop(IP_list.index(IPAddress))
        return IP_list

# created_IP_list = ["192.168.1.13","192.168.1.14"] #test data
# IP_list = ["192.168.1.13","192.168.1.14"] #test data

TIMEOUT = 2

def ping_network_objects(IP_list):
    new_IP_list = []
    with open(os.devnull, "wb") as limbo:
        for i in IP_list:
            firstoctet,secondoctet,thirdoctet,fourthoctet = i.split('.')
            fourthoctet = int(fourthoctet)
            #ping_reply = srp1(IP(dst=i)/ICMP(), timeout=TIMEOUT, verbose=0)
            res = subprocess.Popen(['ping', '-n', '1', '-w', '300', i],
                stdout=limbo, stderr=limbo).wait()
            while fourthoctet != 255:
                if res == 0:
                    print(i + ' ok!')
                    new_IP_list.append(i)
                else:
                    print(i + ' does not respond.')
                break
            #wait until the ping is done. May need to change in the future.
        return new_IP_list

def find_hardware_info(new_IP_list):
        finale = True
        print(f"Here is a list of all active IPs on your network: " + "\n")
        print(new_IP_list)
        end_script = input("Would you like to end the script? (y/n): ")
        while finale:
            if end_script == 'n':
                finale = True
            elif end_script == 'y':
                finale = False
                break
            else:
                print("Invalid choice. Please try again.")
                finale = True
                break

if __name__ == '__main__':
    checkAdmin()
