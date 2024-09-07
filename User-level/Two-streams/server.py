#!/usr/bin/env python3
import os
import sys
from datetime import datetime

from scapy.all import (
    IP,
    UDP,
    sniff,
    sendp,
)

def handle_pkt(pkt):
    if UDP in pkt and pkt[IP].dst == '10.0.0.9' and (pkt[UDP].dport == 6363 or pkt[UDP].dport == 6364):
        print("got a packet")
        print(pkt.time)
        pkt.show2()

        # Modify the destination IP addresses
        if pkt[UDP].dport == 6363:
            dst_ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8']
            for i, dst_ip in enumerate(dst_ips):
                pkt_i = pkt.copy()
                pkt_i[IP].dst = dst_ip
                if pkt_i[IP].dst != pkt_i[IP].src:
                    sendp(pkt_i, iface=f'server-eth{i}')                      

        if pkt[UDP].dport == 6364:
            dst_ips = ['10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8']
            for i, dst_ip in enumerate(dst_ips):
                pkt_i = pkt.copy()
                pkt_i[IP].dst = dst_ip
                if pkt_i[IP].dst != pkt_i[IP].src:
                    sendp(pkt_i, iface=f'server-eth{i + 4}')                                                    

        sys.stdout.flush()
        return     

def main():
    sniff(iface = ["server-eth0","server-eth1","server-eth2","server-eth3","server-eth4","server-eth5","server-eth6","server-eth7"],
          prn = lambda x: handle_pkt(x))


if __name__ == '__main__':
    main()
