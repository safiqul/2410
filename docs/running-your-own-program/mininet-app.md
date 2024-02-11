# Mininet: Running your own applications

## Overview

You have learned how to create your own network with a few lines of python codes. In this lab, you will learn how to run your own applications in  end-hosts. 

* [Part 1: Running your applications](#part-1-running-your-applications)
* [Part 2: Analyzing traces with Wireshark](#part-2-analysing-traces-with-wireshark)

## Learning outcomes

After completing this lab, you will:

* learn how to run your applications in hosts
* learn how to use tcpdump to capture traffic and analyse them with wireshark

## Required packages

[`tcpdump`](https://www.tcpdump.org) is a command-line based packet analyser, used for analysing network traffic by intercepting and displaying packets that are sent to/ recived from the network. It runs only on Linux and most UNIX-type operating systems. 

Install tcpdump:

`sudo apt install tcpdump`



## Part 1: Running your applications

* Transfer your simple client-server code and oblig code (task 1 (webserver.py) and task 2 (webclient.py)) in the mininet directory. 

* After that, run your mininet script to create a topology with 2 hosts and a router (see lab: creating topologies for more info) with:

`sudo python3 simpletopo.py`

* open terminals for h1, r2, and h3

`mininet> xterm h1 h3 r2`

* Run your server code on h3:

`sudo python3 webserver.py`

* run the following comand on r2:

`tcpdump -i r2-eth1 -tttt -w traces.pcap`

*Arguments used in the tcpdump command:*

`-i r2-eth1` -  listen on the r2-eth1 interface

`-tttt`  -  Give maximally human-readable timestamp output.

`-w traces.pcap`  -  write captured traffic to traces.pcap file. You can use Wireshark to
open this trace file.


* Run your client code on h1:

`sudo python3 webclient.py`

* stop the tcpdump process on r2 with `ctrl` and `c`

* stop the webserver on h3 with `ctrl` and `c`


> **NOTE:** Don't forget to replace the IP addresses with the correct ones. *Hint:* Use `ifconfig` to find out the IP addresses of h1 and h3. 


## Part 2: Analysing traces with Wireshark


* Open your traces.pcap file with Wireshark and analyse the captured packets.

> Q: Can you explain the communication between the client-server pair by looking at the traces? 


