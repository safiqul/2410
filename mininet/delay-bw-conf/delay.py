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
