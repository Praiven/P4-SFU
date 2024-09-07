#!/usr/bin/env python3

import random
import socket
import sys
import time  # Import the time module for sleep

from scapy.all import IP, UDP, Ether, get_if_hwaddr, get_if_list, sendp


def get_if():
    ifs = get_if_list()
    iface = None  # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface = i
            break
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface


def main():
    if len(sys.argv) < 3:
        print('pass 2 arguments: <destination> <letter>')
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    print("sending on interface %s to %s" % (iface, str(addr)))

    # Create the packet
    pkt_base  = Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt_base  = pkt_base  / IP(dst=addr) / UDP(dport=6363, sport=random.randint(49152, 65535)) 
    pkth_base = Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkth_base = pkth_base / IP(dst=addr) / UDP(dport=6364, sport=random.randint(49152, 65535))

    # Define the interval 
    interval = 0.014 

    try:
        counter = 0
        start_time = time.time()  # Record the start time        
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 60:  # Check if 60 seconds have passed
                print("\nPacket sending stopped after 1 minute.")
                break
                        
            counter = counter + 1
            data = sys.argv[2] + str(counter)
            pkt = pkt_base / data
            pkt.show2()
            sendp(pkt, iface=iface, verbose=False)
            counter = counter + 1
            data = sys.argv[2] + str(counter)
            pkth = pkth_base / data
            pkth.show2()
            sendp(pkth, iface=iface, verbose=False)
            time.sleep(interval)  # Sleep for the specified interval
    except KeyboardInterrupt:
        print("\nPacket sending stopped by user.")


if __name__ == '__main__':
    main()

