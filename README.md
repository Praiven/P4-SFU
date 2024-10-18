# P4-SFU

This repository contains the code that was executed in order to determine whether a P4 SFU can decrease the proccessing time needed for packet multicasting in comparison to a User-level SFU. P4 folder contains files for the P4 SFU experiment, while User-level for the server based SFU written in Python.

## Introduction
The purpose of this text is to provide an insight on the capabilities of an SFU in P4. Also known as *Selective Forwarding Unit* (SFU). It is deployed in almost every modern conferencing system and serves as a mean to duplicate and forward media streams between users. However, it is a frequent phenomenon for SFUs to not be specialized with the goal of reducing delay, and that load falls into the mechanisms that are responsible for the transportation of packets between kernel and user space. This occurrence can be bypassed with the use of P4.

## SFU methods
We will examine the performance of two different SFUs. One built in the P4 programming language, and another built to mimic an SFU that uses the application layer to perform packet duplication. P4 stands for Programming Protocol-independent Packet Processors. This programming language allows for greater flexibility in the functionality of switches. This is the feature that we will be taking advantage of, in order to build an SFU that can manage to duplicate packets without reaching the application level. With the aim of having a comparison measure for the SFU in P4, we also created an SFU that runs purely on python scripts.

## Implementation Details

### Environment configuration
For the implementation of an SFU in P4, a virtual machine was used with a freshly installed Ubuntu 20.04.6 LTS. In order to install all the required P4 development tools, the following script was executed: [install-p4dev-v5.sh](https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md). The experiment is being run on the folders of the [p4 tutorial exercises](https://github.com/p4lang/tutorials/tree/master/exercises) so the main makefile can be used to automate network generation process. As per exercise, and explained [in](https://github.com/p4lang/tutorials/tree/master/utils) the project folders includes, a secondary make file that configures the architecture of the P4 switch and the topology. The architecture being used is that of BMv2. Both of the SFUs used Mininet to emulate and handle the virtual network. The traffic that flows through our virtual network was captured and analyzed through Wireshark.

### P4 SFU
The P4 SFU uses the BMv2 framework with the simple switch grpc process. The P4 file is written in the P4 16 version of the P4 language and uses core.p4 and the v1model. The packets that circulate in our virtual network are UDP packets. Consequently, the headers of the P4 file include 3 structures, an ethernet, an ipv4 and a udp structure. The SFU parser identifies and extracts these three headers and passes that packet to ingress processing. Inside the ingress processing block, four actions are specified. action drop marks a packet for drop, action ipv4 forward forwards the packet according to control plane rules. Finally, actions multicastLQ and multicastHQ are used to mark a packet according to the group it needs to be multicast towards. This is used by changing the standard metadata.mcast grp field provided by the v1model. The multicast group entries are provided in the s1-runtime file. The condition that decides where the packet will be multicasted is that of the UDP destination port. After the ingress processing block, naturally, comes the the egress processing block. There, the packets’ egress port is compared with the ingress port for the purpose of avoiding the packet to be sent to the sender himself. Following the V1Switch architecture, the packet has its headers reassembled and becomes serialized in order to be sent towards the appropriate recipients.

### User-level SFU
The User-level SFU aims to produce the same result as the P4 SFU but through a different approach. With this aim in mind, a python program was created. The program acts as the SFU and it is deployed on the central host of the star topology. Since, packet handling is needed, we opted for the use of python’s scapy library. The python program constantly sniffs at every available interface. When a packet is caught, a function that handles its processing is being called asynchronously. The function takes the packet and checks where is it headed. If it is headed for the SFU server, it means the packet has just arrived and needs to be duplicated and forwarded accordingly. So, the IP destination is checked, along with the UDP destination port in order to decide on the correct multicast group. Subsequently, the packet is duplicated as many times it needs to be duplicated and forwarded to the correct receiver.

## The experiment

The experiment has been structured to mimic a conferencing application. Firstly, a network topology was established. N Hosts communicated with each other through a star configuration topology, in the middle of which, a P4 switch was managing the traffic. In the case of the server based SFU, we deployed an extra host, which acted as the SFU. This host was connected with every other host on a separate interface. A python script would run on this host, that enabled the SFU host to receive packets from its interfaces and forward them to the proper multicast group, similarly to how the P4 switch functioned. With the intention of imitating a conferencing application environment, that runs with an SFU, it was decided that N of those hosts would receive packets that were of low quality streams, and N/2 of them would receive high quality streams. Each hosts runs a certain python script that allows it to receive its matching quality stream. Furthermore, each host can send a packet to the switch. The switch receives the packet and checks from which UDP port the packet was sent from. Judging based on it, the switch forwards the packet towards the correct multicast group. This part is crucial in conferencing applications and the whole point of this research is to minimize the time it needs to be completed. In addition to this, another set of experiments was conducted, with the purpose of simplifying the interpretation of the results. Particularly, in the second set of experiments, each participant host receives a low quality stream from all its peers. The volume of traffic passing through the SFU varies according to the number of senders and the simulation was running for approximately one minute for both scenarios.

## Results

Using our SFU implementations we ran a number of experiments to determine the latency in packet processing from the P4 and User-level SFUs. The difference between the time the packet entered the SFU and the time the packet left the SFU was measured in order to determine the processing cost in each case. In the following tables we can see the results of our experiments. Assuming, that no queues are being formed during the execution of the experiments, the difference between the P4 and the server based SFU is evident. As the number of hosts increases, so does the difference between the delay of each method. Below are the tables which contain the results of the experiments that were conducted.

### P4 based SFU statistics with one stream.

| Hosts | Min       | Max       | Avg       | Increase | Packets | Traffic Volume |
|-------|-----------|-----------|-----------|----------|---------|----------------|
| 2     | 0.000505  | 0.002907  | 0.000778  | 0        | 1456    | 1071 Kbits     |
| 3     | 0.000471  | 0.004113  | 0.000937  | 20%      | 1484    | 3276 Kbits     |
| 4     | 0.000467  | 0.007507  | 0.001134  | 21%      | 1525    | 6734 Kbits     |
| 5     | 0.000458  | 0.017137  | 0.001675  | 48%      | 1558    | 11466 Kbits    |
| 6     | 0.000453  | 0.015145  | 0.001978  | 18%      | 1590    | 17553 Kbits    |
| 7     | 0.000456  | 0.030355  | 0.003095  | 56%      | 1610    | 24884 Kbits    |
| 8     | 0.000462  | 0.052992  | 0.004736  | 53%      | 1608    | 33137 Kbits    |
| 9     | 0.000460  | 0.106720  | 0.009122  | 93%      | 1601    | 42420 Kbits    |
| 10    | 0.000484  | 0.328883  | 0.031889  | 250%     | 1591    | 52693 Kbits    |
| 11    | 0.000514  | 0.989098  | 0.267746  | 740%     | 1585    | 64160 Kbits    |
| 12    | 0.000523  | 5.958905  | 3.986195  | 1389%    | 1569    | 68594 Kbits    |

### P4 based SFU statistics with two streams.

| Hosts | Min       | Max       | Avg       | Increase | Packets | Traffic Volume |
|-------|-----------|-----------|-----------|----------|---------|----------------|
| 2     | 0.000515  | 0.002859  | 0.000834  | 0        | 1457    | 804 Kbits      |
| 4     | 0.000484  | 0.014854  | 0.001210  | 45%      | 1548    | 5126 Kbits     |
| 6     | 0.000476  | 0.018257  | 0.001987  | 64%      | 1613    | 13358 Kbits    |
| 8     | 0.000457  | 0.051833  | 0.003915  | 97%      | 1633    | 25244 Kbits    |
| 10    | 0.000486  | 0.141570  | 0.015084  | 285%     | 1647    | 40919 Kbits    |

### Server based SFU statistics with one stream.

| Hosts | Min       | Max       | Avg       | Increase | Packets |
|-------|-----------|-----------|-----------|----------|---------|
| 2     | 0.010961  | 10.913122 | 7.860589  | 0        | 1557    | 
| 3     | 0.015288  | 32.523685 | 23.351614 | 197%     | 1564    |

### P4 based SFU statistics with two streams.

| Hosts | Min       | Max       | Avg       | Increase | Packets | 
|-------|-----------|-----------|-----------|----------|---------|
| 2     | 0.013842  | 6.811303  | 4.585829  | 0        | 1566    | 
| 4     | 0.019133  | 53.473191 | 34.797006 | 659%     | 1614    | 
