# Network Fundamentals - CCNA Level Guide

## Table of Contents
1. [Network Fundamentals](#network-fundamentals)
2. [OSI Model](#osi-model)
3. [TCP/IP Model](#tcpip-model)
4. [IP Addressing](#ip-addressing)
5. [Subnetting](#subnetting)
6. [Routing Protocols](#routing-protocols)
7. [Firewalls](#firewalls)
8. [Common Ports](#common-ports)
9. [Network Devices](#network-devices)
10. [Key Terms Glossary](#key-terms-glossary)
11. [Network Topology Map](#network-topology-map)

---

## Network Fundamentals

### What is a Network?
A computer network is a collection of interconnected devices that can communicate and share resources with each other. Networks enable data transmission, resource sharing, and collaborative communication.

### Network Types
- **LAN (Local Area Network)**: Network within a limited area (building, campus)
- **WAN (Wide Area Network)**: Network spanning large geographical areas
- **MAN (Metropolitan Area Network)**: Network covering a city or metropolitan area
- **PAN (Personal Area Network)**: Small network for personal devices (Bluetooth, etc.)
- **WLAN (Wireless Local Area Network)**: Wireless version of LAN

### Network Topologies
- **Bus**: All devices connected to a single cable
- **Star**: All devices connected to a central hub/switch
- **Ring**: Devices connected in a circular fashion
- **Mesh**: Every device connected to every other device
- **Hybrid**: Combination of two or more topologies

---

## OSI Model

The **OSI (Open Systems Interconnection)** model is a conceptual framework with 7 layers:

### Layer 7 - Application Layer
- **Function**: User interface, application services
- **Protocols**: HTTP, HTTPS, FTP, SMTP, DNS, DHCP, Telnet, SSH
- **Devices**: Application gateways, proxies
- **Data Unit**: Data

### Layer 6 - Presentation Layer
- **Function**: Data translation, encryption, compression
- **Protocols**: SSL/TLS, JPEG, GIF, MPEG
- **Data Unit**: Data

### Layer 5 - Session Layer
- **Function**: Manages sessions between applications
- **Protocols**: NetBIOS, RPC, PPTP
- **Data Unit**: Data

### Layer 4 - Transport Layer
- **Function**: End-to-end communication, reliability
- **Protocols**: TCP (connection-oriented), UDP (connectionless)
- **Devices**: Layer 4 switches, load balancers
- **Data Unit**: Segment (TCP) / Datagram (UDP)

### Layer 3 - Network Layer
- **Function**: Logical addressing, routing, path determination
- **Protocols**: IP, ICMP, IGMP, IPsec, OSPF, EIGRP, BGP
- **Devices**: Routers, Layer 3 switches
- **Data Unit**: Packet

### Layer 2 - Data Link Layer
- **Function**: Physical addressing (MAC), frame formatting, error detection
- **Protocols**: Ethernet, PPP, Frame Relay, HDLC
- **Devices**: Switches, bridges, NICs
- **Data Unit**: Frame
- **Sub-layers**: LLC (Logical Link Control), MAC (Media Access Control)

### Layer 1 - Physical Layer
- **Function**: Physical transmission of bits
- **Components**: Cables, connectors, hubs, repeaters
- **Standards**: 10BASE-T, 100BASE-TX, 1000BASE-T
- **Data Unit**: Bits

**Mnemonic**: "Please Do Not Throw Sausage Pizza Away"

---

## TCP/IP Model

The TCP/IP model has 4 layers (compared to OSI's 7):

1. **Application Layer** (combines OSI layers 5-7)
2. **Transport Layer** (OSI Layer 4)
3. **Internet Layer** (OSI Layer 3)
4. **Network Access Layer** (combines OSI layers 1-2)

---

## IP Addressing

### IPv4
- **Format**: 32-bit address (4 octets)
- **Example**: 192.168.1.1
- **Total Addresses**: ~4.3 billion

#### IPv4 Classes

| Class | Range | Default Subnet Mask | Network/Host Bits | Usage |
|-------|-------|---------------------|-------------------|-------|
| A | 1.0.0.0 - 126.255.255.255 | 255.0.0.0 (/8) | 8/24 | Large organizations |
| B | 128.0.0.0 - 191.255.255.255 | 255.255.0.0 (/16) | 16/16 | Medium organizations |
| C | 192.0.0.0 - 223.255.255.255 | 255.255.255.0 (/24) | 24/8 | Small organizations |
| D | 224.0.0.0 - 239.255.255.255 | N/A | N/A | Multicast |
| E | 240.0.0.0 - 255.255.255.255 | N/A | N/A | Experimental |

#### Private IP Ranges (RFC 1918)
- **Class A**: 10.0.0.0 - 10.255.255.255 (/8)
- **Class B**: 172.16.0.0 - 172.31.255.255 (/12)
- **Class C**: 192.168.0.0 - 192.168.255.255 (/16)

#### Special IP Addresses
- **127.0.0.1**: Loopback address (localhost)
- **0.0.0.0**: Default route or unknown address
- **255.255.255.255**: Broadcast address
- **169.254.0.0/16**: APIPA (Automatic Private IP Addressing)

### IPv6
- **Format**: 128-bit address (8 groups of 4 hexadecimal digits)
- **Example**: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
- **Shortened**: 2001:db8:85a3::8a2e:370:7334
- **Total Addresses**: 340 undecillion

#### IPv6 Address Types
- **Unicast**: Single interface
- **Multicast**: Multiple interfaces
- **Anycast**: Nearest interface in a group

---

## Subnetting

### CIDR (Classless Inter-Domain Routing)
CIDR notation: IP address followed by /prefix length
- Example: 192.168.1.0/24

### Subnet Mask Cheat Sheet

| CIDR | Subnet Mask | Hosts | Subnets |
|------|-------------|-------|---------|
| /24 | 255.255.255.0 | 254 | 256 |
| /25 | 255.255.255.128 | 126 | 512 |
| /26 | 255.255.255.192 | 62 | 1024 |
| /27 | 255.255.255.224 | 30 | 2048 |
| /28 | 255.255.255.240 | 14 | 4096 |
| /29 | 255.255.255.248 | 6 | 8192 |
| /30 | 255.255.255.252 | 2 | 16384 |

### Subnetting Formula
- **Number of Subnets**: 2^n (n = borrowed bits)
- **Number of Hosts**: 2^h - 2 (h = host bits)
- **Network Address**: First address in subnet
- **Broadcast Address**: Last address in subnet

### VLSM (Variable Length Subnet Masking)
Allows different subnet masks within the same network for efficient IP utilization.

---

## Routing Protocols

### Static vs. Dynamic Routing

#### Static Routing
- **Pros**: Secure, no overhead, predictable
- **Cons**: Not scalable, manual configuration
- **Use Case**: Small networks, stub networks

#### Dynamic Routing
- **Pros**: Automatic route discovery, scalable, adapts to changes
- **Cons**: Resource overhead, complexity
- **Use Case**: Large, dynamic networks

### Routing Protocol Categories

#### Interior Gateway Protocols (IGP)
Used within an autonomous system (AS).

##### Distance Vector Protocols
- **Metric**: Hop count
- **Algorithm**: Bellman-Ford
- **Updates**: Periodic, broadcast entire routing table

**RIP (Routing Information Protocol)**
- **Version**: RIPv1 (classful), RIPv2 (classless)
- **Metric**: Hop count (max 15 hops)
- **Update Timer**: 30 seconds
- **Administrative Distance**: 120
- **Pros**: Simple, easy to configure
- **Cons**: Slow convergence, limited scalability

**EIGRP (Enhanced Interior Gateway Routing Protocol)**
- **Type**: Advanced distance vector (hybrid)
- **Vendor**: Cisco proprietary
- **Metric**: Bandwidth, delay, load, reliability
- **Features**: Fast convergence, VLSM support, unequal cost load balancing
- **Administrative Distance**: 90 (internal), 170 (external)
- **Algorithm**: DUAL (Diffusing Update Algorithm)

##### Link-State Protocols
- **Metric**: Cost (based on bandwidth)
- **Algorithm**: Dijkstra's SPF
- **Updates**: Triggered, send only changes

**OSPF (Open Shortest Path First)**
- **Standard**: RFC 2328 (v2), RFC 5340 (v3)
- **Metric**: Cost (100,000,000 / bandwidth in bps)
- **Areas**: Hierarchical design with Area 0 (backbone)
- **Administrative Distance**: 110
- **Features**: Fast convergence, classless, scalable
- **Types of LSAs**: Router LSA, Network LSA, Summary LSA, etc.
- **Neighbor States**: Down, Init, 2-Way, ExStart, Exchange, Loading, Full

**IS-IS (Intermediate System to Intermediate System)**
- **Use**: Service provider networks
- **Metric**: Cost
- **Features**: Similar to OSPF, works at Layer 2

#### Exterior Gateway Protocols (EGP)
Used between autonomous systems.

**BGP (Border Gateway Protocol)**
- **Version**: BGP-4
- **Type**: Path vector protocol
- **Metric**: AS path, local preference, MED
- **Administrative Distance**: 20 (eBGP), 200 (iBGP)
- **Use**: Internet routing, connecting ISPs
- **Features**: Policy-based routing, supports CIDR
- **Port**: TCP 179

### Administrative Distance (AD)

| Route Source | AD Value |
|--------------|----------|
| Connected | 0 |
| Static | 1 |
| EIGRP Summary | 5 |
| eBGP | 20 |
| EIGRP Internal | 90 |
| IGRP | 100 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| EIGRP External | 170 |
| iBGP | 200 |
| Unknown | 255 |

---

## Firewalls

### What is a Firewall?
A network security device that monitors and controls incoming and outgoing network traffic based on predetermined security rules.

### Firewall Types

#### Based on Deployment
1. **Network Firewall**: Hardware appliance protecting network perimeter
2. **Host-based Firewall**: Software on individual devices
3. **Cloud Firewall**: Virtual firewall in cloud environments (FWaaS)

#### Based on Functionality

##### Packet Filtering Firewall (Layer 3-4)
- **Operation**: Examines packet headers (IP, port, protocol)
- **Stateless**: Each packet evaluated independently
- **Pros**: Fast, low resource usage
- **Cons**: No context awareness, vulnerable to spoofing

##### Stateful Inspection Firewall (Layer 3-4)
- **Operation**: Tracks connection state
- **Features**: Maintains state table of active connections
- **Pros**: Better security than packet filtering
- **Cons**: More resource intensive

##### Application Layer Firewall (Layer 7)
- **Operation**: Deep packet inspection, examines application data
- **Also known as**: Proxy firewall, application gateway
- **Pros**: Granular control, content filtering
- **Cons**: Performance impact, complexity

##### Next-Generation Firewall (NGFW)
- **Features**:
  - Traditional firewall capabilities
  - Intrusion Prevention System (IPS)
  - Application awareness and control
  - Threat intelligence
  - SSL/TLS inspection
  - User identity integration
- **Examples**: Palo Alto, Fortinet, Cisco Firepower

##### Unified Threat Management (UTM)
- **Features**: All-in-one security appliance
  - Firewall
  - Antivirus
  - Content filtering
  - Spam filtering
  - VPN

### Firewall Rules
- **Default Deny**: Block all traffic except explicitly allowed
- **Default Allow**: Allow all traffic except explicitly blocked
- **Rule Components**:
  - Source IP/network
  - Destination IP/network
  - Protocol (TCP/UDP/ICMP)
  - Source port
  - Destination port
  - Action (permit/deny)

### Firewall Zones
- **Inside/Trusted**: Internal corporate network
- **Outside/Untrusted**: External networks (Internet)
- **DMZ (Demilitarized Zone)**: Semi-trusted zone for public-facing servers

### Security Levels (Cisco ASA)
- **Inside**: Security level 100
- **DMZ**: Security level 50
- **Outside**: Security level 0
- **Rule**: Traffic flows from higher to lower by default

---

## Common Ports

### Well-Known Ports (0-1023)

#### TCP Ports
| Port | Protocol | Description |
|------|----------|-------------|
| 20 | FTP Data | File Transfer Protocol (data) |
| 21 | FTP Control | File Transfer Protocol (control) |
| 22 | SSH | Secure Shell |
| 23 | Telnet | Unencrypted remote access |
| 25 | SMTP | Simple Mail Transfer Protocol |
| 53 | DNS | Domain Name System (also UDP) |
| 80 | HTTP | Hypertext Transfer Protocol |
| 110 | POP3 | Post Office Protocol v3 |
| 143 | IMAP | Internet Message Access Protocol |
| 443 | HTTPS | HTTP Secure (SSL/TLS) |
| 445 | SMB | Server Message Block |
| 465 | SMTPS | SMTP Secure |
| 587 | SMTP | Mail submission |
| 993 | IMAPS | IMAP Secure |
| 995 | POP3S | POP3 Secure |
| 3306 | MySQL | MySQL Database |
| 3389 | RDP | Remote Desktop Protocol |
| 5432 | PostgreSQL | PostgreSQL Database |
| 8080 | HTTP Alt | Alternative HTTP port |

#### UDP Ports
| Port | Protocol | Description |
|------|----------|-------------|
| 53 | DNS | Domain Name System |
| 67 | DHCP Server | Dynamic Host Configuration Protocol |
| 68 | DHCP Client | DHCP client |
| 69 | TFTP | Trivial File Transfer Protocol |
| 123 | NTP | Network Time Protocol |
| 161 | SNMP | Simple Network Management Protocol |
| 162 | SNMP Trap | SNMP Notifications |
| 514 | Syslog | System Logging |
| 520 | RIP | Routing Information Protocol |

#### Both TCP and UDP
| Port | Protocol | Description |
|------|----------|-------------|
| 53 | DNS | Domain Name System |
| 88 | Kerberos | Authentication |
| 389 | LDAP | Lightweight Directory Access Protocol |
| 636 | LDAPS | LDAP Secure |

### Registered Ports (1024-49151)
Used by applications and services.

### Dynamic/Private Ports (49152-65535)
Ephemeral ports used by client applications.

---

## Network Devices

### Layer 1 Devices

#### Hub
- **Function**: Broadcasts data to all ports
- **Type**: Passive (no power) or Active (with power)
- **Collision Domain**: Single collision domain
- **Broadcast Domain**: Single broadcast domain
- **Use**: Obsolete, replaced by switches

#### Repeater
- **Function**: Regenerates and amplifies signals
- **Use**: Extends network cable distance

### Layer 2 Devices

#### Switch
- **Function**: Forwards frames based on MAC addresses
- **MAC Address Table**: Learns MAC addresses dynamically
- **Collision Domain**: Separate collision domain per port
- **Broadcast Domain**: Single broadcast domain
- **Features**:
  - Full-duplex communication
  - VLAN support
  - Spanning Tree Protocol (STP)
  - Port security

#### Bridge
- **Function**: Connects two network segments
- **Difference from Switch**: Fewer ports, software-based
- **Use**: Legacy device, mostly replaced by switches

### Layer 3 Devices

#### Router
- **Function**: Routes packets between networks based on IP addresses
- **Routing Table**: Stores network paths
- **Collision Domain**: Separate per port
- **Broadcast Domain**: Separate per interface
- **Features**:
  - Inter-VLAN routing
  - NAT/PAT
  - Access Control Lists (ACLs)
  - QoS (Quality of Service)
  - Routing protocols

#### Layer 3 Switch
- **Function**: Switch with routing capabilities
- **Difference from Router**: Hardware-based routing, faster
- **Use**: Data center, campus core networks

### Other Network Devices

#### Wireless Access Point (WAP)
- **Function**: Provides wireless connectivity
- **Standards**: 802.11a/b/g/n/ac/ax (Wi-Fi 6)

#### Modem
- **Function**: Modulates and demodulates signals
- **Types**: DSL, cable, fiber

#### Load Balancer
- **Function**: Distributes traffic across multiple servers
- **Algorithms**: Round-robin, least connections, IP hash

#### Proxy Server
- **Function**: Intermediary between clients and servers
- **Types**: Forward proxy, reverse proxy

#### Firewall
- **Function**: Network security device (see Firewalls section)

---

## Key Terms Glossary

### A
- **ACL (Access Control List)**: Rules that permit or deny traffic
- **ARP (Address Resolution Protocol)**: Resolves IP to MAC addresses
- **AS (Autonomous System)**: Collection of IP networks under single administrative control

### B
- **Bandwidth**: Maximum data transfer rate
- **BGP (Border Gateway Protocol)**: Exterior gateway routing protocol
- **Broadcast Domain**: Set of devices that receive broadcast frames

### C
- **CAM Table**: Content Addressable Memory, stores MAC addresses in switches
- **CIDR**: Classless Inter-Domain Routing
- **Collision Domain**: Network segment where collisions can occur
- **Convergence**: Time for all routers to agree on network topology

### D
- **DHCP (Dynamic Host Configuration Protocol)**: Automatically assigns IP addresses
- **DNS (Domain Name System)**: Translates domain names to IP addresses
- **Duplex**: Full-duplex (simultaneous send/receive), Half-duplex (one direction at a time)

### E
- **Encapsulation**: Wrapping data with protocol headers
- **Ethernet**: Layer 2 protocol for LAN communication

### F
- **FIB (Forwarding Information Base)**: Used by routers for packet forwarding
- **Frame**: Layer 2 data unit

### G
- **Gateway**: Device connecting different networks (usually a router)
- **GRE (Generic Routing Encapsulation)**: Tunneling protocol

### H
- **HSRP (Hot Standby Router Protocol)**: Cisco redundancy protocol
- **HTTP/HTTPS**: Web protocols

### I
- **ICMP (Internet Control Message Protocol)**: Used by ping, traceroute
- **IGMP (Internet Group Management Protocol)**: Manages multicast groups
- **Ingress**: Incoming traffic
- **IPsec**: Security protocol for VPNs

### L
- **Latency**: Delay in network communication
- **Load Balancing**: Distributing traffic across multiple paths

### M
- **MAC Address**: 48-bit physical address (e.g., 00:1A:2B:3C:4D:5E)
- **MTU (Maximum Transmission Unit)**: Largest packet size (usually 1500 bytes)
- **Multicast**: One-to-many communication

### N
- **NAT (Network Address Translation)**: Translates private to public IP
- **PAT (Port Address Translation)**: NAT with port mapping
- **Next Hop**: Next router in packet path

### O
- **OSI Model**: 7-layer network reference model

### P
- **Packet**: Layer 3 data unit
- **Port**: Logical endpoint for communication
- **Protocol**: Set of rules for communication

### Q
- **QoS (Quality of Service)**: Prioritizes network traffic

### R
- **Routing Table**: Database of network routes
- **RIB (Routing Information Base)**: Contains all routes known to router

### S
- **Segment**: Layer 4 data unit (TCP)
- **Subnet**: Subdivision of IP network
- **STP (Spanning Tree Protocol)**: Prevents Layer 2 loops
- **Switch**: Layer 2 device

### T
- **TCP (Transmission Control Protocol)**: Reliable, connection-oriented protocol
- **Three-Way Handshake**: TCP connection establishment (SYN, SYN-ACK, ACK)
- **TTL (Time To Live)**: Hop count limit in IP header
- **Trunk**: Port carrying multiple VLANs

### U
- **UDP (User Datagram Protocol)**: Unreliable, connectionless protocol
- **Unicast**: One-to-one communication

### V
- **VLAN (Virtual LAN)**: Logical network segmentation
- **VPN (Virtual Private Network)**: Secure encrypted tunnel
- **VRRP (Virtual Router Redundancy Protocol)**: Redundancy protocol

### W
- **WAN**: Wide Area Network
- **Wildcard Mask**: Inverse of subnet mask (used in ACLs)

---

## Network Topology Map

### Example Enterprise Network Diagram

```
                            INTERNET
                                |
                                |
                    [Border Router] (BGP)
                                |
                                |
                    [Edge Firewall] (NGFW)
                                |
                                |
        +----------------------DMZ----------------------+
        |                      |                       |
   [Web Server]         [Mail Server]            [DNS Server]
   (HTTP/HTTPS)            (SMTP)                   (DNS)
        +------------------------------------------------+
                                |
                                |
                    [Internal Firewall]
                                |
                                |
                    [Core Layer Switch] (L3)
                     (OSPF/EIGRP)
                                |
                                |
        +-----------------------+------------------------+
        |                       |                        |
[Distribution L3 Switch] [Distribution L3 Switch]  [Distribution L3 Switch]
    (VLAN 10-20)             (VLAN 30-40)            (VLAN 50-60)
        |                       |                        |
        |                       |                        |
   +----+----+             +----+----+              +----+----+
   |         |             |         |              |         |
[Access   [Access      [Access   [Access        [Access   [Access
Switch]   Switch]      Switch]   Switch]        Switch]   Switch]
   |         |             |         |              |         |
   |         |             |         |              |         |
[End     [End          [End     [End            [End     [End
Users]   Users]        Users]   Users]          Users]   Users]
(VLAN    (VLAN         (VLAN    (VLAN           (VLAN    (VLAN
 10)      20)           30)      40)             50)      60)
```

### Network Segments

#### VLAN Design Example
- **VLAN 10**: Management Network (10.0.10.0/24)
- **VLAN 20**: Employee Network (10.0.20.0/24)
- **VLAN 30**: Guest Network (10.0.30.0/24)
- **VLAN 40**: Voice Network (10.0.40.0/24)
- **VLAN 50**: Server Network (10.0.50.0/24)
- **VLAN 60**: Security/IoT Network (10.0.60.0/24)

### Three-Tier Network Architecture

#### Core Layer
- **Function**: High-speed backbone, packet forwarding
- **Devices**: Layer 3 switches, high-end routers
- **Features**: Redundancy, fast convergence, no ACLs

#### Distribution Layer
- **Function**: Routing, filtering, inter-VLAN routing
- **Devices**: Layer 3 switches, routers
- **Features**: ACLs, QoS policies, route redistribution

#### Access Layer
- **Function**: End-user connectivity
- **Devices**: Layer 2 switches, wireless APs
- **Features**: Port security, VLAN assignment, PoE

---

## Network Troubleshooting Commands

### Common Commands

```bash
# Connectivity Testing
ping <destination>              # Test reachability
ping -t <destination>           # Continuous ping (Windows)
ping -c 4 <destination>         # 4 pings (Linux)

# Route Tracing
tracert <destination>           # Windows
traceroute <destination>        # Linux/Mac

# DNS Lookup
nslookup <domain>               # DNS query
dig <domain>                    # Detailed DNS query (Linux)

# Network Configuration
ipconfig                        # Windows
ipconfig /all                   # Detailed info
ifconfig                        # Linux/Mac (deprecated)
ip addr show                    # Linux (modern)
ip route show                   # Show routing table

# ARP Cache
arp -a                          # View ARP cache
arp -d                          # Clear ARP cache

# Network Statistics
netstat -an                     # Active connections
netstat -rn                     # Routing table
ss -tuln                        # Socket statistics (Linux)

# Cisco IOS Commands
show ip interface brief         # Interface status
show ip route                   # Routing table
show running-config             # Current configuration
show vlan brief                 # VLAN information
show mac address-table          # MAC address table
show ip protocols               # Routing protocols
show ip ospf neighbor           # OSPF neighbors
show ip eigrp neighbors         # EIGRP neighbors
```

---

## Best Practices

### Network Design
1. **Hierarchical Design**: Use core, distribution, access layers
2. **Redundancy**: Implement redundant paths and devices
3. **Scalability**: Design for future growth
4. **Security**: Defense in depth, segmentation
5. **Documentation**: Maintain network diagrams and IP schemes

### IP Addressing
1. **Use Private IPs**: Internally with NAT for Internet access
2. **Plan Subnetting**: Allocate IP space efficiently with VLSM
3. **Reserve Space**: For growth and expansion
4. **Document**: Maintain IP address management (IPAM)

### Routing
1. **Use Dynamic Routing**: In large networks for scalability
2. **Summarization**: Reduce routing table size
3. **Default Routes**: For Internet-bound traffic
4. **Redundancy**: Multiple paths for reliability

### Security
1. **Least Privilege**: Allow only necessary traffic
2. **Segmentation**: Use VLANs and firewalls
3. **ACLs**: Filter traffic at boundaries
4. **Monitoring**: Log and monitor network activity
5. **Updates**: Keep firmware and software current

---

## Summary

This guide covers the essential network fundamentals at CCNA level, including:
- OSI and TCP/IP models
- IP addressing and subnetting
- Routing protocols (RIP, EIGRP, OSPF, BGP)
- Firewall types and configurations
- Common ports and protocols
- Network devices and their functions
- Key networking terms
- Network topology and design

Use this as a reference for studying, interviews, or day-to-day network administration tasks.

---

**Last Updated**: October 2025
**Target Audience**: CCNA-level network engineers, system administrators
**Version**: 1.0
