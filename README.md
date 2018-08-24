# Data Driven Intrusion Detection

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

In order to symulate an intrusion, the first step to perform is collecting data from a network. In this experiment we set up a public IPv6/6LoWPAN network with RIOT on 15 A8-M3 nodes on Iot-Lab. If you don't have an account on the Iot-Lab website, please register.
1. Connect to a site host:
```
my_computer$ ssh <login>@<site>.iot-lab.info
```
2. In this experiment we choosed *grenoble* as site host. Start an experiment called **riot_a8** that contains `<num_of_nodes>` A8 nodes:
```
<login>@grenoble:~$ iotlab-auth -u <login> 
<login>@grenoble:~$ iotlab-experiment submit -n riot_a8 -d 60 -l <num_of_nodes>,archi=a8:at86rf231+site=grenoble
```
3. Wait a moment until the experiment is launched (state is Running) and get the nodes list. You will obtain a list that contains nodes called `a8-<id>.grenoble.iot-lab.info`. The first node of the list will act as border router node.
```
 <login>@grenoble:~$ iotlab-experiment get -i <exp_id> -s
 <login>@grenoble:~$ iotlab-experiment get -i <exp_id> -r
```
4. Get the code of the 2017.07 release of RIOT from GitHub:
```
<login>@grenoble:~$ mkdir -p ~/A8/riot
<login>@grenoble:~$ cd ~/A8/riot
<login>@grenoble:~/A8/riot$ git clone https://github.com/RIOT-OS/RIOT.git
<login>@grenoble:~/A8/riot$ cd RIOT
<login>@grenoble:~/A8/riot$ git checkout 2017.07-branch
```
5. Build the required firmware for the border router node. The border firmware is built using the RIOT *gnrc_border_router* example.
```
<login>@grenoble:~/A8/riot$ cd RIOT/examples/gnrc_border_router
<login>@grenoble:~/A8/riot/RIOT/examples/gnrc_border_router$ make ETHOS_BAUDRATE=500000 DEFAULT_CHANNEL=<channel> BOARD=iotlab-a8-m3 clean all
<login>@grenoble:~/A8/riot/RIOT/examples/gnrc_border_router$ cp bin/iotlab-a8-m3/gnrc_border_router.elf ~/A8/.
```
6. Build the required firmware for the other nodes. RIOT *gnrc_networking* example will be used for this purpose.
```
<login>@grenoble:~/A8/riot/RIOT/examples/gnrc_border_router$ cd ../gnrc_networking 
<login>@grenoble:~/A8/riot/RIOT/examples/gnrc_networking$ make DEFAULT_CHANNEL=<channel> BOARD=iotlab-a8-m3 clean all
<login>@grenoble:~/A8/riot/RIOT/examples/gnrc_networking$ cp bin/iotlab-a8-m3/gnrc_networking.elf ~/A8/
```
7. Connect to the A8 of the M3 border router: `node-a8-<id>`.
```
<login>@grenoble:~$ ssh root@node-a8-<id>
```
Then flash the BR firmware on the M3 and build the required RIOT configuration tools: uhcpd (*Micro Host Configuration Protocol*) and ethos (*Ethernet Over Serial*).
On the border router, the network can finally be configured automatically using the following commands:
```
root@node-a8-<id>:~/A8/riot/RIOT/dist/tools/ethos# ./start_network.sh /dev/ttyA8_M3 tap0 2001:660:3207:401::/64 500000
net.ipv6.conf.tap0.forwarding = 1
net.ipv6.conf.tap0.accept_ra = 0
----> ethos: sending hello.
----> ethos: activating serial pass through.
----> ethos: hello reply received
```
Note that we propagate another subnetwork for the border router (M3 node) in our LLN, 2001:660:3207:401::/64. You can also get this prefix directly on the A8 node :
```
root@node-a8-<id>:~# printenv
INET6_PREFIX_LEN=64
INET6_PREFIX=2001:0660:3207:401
INET6_ADDR=2001:0660:3207:0400::1/64
```
8. Now, in another terminal, log on the remaining A8 nodes and flash the gnrc_networking firmware on the M3:
```
my_computer$ ssh <login>@grenoble.iot-lab.info
<login>@grenoble:~$ ssh root@node-a8-<id>
root@node-a8-<id>:~# flash_a8_m3 A8/gnrc_networking.elf
```
9. Still in the border router, clone this responsory to automatically ping all the other nodes:
```
root@node-a8-<id>:~# cd
root@node-a8-<id>:~# git clone https://github.com/lucamaiano/data-driven-intrusion-detection
root@node-a8-<id>:~# cd data-driven-intrusion-detection/data
root@node-a8-<id>:~# python3 log.py
```
The `log.py` script will ask you to prompt the list of A8 nodes that you want to ping from the border router:
```
root@node-a8-<id>:~# Enter a node or a list of nodes to ping: <node-a8-<id1>,node-a8-<id2>,...,node-a8-<idN>
```
This command will generate a new file called `ping.log`. Now you can read the file with the results of the experiment.
```
root@node-a8-<id>:~# less ping.log
```










