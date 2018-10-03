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
2. Get the code of the 2017.07 release of RIOT from GitHub:
```
<login>@grenoble:~$ mkdir -p ~/riot
<login>@grenoble:~$ cd ~/riot
<login>@grenoble:~/riot$ git clone https://github.com/RIOT-OS/RIOT.git
<login>@grenoble:~/riot$ cd RIOT
<login>@grenoble:~/riot/RIOT$ git checkout 2017.07-branch
```
3. Compile the firmware:
```
<login>@grenoble:~/riot/RIOT$ make BOARD=iotlab-m3 -C examples/gnrc_networking clean all
```
4. Retrieve the generated binary firmware file on your computer (execute this scp command on your computer!)
```
my_computer:$ scp <login>@grenoble.iot-lab.info:riot/RIOT/examples/gnrc_networking/bin/iotlab-m3/gnrc_networking.elf gnrc_networking.elf
```
5. Log into the Web portal with your account credentials and submit a new experiment:
6. Set an experiment name (no spaces nor funny chars in the experiment name)
7. Duration: 60 minutes and starting “As soon as possible“
8. Select nodes from list or map
9. Choose nodes from Site = grenoble / M3 (at86rf231) / Not Mobile and click “Add to experiment”
10. Add your binary firmware gnrc_networking.elf with nodes selected and click "Submit experiment"
11. Wait experiment state Running in dashboard list. After click on experiment details and verify that you have Success in the deployment result
12. First, we have to initialize RPL on all nodes for interface 7 (can be obtained by looking at the output of ifconfig). We use on the SSH frontend the serial aggregator to talk to all nodes:
```
<login>@<site>:~$ serial_aggregator
1538581103.276934;Aggregator started
rpl init 7
1538581116.521179;m3-230; rpl init 7
1538581116.521659;m3-96;rpl init 7
1538581116.521826;m3-203;rpl init 7
1538581116.522080;m3-70;rpl init 7
1538581116.522350;m3-126;rpl init 7
1538581116.522716;m3-280;rpl init 7
1538581116.522910;m3-280;successfully initialized RPL on interface 7
1538581116.523047;m3-96;successfully initialized RPL on interface 7
1538581116.523273;m3-178;rpl init 7
1538581116.523512;m3-150;rpl init 7
1538581116.523620;m3-150;successfully initialized RPL on interface 7
1538581116.523783;m3-70;successfully initialized RPL on interface 7
1538581116.523920;m3-126;successfully initialized RPL on interface 7
1538581116.524211;m3-230;successfully initialized RPL on interface 7
1538581116.524360;m3-192;rpl init 7
1538581116.524548;m3-203;successfully initialized RPL on interface 7
1538581116.524678;m3-258;rpl init 7
1538581116.524866;m3-192;successfully initialized RPL on interface 7
1538581116.525326;m3-178;successfully initialized RPL on interface 7
1538581116.527159;m3-258;successfully initialized RPL on interface 7
```
13. With RPL two types of nodes are available: **simple router** nodes and **root nodes** (the root of the DAG).In our example we will choose m3-6 as the root of the DAG. Before doing so however, we need to configure a global IPv6 address form3-6 that can be used as the RPL DODAG-ID.
```
m3-96;ifconfig 7 add 2001:db8::1
1538581289.470753;m3-96;> ifconfig 7 add 2001:db8::1
1538581289.471001;m3-96;success: added 2001:db8::1/64 to interface 7
```
14. To show the dodag at node 7 and 8:

