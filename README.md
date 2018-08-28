# Data Driven Intrusion Detection


## Table of Contents
1. [IPv6LoWPAN, COAP protocol and RPL](#ipv6lowpan-coap-protocol-and-rpl)
2. [Black Hole attack](#black-hole-attack)
3. [The Experiment](#the-experiment)

## IPv6LoWPAN, COAP protocol and RPL
As the name suggest, **IPv6LowPAN** (*IPv6* over *Lo*w-Power *W*ireless *P*ersonal *A*rea *N*etwork) is a networking technology or adaptation layer that allows IPv6 packets to be carried efficiently within small link layer frames defined by IEEE 802.15.4. The following image shows an example of IPv6LoWPAN network that is connected to the IPv6 network using an edge router. 

![IPv6LoWPAN network architecture](images/IPv6LoWPAN_network_architecture.png)

The router performs three actions: 
1. the data exchange between IPv6LowPAN devices and the internet;
2. local data exchange between devices inside the IPv6LowPAN;
3. the generation and maintainance of the radio subnet.

Usually IPv6LowPAN networks operate on the edge acting as stub nets, i.e. data going into the network is destined for one of the devices of the IPv6LowPAN net. There are two kind of devices inside a typical IPv6LowPAN network: routers and hosts. Routers route data destined to another nodes in the network and hosts are the end devices.

![IPv6LoWPAN stack](images/system_stack.png)

The image above shows the IPv6LoWPAN stack. As you can see, 6LoWPAN provides an adaptation layer between link and network layers to enable transmission of IPv6 datagrams over IEEE 802.15.4 radio links. We should focus our attention on two important components: the application layer and the network layer.

The application layer is responsible for data formatting and makes sure that data is transported in application-optimal schemes. A broadly used application layer on the internet is HTTP running over TCP, but HTTP has a large overhead, thus it is not optimal to use in many IPv6LoWPAN applications. However, it can still be very useful for communications between IPv6LoWPAN and the internet. To solve this problem, we use the contrained application protocol (**COAP**), a message protocol running over UDP with a bit-optimized REST mechanism that is very easy to map to HTTP via proxies. The protocol is described in RFC 7252 and defines retransmission, confirmable and non-confirmable messages, support for sleepy devices (typical on IoT netoworks!), block transfers, subscription support and resource discovery. 

![Routing](images/routing.png)

We can distinguish two kind of routing: mesh-under and route-over. The first uses the link layer addresses to forward data; while route-over uses the network layer, thus each hop in such networks represents one IP router. The usage of IP routing provides the foundation to larger and more powerful and scalable networks, since every router must implement all features supported by  normal IP router. The most used protocol for route-over IPv6LoWPAN networks is the *R*outing Low-*P*ower and *L*ossy network protocol (**RPL**). This protocol is defined in RFC 6550 and supports two different routing models; storing mode and non storing mode. In the first model, all devices configured as routers maintain a routing table and a neighbor table. The routing table is used to look up routes to devices and the neighbor table is used to keep track of a node's direct neighbor. In non-storing mode the only device with a routing table is the edge router, hence source routing is used, i.e. packet includes the complete route it needs to take to reach the destination. The first mode implies higher requirements on the devices acting as routers, while the second increase the overhead as the number of hops a packet needs to traverse to reach the destination grows up.


## Black Hole attack

Black hole attack is a denial-of-service attack in which a router that is supposed to relay packets instead discards them. This usually occurs from a router becoming compromised from a number of different causes. Black hole is one of the well-known security threats in wireless mobile ad hoc networks. The intruders utilize the loophole to carry out their malicious behaviors because the route discovery process is necessary and inevitable. Usually one malicious node utilizes the routing protocol to claim itself of being the shortest path to the destination node and drops the routing packets but does not forward packets to its neighbors.  

The image below shows an example of a *single black hole attack*. Node 1 stands for the source node and node 4 represents the destination node. Node 3 is a malicious node who replies the RREQ packet sent from source node, and makes a false response that it has the quickest route to the destination node. Node 1 erroneously judges the route discovery process with completion, and starts to send data packets to node 3. The malicious node probably drops or consumes the packets. 

![Black Hole attack](images/blackhole_attack.png)

In a bit more complex scenario, a couple of malicious nodes collaborate together in order to beguile the normal into their fabricated routing information, hiding from the existing detection scheme.


## The Experiment

In order to symulate an intrusion, the first step to perform is collecting data from a network. In this experiment we set up a public IPv6/6LoWPAN network with RIOT on 15 M3 nodes on Iot-Lab. If you don't have an account on the Iot-Lab website, please register.
1. Connect to a site host:
```
my_computer$ ssh <login>@<site>.iot-lab.info
```
2. In this experiment we choosed *grenoble* as site host. Start an experiment called **riot_m3** that contains `<num_of_nodes>` M3 nodes:
```
<login>@grenoble:~$ iotlab-auth -u <login> 
<login>@grenoble:~$ iotlab-experiment submit -n riot_m3 -d 60 -l grenoble,m3,2+4-5+9-11+15-25
```
3. Wait a moment until the experiment is launched (state is Running) and get the nodes list.
```
 <login>@grenoble:~$ iotlab-experiment get -li
```
4. Get the code of the 2017.07 release of RIOT from GitHub:
```
<login>@grenoble:~$ mkdir -p ~/riot
<login>@grenoble:~$ cd ~/riot
<login>@grenoble:~/riot$ git clone https://github.com/RIOT-OS/RIOT.git
<login>@grenoble:~/riot$ cd RIOT
<login>@grenoble:~/riot$ git checkout -b 2017.07-branch
```
Build the required firmware for the border router node. The node m3-2 will act as the border router in this experiment. The border firmware is built using the RIOT gnrc_border_router example.
```
<login>@grenoble:~/riot/RIOT/$ make ETHOS_BAUDRATE=500000 DEFAULT_CHANNEL=<channel> BOARD=iotlab-m3 -C examples/gnrc_border_router clean all
```
5. Now you can configure the network of the border router on m3-2 and propagate an IPv6 prefix with *ethos_uhcpd.py*.
```
<login>@grenoble:~$ sudo ethos_uhcpd.py m3-1 tap0 2001:660:5307:3100::1/64
```
The network is finally configured:
```
net.ipv6.conf.tap0.forwarding = 1
net.ipv6.conf.tap0.accept_ra = 0
----> ethos: sending hello.
----> ethos: activating serial pass through.
----> ethos: hello reply received
```
**Note 1**: leave the terminal open (you don’t want to kill ethos_uhcpd.py, it bridges the BR to the front-end network).
**Note 2**: If you have an error “Invalid prefix – Network overlapping with routes”, it’s because another experiment is using the same ipv6 prefix (e.g. 2001:660:5307:3100::1/64).
**Note 3**: If you have an error “Device or resource busy”, it’s because another user is using the same tap interface (e.g. tap0). Just use another one.
6. Build the required firmware for the other nodes. Open another terminal with SSH and type:
```
<login>@grenoble:~/riot/RIOT/$ make DEFAULT_CHANNEL=<channel> BOARD=iotlab-m3 -C examples/gnrc_networking clean all
<login>@grenoble:~/riot/RIOT/$ iotlab-node --update examples/gnrc_networking/bin/iotlab-m3/gnrc_networking.elf -l grenoble,m3,4-5+9-11+15-25
```
7. You can now interact with the other M3 nodes (`node-m3-<id>`) using nc.
```
my_computer$ ssh <login>@grenoble.iot-lab.info
<login>@grenoble:~$ nc m3-<id> 20000
```
Use RIOT shell ifconfig command to get the IP of the M3 node:
```
> ifconfig
Iface  7   HWaddr: 29:02  Channel: 26  Page: 0  NID: 0x23
        Long HWaddr: 36:32:48:33:46:df:a9:02 
        TX-Power: 0dBm  State: IDLE  max. Retrans.: 3  CSMA Retries: 4 
        AUTOACK  CSMA  MTU:1280  HL:64  6LO  RTR  RTR_ADV  IPHC  
        Source address length: 8
        Link type: wireless
        inet6 addr: ff02::1/128  scope: local [multicast]
        inet6 addr: fe80::1711:6b10:65fd:bd36/64  scope: local
        inet6 addr: ff02::1:fffd:bd36/128  scope: local [multicast]
        inet6 addr: 2001:660:3207:4c1:1711:6b10:65fd:bd36/64  scope: global
        inet6 addr: ff02::2/128  scope: local [multicast]
```
The global prefix has been successfully propagated, the IP on the M3 is 2001:660:3207:4c1:1711:6b10:65fd:bd36. Verify that it answers to “ping” from the frontend SSH (and from any computer with a global IPv6):
```
<login>@grenoble:~$ ping6 -c 3 2001:660:3207:4c1:1711:6b10:65fd:bd36
PING 2001:660:3207:4c1:1711:6b10:65fd:bd36(2001:660:3207:4c1:1711:6b10:65fd:bd36) 56 data bytes
64 bytes from 2001:660:3207:4c1:1711:6b10:65fd:bd36: icmp_seq=1 ttl=61 time=45.7 ms
64 bytes from 2001:660:3207:4c1:1711:6b10:65fd:bd36: icmp_seq=2 ttl=61 time=46.5 ms
64 bytes from 2001:660:3207:4c1:1711:6b10:65fd:bd36: icmp_seq=3 ttl=61 time=44.9 ms

--- 2001:660:3207:4c1:1711:6b10:65fd:bd36 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 44.919/45.759/46.595/0.684 ms
```
8. Still in the border router, clone this responsory to automatically ping all the other nodes:
```
root@node-m3-<id>:~# cd
root@node-m3-<id>:~# git clone https://github.com/lucamaiano/data-driven-intrusion-detection
root@node-m3-<id>:~# cd data-driven-intrusion-detection/data
root@node-m3-<id>:~# python3 log.py
```
The `log.py` script will ask you to prompt the list of A8 nodes that you want to ping from the border router:
```
root@node-m3-<id>:~# Enter a node or a list of nodes to ping: <node-m3-<id1>,node-m3-<id2>,...,node-m3-<idN>
```
This command will generate a new file called `ping.log`. Now you can read the file with the results of the experiment.
```
root@node-m3-<id>:~# less ping.log
```










