# Mininet: Emulating long-distance networks with Netem

## Overview

In this lab, we'll learn how to limit the bandwidth and add delay to a virtual network consists of two hosts and two routers, and run a very simple ping test to see the effect of the limited bandwidth and added delay. The primary objective is to see the emulated behavior of a realistic long-distance network configuration “in action”. 

* [Part 1: Delay with Netem](#part-1-delay-with-netem)
* [Part 2: Other network parameters](#part-2-other-network-parameters)

## Learning outcomes

After completing this lab, you will:

* learn how to configure network parameters (delay, jitter, packet loss, reordering, corruption) that affect the performane of network and limit bandwidth. 

* emulate the behavior of a long distance network with a simple topology.


## Network topology

Here is a simple network topology (based on [/mininet/delay-bw-conf](https://github.com/safiqul/2410/tree/main/mininet/delay-bw-conf)) which consists of two hosts (h1 and h2) connected via routers (r1 and r2) - 'h1 -> r1 -> r2 -> h2'.


```python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink


class LinuxRouter( Node ):
    """A Node with IP forwarding enabled.
    Means that every packet that is in this node, comunicate freely with its interfaces."""

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):

    def build( self, **_opts ):		
        h1=self.addHost("h1",ip='10.0.0.1/24', defaultRoute='via 10.0.0.2')
        r1=self.addNode("r1",cls=LinuxRouter,ip=None)  
        r2=self.addNode("r2",cls=LinuxRouter,ip=None)
        h2=self.addHost("h2",ip='10.0.2.1/24')
        self.addLink(h1, r1,intfName1= 'h1-r1', intfName2= 'r1-h1', \
                params2={ 'ip' : '10.0.0.2/24' })
        self.addLink(r1, r2, params1={ 'ip' : '10.0.1.1/24' }, \
                intfName1= 'r1-r2', params2={ 'ip' : '10.0.1.2/24' }, intfName2= 'r2-r1')
        self.addLink(r2,h2,intfName1= 'r2-h2', intfName2= 'h2-r2', \
                params1={ 'ip' : '10.0.2.2/24' })
topo = NetworkTopo()
net = Mininet( topo=topo, link=TCLink )
net.start()

#ip route add ipA via ipB dev INTERFACE
#every packet going to ipA must first go to ipB using INTERFACE
net["r1"].cmd("ip route add 10.0.2.0/24 via 10.0.1.2 dev r1-r2")
net["r2"].cmd("ip route add 10.0.0.0/24 via 10.0.1.1 dev r2-r1")
net["h2"].cmd("ip route add 10.0.0.0/24 via 10.0.2.2 dev h2-r2")
net["h2"].cmd("ip route add 10.0.1.0/24 via 10.0.2.2 dev h2-r2")

net["h1"].cmd("ethtool -K h1-eth0 tso off")
net["h1"].cmd("ethtool -K h1-eth0 gso off")
net["h1"].cmd("ethtool -K h1-eth0 lro off")
net["h1"].cmd("ethtool -K h1-eth0 gro off")
net["h1"].cmd("ethtool -K h1-eth0 ufo off")

result = net['h1'].cmd('ifconfig')
print (result)

net.pingAll()
CLI( net )
net.stop()

```



## Part 1: Delay with Netem

`Netem` is a widely used linux emulator to test the performance of network applications in a virtual network. This allows you to emulate the behavior of long-distance networks by configuring network parameters (delay, loss, jitter, reordering etc.).

Netem consists of queuing discipline (default: first in first out (FIFO)), sitting between the Internet protocol and the network device. It exposes a command line tool for the network administrators, between the user-space (application) and kernel space (transport protocol and protocols below the transport layer), to configure the network parameters. The policies (e.g, what to delay/drop) are applied at the packets that enter the queuing discipline before it is released from the other side to the network device. 

Let's see `Netem` in action:

The user invokes `Netem` using [Traffic control `tc`](https://netbeez.net/blog/how-to-use-the-linux-traffic-control/), a powerful Linux tool to configure the kernel packet scheduler.

`sudo tc qdisc ad dev <interface> root netem options`

* `qdisc`: also known as queuing discipline, is a scheduler. Default is first in first out (FIFO). The rules are applied to the packets entering in the qdisc before it is released from the qdisck and sent to the network device.

* `add`: add a rule (e.g., delay). Other options are `del`, `replace`, `change`,  and `show`. `add` should be replaced with `change` if you want to change

* `interface`: packets outgoing from the interface will experience the effect of added policies. 

* `root`: modify the outbound traffic scheduler (egress qdisc)

* `options`: specifies the total amount of delay, loss, reordering etc. should be applied


Before, we set out to add a rule on the outgoing interface of r1 that connects us to the rest of the network. Let's ping first without any rules:


```
    root@safiqul-virtual-machine:data2410-lab/lab-setup/delay-bandwidth# ping 10.0.2.1
    PING 10.0.2.1 (10.0.2.1) 56(84) bytes of data.
    64 bytes from 10.0.2.1: icmp_seq=1 ttl=62 time=0.051 ms
    64 bytes from 10.0.2.1: icmp_seq=2 ttl=62 time=0.069 ms
    64 bytes from 10.0.2.1: icmp_seq=3 ttl=62 time=0.094 ms
    64 bytes from 10.0.2.1: icmp_seq=4 ttl=62 time=0.093 ms
    64 bytes from 10.0.2.1: icmp_seq=5 ttl=62 time=0.063 ms
    64 bytes from 10.0.2.1: icmp_seq=6 ttl=62 time=0.067 ms
    64 bytes from 10.0.2.1: icmp_seq=7 ttl=62 time=0.093 ms
    64 bytes from 10.0.2.1: icmp_seq=8 ttl=62 time=0.068 ms
    64 bytes from 10.0.2.1: icmp_seq=9 ttl=62 time=0.066 ms
    64 bytes from 10.0.2.1: icmp_seq=10 ttl=62 time=0.058 ms
    64 bytes from 10.0.2.1: icmp_seq=11 ttl=62 time=0.065 ms
    64 bytes from 10.0.2.1: icmp_seq=12 ttl=62 time=0.067 ms
    64 bytes from 10.0.2.1: icmp_seq=13 ttl=62 time=0.057 ms
    --- 10.0.2.1 ping statistics ---
    13 packets transmitted, 13 received, 0% packet loss, time 12286ms
    rtt min/avg/max/mdev = 0.051/0.070/0.094/0.013 ms

```

Now, let's add `100ms` delay with:

> `tc qdisc add dev r1-r2 root netem delay 100ms`

now, ping again:

```
root@safiqul-virtual-machine:data2410-lab/lab-setup/delay-bandwidth# ping 10.0.2.1
PING 10.0.2.1 (10.0.2.1) 56(84) bytes of data.
64 bytes from 10.0.2.1: icmp_seq=1 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=2 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=3 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=4 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=5 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=6 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=7 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=8 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=9 ttl=62 time=101 ms
--- 10.0.2.1 ping statistics ---
9 packets transmitted, 9 received, 0% packet loss, time 8011ms
rtt min/avg/max/mdev = 100.253/100.353/100.549/0.096 ms
```

> **Task:** change the delay to 50ms by replacing `add` with `change` and ping h2 from h1


Use the following if you want to delete the rule:

> `tc qdisc del dev r1-r2 root netem delay 100ms`

ping again and see what happens.

> **NOTE:** I renamed the interface name of r1 to `r1-r2`. The default naming convention is always: nodename-eth# (e.g.m r1-eth0 or r1-eth1)


## Part 2: Other network parameters

You have already learned that packets could be lost, duplicated, reordered, or corrupted. Let's add our own rules to see the affect of these parameters.

### Emulate packet loss:

Restore the default configuration by deleting the previous rules:

`tc qdisc del dev r1-r2 root netem`


The following command adds 50% packet losess at the r1's outgoing interface

> `sudo tc qdisc add dev r1-r2 root netem loss 50%`

Let's ping h1 from h2 to see the above command in action:

```
root@safiqul-virtual-machine:data2410-lab/lab-setup/delay-bandwidth# ping 10.0.2
.1
PING 10.0.2.1 (10.0.2.1) 56(84) bytes of data.
64 bytes from 10.0.2.1: icmp_seq=2 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=3 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=5 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=6 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=10 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=11 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=12 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=13 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=14 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=16 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=19 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=20 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=24 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=25 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=26 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=27 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=28 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=31 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=32 ttl=62 time=100 ms
^C
--- 10.0.2.1 ping statistics ---
32 packets transmitted, 19 received, 40.625% packet loss, time 31242ms
rtt min/avg/max/mdev = 100.105/100.301/100.457/0.107 ms

```

### Emulate packet duplication

Restore the default configuration by deleting the previous rules:

`tc qdisc del dev r1-r2 root netem`


The command below produces a duplication of 50%.  

> `tc qdisc add dev r1-r2 root netem delay 100ms duplicate 50%`

```

See the ping output from h1 to h2. Packets are marked with (DUP!)

root@safiqul-virtual-machine:data2410-lab/lab-setup/delay-bandwidth# ping 10.0.2.1
PING 10.0.2.1 (10.0.2.1) 56(84) bytes of data.
64 bytes from 10.0.2.1: icmp_seq=1 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=2 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=3 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=3 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=4 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=5 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=5 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=6 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=7 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=8 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=9 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=10 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=10 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=11 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=11 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=12 ttl=62 time=101 ms
64 bytes from 10.0.2.1: icmp_seq=12 ttl=62 time=101 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=13 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=13 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=14 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=14 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=15 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=15 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=16 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=16 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=17 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=18 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=18 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=19 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=19 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=20 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=20 ttl=62 time=100 ms (DUP!)
64 bytes from 10.0.2.1: icmp_seq=21 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=22 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=22 ttl=62 time=100 ms (DUP!)
^C
--- 10.0.2.1 ping statistics ---
22 packets transmitted, 22 received, +13 duplicates, 0% packet loss, time 21032ms
rtt min/avg/max/mdev = 100.193/100.345/100.873/0.157 ms
```


#### Effect of Jitter (variation of delay)

Restore the default configuration by deleting the previous rukes:

`tc qdisc del dev r1-r2 root netem`

use the followind command to see the effect of jitter:

> `sudo tc qdisc add dev r1-r2 root netem delay 100ms 20ms`

This will add 100ms delay with a random variation of +/- 20 ms.

**Task** Ping h2 from h1 and explain your answer


#### Effect of packet reordering

Restore the default configuration by deleting the previous rules:

`tc qdisc del dev r1-r2 root netem`

Then, add the following to see the effect of packet reordering.


> `sudo tc qdisc add dev r1-r2 root netem delay 100ms reorder 50% 50%`

Here, This will transfer 50% of the packets with a correlation value of 50%.  The other 50% will experience delay by 100ms.

Here is our ping output between h1 and h2:

```
root@safiqul-virtual-machine:data2410-lab/lab-setup/delay-bandwidth# ping 10.0.2.1
PING 10.0.2.1 (10.0.2.1) 56(84) bytes of data.
64 bytes from 10.0.2.1: icmp_seq=1 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=2 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=3 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=4 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=5 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=6 ttl=62 time=0.101 ms
64 bytes from 10.0.2.1: icmp_seq=7 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=8 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=9 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=10 ttl=62 time=0.052 ms
64 bytes from 10.0.2.1: icmp_seq=11 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=12 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=13 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=14 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=15 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=16 ttl=62 time=0.073 ms
64 bytes from 10.0.2.1: icmp_seq=17 ttl=62 time=0.072 ms
64 bytes from 10.0.2.1: icmp_seq=18 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=19 ttl=62 time=0.095 ms
64 bytes from 10.0.2.1: icmp_seq=20 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=21 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=22 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=23 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=24 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=25 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=26 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=27 ttl=62 time=0.122 ms
64 bytes from 10.0.2.1: icmp_seq=28 ttl=62 time=100 ms
64 bytes from 10.0.2.1: icmp_seq=29 ttl=62 time=100 ms
^C
--- 10.0.2.1 ping statistics ---
29 packets transmitted, 29 received, 0% packet loss, time 28162ms
rtt min/avg/max/mdev = 0.052/79.618/100.489/40.621 ms
```

Look at icmp_seq 6 and 10 - they did not experience any delay. While packets 1-5 experienced delay of 100ms.





