# Network Technologies and Protocols Guide

## Table of Contents
- [VRF (Virtual Routing and Forwarding)](#vrf)
- [Routing Protocols](#routing-protocols)
  - [OSPF](#ospf)
  - [EIGRP](#eigrp)
  - [BGP](#bgp)
  - [IS-IS](#is-is)
  - [RIP](#rip)
- [FHRP Protocols](#fhrp-protocols)
  - [HSRP](#hsrp)
  - [GLBP](#glbp)
- [Multicast](#multicast)
- [Network Address Translation (NAT)](#nat)
- [LISP](#lisp)
- [MPLS](#mpls)
- [Security Technologies](#security-technologies)
  - [ASA](#asa)
  - [IPSec](#ipsec)
  - [VPN](#vpn)
  - [GRE](#gre)
- [Access Control](#access-control)
  - [Access-List (ACL)](#access-list-acl)
- [Protocol Differences](#protocol-differences)
  - [TCP vs UDP](#tcp-vs-udp)
- [HTTPS Communication](#https-communication)
- [Security Concepts](#security-concepts)
- [Layer 2 Security](#layer-2-security)
  - [Port-Security](#port-security)
  - [DHCP Snooping](#dhcp-snooping)
- [AAA, TACACS+, and RADIUS](#aaa-tacacs-radius)

---

## VRF (Virtual Routing and Forwarding) {#vrf}

### Overview
VRF is a technology that allows multiple instances of a routing table to coexist within the same router simultaneously. It provides network path isolation and segmentation.

### Key Concepts
- **Logical Separation**: Creates independent routing instances on a single physical device
- **Use Cases**:
  - Service provider networks (separating customer traffic)
  - Enterprise networks (separating departments or security zones)
  - Multi-tenancy environments

### Configuration Example
```
ip vrf CUSTOMER_A
 rd 100:1
 route-target export 100:1
 route-target import 100:1

interface GigabitEthernet0/0
 ip vrf forwarding CUSTOMER_A
 ip address 10.1.1.1 255.255.255.0
```

### Benefits
- Traffic isolation between VRFs
- Overlapping IP address spaces
- Enhanced security
- Simplified network management

---

## Routing Protocols

## OSPF (Open Shortest Path First) {#ospf}

### Overview
OSPF is a link-state routing protocol that uses Dijkstra's algorithm to calculate the shortest path. It's an IGP (Interior Gateway Protocol) designed for IP networks.

### Key Features
- **Protocol Type**: Link-State
- **Algorithm**: Dijkstra's Shortest Path First (SPF)
- **Metric**: Cost (based on bandwidth)
- **Administrative Distance**: 110
- **Multicast Addresses**: 224.0.0.5 (All OSPF Routers), 224.0.0.6 (DR/BDR)

### OSPF Areas
- **Area 0 (Backbone)**: All areas must connect to Area 0
- **Standard Areas**: Can contain all LSA types
- **Stub Areas**: Block external routes (Type 5 LSAs)
- **Totally Stubby Areas**: Block external and inter-area routes
- **NSSA**: Allows limited external routes

### OSPF Packet Types
1. **Hello**: Neighbor discovery and keepalive
2. **DBD (Database Description)**: Summary of LSDB
3. **LSR (Link State Request)**: Request specific LSAs
4. **LSU (Link State Update)**: Send LSAs
5. **LSAck**: Acknowledge received LSAs

### OSPF States
1. Down
2. Init
3. Two-Way
4. ExStart
5. Exchange
6. Loading
7. Full

### Configuration Example
```
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.0.255 area 0
 network 192.168.1.0 0.0.0.255 area 1
```

### Best Practices
- Design hierarchical topology with proper area planning
- Use area summarization to reduce routing table size
- Implement authentication for security
- Tune timers for faster convergence in critical areas

---

## EIGRP (Enhanced Interior Gateway Routing Protocol) {#eigrp}

### Overview
EIGRP is Cisco's advanced distance-vector (hybrid) routing protocol that combines the best features of link-state and distance-vector protocols.

### Key Features
- **Protocol Type**: Advanced Distance-Vector (Hybrid)
- **Algorithm**: DUAL (Diffusing Update Algorithm)
- **Metric**: Composite (Bandwidth, Delay, Reliability, Load, MTU)
- **Administrative Distance**: 
  - Internal: 90
  - External: 170
  - Summary: 5
- **Multicast Address**: 224.0.0.10
- **Protocol Number**: 88

### EIGRP Terminology
- **Successor**: Best route to destination
- **Feasible Successor**: Backup route that meets feasibility condition
- **Feasibility Condition**: Prevents routing loops
- **Reported Distance (RD)**: Neighbor's distance to destination
- **Feasible Distance (FD)**: Total distance to destination

### EIGRP Packet Types
1. **Hello**: Neighbor discovery (5 sec on high-speed, 60 sec on low-speed)
2. **Update**: Routing updates
3. **Query**: Ask neighbors about routes
4. **Reply**: Response to queries
5. **Ack**: Acknowledge reliable packets

### Configuration Example
```
router eigrp 100
 network 10.0.0.0
 network 192.168.1.0
 no auto-summary
 eigrp router-id 1.1.1.1
```

### Named EIGRP Configuration
```
router eigrp ENTERPRISE
 address-family ipv4 unicast autonomous-system 100
  network 10.0.0.0
  topology base
  exit-af-topology
 exit-address-family
```

### Advantages
- Fast convergence using DUAL
- Support for VLSM and CIDR
- Unequal-cost load balancing
- Reduced bandwidth usage (incremental updates)
- Support for multiple network layer protocols

---

## BGP (Border Gateway Protocol) {#bgp}

### Overview
BGP is the routing protocol of the Internet, used to exchange routing information between autonomous systems (AS). It's a path-vector protocol.

### Key Features
- **Protocol Type**: Path-Vector
- **Port**: TCP 179
- **Administrative Distance**:
  - eBGP: 20
  - iBGP: 200
- **Metric**: Path attributes (not a simple metric)

### BGP Types
- **eBGP (External BGP)**: Between different autonomous systems
- **iBGP (Internal BGP)**: Within the same autonomous system

### BGP Attributes
**Well-Known Mandatory**:
1. **AS_PATH**: List of AS numbers the route has traversed
2. **NEXT_HOP**: Next hop IP address
3. **ORIGIN**: How route was originated (IGP, EGP, Incomplete)

**Well-Known Discretionary**:
4. **LOCAL_PREF**: Prefer outbound path (higher is better)
5. **ATOMIC_AGGREGATE**: Route has been summarized

**Optional Transitive**:
6. **AGGREGATOR**: Router that performed aggregation
7. **COMMUNITY**: Group routes with common properties

**Optional Non-Transitive**:
8. **MED (Multi-Exit Discriminator)**: Suggest inbound path to neighbor AS (lower is better)
9. **CLUSTER_LIST**: Route reflector cluster IDs
10. **ORIGINATOR_ID**: Router ID of originator in route reflector

### BGP Best Path Selection
1. Highest Weight (Cisco-specific)
2. Highest Local Preference
3. Locally originated route
4. Shortest AS_PATH
5. Lowest Origin type (IGP < EGP < Incomplete)
6. Lowest MED
7. eBGP over iBGP
8. Lowest IGP metric to BGP next hop
9. Oldest route
10. Lowest Router ID
11. Lowest neighbor address

### BGP States
1. **Idle**: Initial state
2. **Connect**: Waiting for TCP connection
3. **Active**: Trying to establish TCP connection
4. **OpenSent**: TCP established, Open message sent
5. **OpenConfirm**: Open message received
6. **Established**: Peers exchanging routing information

### Configuration Example
```
router bgp 65001
 bgp router-id 1.1.1.1
 neighbor 10.1.1.2 remote-as 65002
 neighbor 192.168.1.1 remote-as 65001
 !
 address-family ipv4
  network 10.0.0.0 mask 255.255.255.0
  neighbor 10.1.1.2 activate
  neighbor 192.168.1.1 activate
  neighbor 192.168.1.1 next-hop-self
 exit-address-family
```

### Best Practices
- Use route filtering and prefix lists
- Implement BGP authentication
- Use route reflectors or confederations for iBGP scaling
- Tune timers carefully
- Implement proper security policies

---

## IS-IS (Intermediate System to Intermediate System) {#is-is}

### Overview
IS-IS is a link-state routing protocol originally designed for OSI networks but adapted for IP (Integrated IS-IS). Popular in service provider networks.

### Key Features
- **Protocol Type**: Link-State
- **OSI Layer**: Runs directly on Layer 2 (not IP)
- **Metric**: Cost (default 10 per interface)
- **Administrative Distance**: 115

### IS-IS Levels
- **Level 1 (L1)**: Intra-area routing (like OSPF non-backbone areas)
- **Level 2 (L2)**: Inter-area routing (like OSPF backbone)
- **Level 1-2**: Router participates in both levels

### IS-IS vs OSPF
| Feature | IS-IS | OSPF |
|---------|-------|------|
| Layer | Data Link (L2) | Network (L3) |
| Addressing | NSAP | IP |
| Areas | More flexible | Hierarchical (must connect to Area 0) |
| Scalability | Better | Good |
| Vendor Support | Multi-vendor | Multi-vendor |

### Configuration Example
```
router isis CORE
 net 49.0001.1111.1111.1111.00
 is-type level-2-only
!
interface GigabitEthernet0/0
 ip router isis CORE
 isis circuit-type level-2-only
```

### Advantages
- Fast convergence
- Better scalability than OSPF
- Simpler hierarchy
- Less overhead on links

---

## RIP (Routing Information Protocol) {#rip}

### Overview
RIP is one of the oldest distance-vector routing protocols, simple but limited in modern networks.

### Versions
- **RIPv1**: Classful, no authentication, broadcast updates
- **RIPv2**: Classless, supports VLSM, authentication, multicast updates (224.0.0.9)
- **RIPng**: For IPv6

### Key Features
- **Metric**: Hop count (maximum 15, 16 = unreachable)
- **Administrative Distance**: 120
- **Update Timer**: 30 seconds
- **Invalid Timer**: 180 seconds
- **Flush Timer**: 240 seconds
- **Holddown Timer**: 180 seconds

### Configuration Example
```
router rip
 version 2
 network 10.0.0.0
 network 192.168.1.0
 no auto-summary
```

### Limitations
- Maximum 15 hops
- Slow convergence
- Periodic updates waste bandwidth
- No load balancing support

### When to Use RIP
- Very small networks
- Legacy compatibility
- Learning/lab environments

---

## FHRP Protocols (First Hop Redundancy Protocols) {#fhrp-protocols}

### Overview
FHRPs provide gateway redundancy for hosts by allowing multiple routers to share a virtual IP address.

### Common FHRPs
- **HSRP**: Cisco proprietary
- **VRRP**: Industry standard (RFC 5798)
- **GLBP**: Cisco proprietary with load balancing

---

## HSRP (Hot Standby Router Protocol) {#hsrp}

### Overview
HSRP is Cisco's proprietary FHRP that provides default gateway redundancy.

### Key Features
- **Versions**: HSRPv1 and HSRPv2
- **Virtual MAC**: 
  - v1: 0000.0c07.acXX (XX = group number)
  - v2: 0000.0c9f.fXXX (XXX = group number)
- **Multicast Address**:
  - v1: 224.0.0.2
  - v2: 224.0.0.102
- **Hello Timer**: 3 seconds (default)
- **Hold Timer**: 10 seconds (default)

### HSRP States
1. **Initial**: Starting state
2. **Learn**: Waiting to hear from active router
3. **Listen**: Monitoring hello messages
4. **Speak**: Participating in election
5. **Standby**: Backup router
6. **Active**: Active router forwarding traffic

### HSRP Priority
- Default priority: 100
- Higher priority becomes active
- Preempt must be enabled to take over

### Configuration Example
```
interface GigabitEthernet0/0
 ip address 192.168.1.2 255.255.255.0
 standby 1 ip 192.168.1.1
 standby 1 priority 110
 standby 1 preempt
 standby 1 authentication md5 key-string MySecret
```

### HSRP Load Balancing
Use multiple HSRP groups with different active routers:
```
! Router 1
interface Vlan10
 standby 10 ip 10.1.10.1
 standby 10 priority 110
 standby 10 preempt

interface Vlan20
 standby 20 ip 10.1.20.1
 standby 20 priority 90

! Router 2
interface Vlan10
 standby 10 ip 10.1.10.1
 standby 10 priority 90

interface Vlan20
 standby 20 ip 10.1.20.1
 standby 20 priority 110
 standby 20 preempt
```

---

## GLBP (Gateway Load Balancing Protocol) {#glbp}

### Overview
GLBP is Cisco's proprietary FHRP that provides both redundancy and load balancing across multiple routers.

### Key Features
- **Load Balancing**: Built-in (unlike HSRP/VRRP)
- **Virtual MAC**: 0007.b400.XXYY
- **Multicast Address**: 224.0.0.102
- **Port**: UDP 3222

### GLBP Roles
- **AVG (Active Virtual Gateway)**: Assigns virtual MAC addresses
- **AVF (Active Virtual Forwarder)**: Forwards traffic
- **Standby Virtual Gateway**: Backup for AVG
- **Standby Virtual Forwarder**: Backup for AVF

### Load Balancing Methods
1. **Round-robin** (default): Distributes MAC addresses equally
2. **Weighted**: Based on configured weights
3. **Host-dependent**: Same host always gets same AVF

### Configuration Example
```
interface GigabitEthernet0/0
 ip address 192.168.1.2 255.255.255.0
 glbp 1 ip 192.168.1.1
 glbp 1 priority 110
 glbp 1 preempt
 glbp 1 load-balancing round-robin
 glbp 1 authentication md5 key-string MySecret
```

### GLBP vs HSRP
| Feature | GLBP | HSRP |
|---------|------|------|
| Load Balancing | Yes (built-in) | No (requires multiple groups) |
| Active Routers | Multiple | One |
| Complexity | Higher | Lower |
| CPU Usage | Higher | Lower |
| Vendor | Cisco only | Cisco only |

---

## Multicast {#multicast}

### Overview
Multicast is a method of sending data to multiple receivers simultaneously using a single transmission.

### IP Multicast Addresses
- **Range**: 224.0.0.0 to 239.255.255.255 (Class D)
- **Reserved**: 224.0.0.0 to 224.0.0.255 (local network control)
- **Public**: 224.0.1.0 to 238.255.255.255
- **Private**: 239.0.0.0 to 239.255.255.255

### Common Multicast Addresses
- **224.0.0.1**: All hosts on subnet
- **224.0.0.2**: All routers on subnet
- **224.0.0.5**: All OSPF routers
- **224.0.0.6**: OSPF DR/BDR
- **224.0.0.9**: RIPv2 routers
- **224.0.0.10**: EIGRP routers

### Multicast Protocols

#### IGMP (Internet Group Management Protocol)
- Used between hosts and routers
- Versions: IGMPv1, IGMPv2, IGMPv3
- Functions: Join/leave multicast groups

#### PIM (Protocol Independent Multicast)
**PIM Dense Mode (PIM-DM)**:
- Flood and prune behavior
- Suitable for small networks with many receivers

**PIM Sparse Mode (PIM-SM)**:
- Uses Rendezvous Point (RP)
- Explicit join model
- Scalable for large networks

**PIM Sparse-Dense Mode**:
- Combination of both modes

**PIM Source-Specific Multicast (PIM-SSM)**:
- Receiver specifies both group and source
- No RP required

### Configuration Example
```
! Enable multicast routing
ip multicast-routing

! Configure PIM on interfaces
interface GigabitEthernet0/0
 ip pim sparse-mode

! Configure RP
ip pim rp-address 10.1.1.1
```

### Multicast Distribution Trees
- **Source Tree (SPT)**: Shortest path from source to receivers
- **Shared Tree (RPT)**: Via Rendezvous Point

---

## Network Address Translation (NAT) {#nat}

### Overview
NAT translates private IP addresses to public IP addresses, allowing multiple devices to share a single public IP.

### NAT Types

#### 1. Static NAT
One-to-one mapping between private and public IP.
```
ip nat inside source static 192.168.1.10 203.0.113.10

interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside
```

#### 2. Dynamic NAT
Many-to-many mapping from a pool.
```
ip nat pool PUBLIC_POOL 203.0.113.10 203.0.113.20 netmask 255.255.255.0
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 pool PUBLIC_POOL

interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside
```

#### 3. PAT (Port Address Translation / NAT Overload)
Many-to-one using port numbers.
```
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload

interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside
```

### NAT Terminology
- **Inside Local**: Private IP address (internal network)
- **Inside Global**: Public IP address (after translation)
- **Outside Global**: Public IP of external host
- **Outside Local**: How internal hosts see external address

### Verification Commands
```
show ip nat translations
show ip nat statistics
clear ip nat translation *
debug ip nat
```

---

## LISP (Locator/ID Separation Protocol) {#lisp}

### Overview
LISP separates device identity (EID) from location (RLOC), improving routing scalability and mobility.

### Key Concepts
- **EID (Endpoint Identifier)**: IP address of endpoint
- **RLOC (Routing Locator)**: IP address of LISP router
- **Map Server/Resolver**: Central database for EID-to-RLOC mappings
- **ITR (Ingress Tunnel Router)**: Encapsulates packets
- **ETR (Egress Tunnel Router)**: Decapsulates packets
- **xTR**: Functions as both ITR and ETR

### Benefits
- Improved routing table scalability
- Better mobility support
- Traffic engineering capabilities
- Multi-homing support

### Use Cases
- Data center interconnect
- VM mobility
- IoT networks
- Network virtualization

---

## MPLS (Multiprotocol Label Switching) {#mpls}

### Overview
MPLS is a routing technique that directs data using short path labels instead of network addresses, improving speed and scalability.

### Key Components
- **Label**: 32-bit identifier (20-bit label, 3-bit EXP, 1-bit S, 8-bit TTL)
- **LSR (Label Switch Router)**: Forwards based on labels
- **LER (Label Edge Router)**: Adds/removes labels at network edge
- **LSP (Label Switched Path)**: Path through network
- **FEC (Forwarding Equivalence Class)**: Group of packets with same treatment

### MPLS Operations
1. **Push**: Add label (ingress)
2. **Swap**: Exchange label (transit)
3. **Pop**: Remove label (egress)

### Label Distribution Protocols
- **LDP (Label Distribution Protocol)**: Standard protocol
- **RSVP-TE**: For traffic engineering
- **MP-BGP**: For MPLS VPNs

### MPLS VPN
**L3 VPN (MPLS VPN)**:
- **VRF**: Virtual routing and forwarding
- **RD (Route Distinguisher)**: Makes routes unique
- **RT (Route Target)**: Controls route import/export
- **MP-BGP**: Exchanges VPN routes

**L2 VPN**:
- **VPLS (Virtual Private LAN Service)**
- **Pseudowires**
- **VPWS (Virtual Private Wire Service)**

### Configuration Example (Basic MPLS)
```
! Enable CEF
ip cef

! Configure MPLS on interfaces
interface GigabitEthernet0/0
 mpls ip

! Configure LDP router ID
mpls ldp router-id Loopback0 force
```

### Benefits
- Traffic engineering
- Fast reroute
- VPN services
- QoS support
- Simplified routing

---

## Security Technologies

## ASA (Adaptive Security Appliance) {#asa}

### Overview
Cisco ASA is a security device combining firewall, VPN, IPS, and other security services.

### Key Features
- Stateful packet inspection
- Application inspection
- VPN support (SSL and IPSec)
- IPS/IDS capabilities
- High availability (Active/Standby, Active/Active)

### Security Levels
- **0-100**: Higher = more trusted
- **Inside**: 100 (most trusted)
- **Outside**: 0 (least trusted)
- **DMZ**: 50 (middle)

### Traffic Rules
- Higher to lower security: Allowed by default
- Lower to higher security: Denied by default (requires ACL)
- Same security level: Denied by default

### Basic Configuration
```
! Configure interfaces
interface GigabitEthernet0/0
 nameif outside
 security-level 0
 ip address 203.0.113.1 255.255.255.0

interface GigabitEthernet0/1
 nameif inside
 security-level 100
 ip address 192.168.1.1 255.255.255.0

! Configure NAT
object network INSIDE_NET
 subnet 192.168.1.0 255.255.255.0
 nat (inside,outside) dynamic interface

! Configure ACL
access-list OUTSIDE_IN extended permit tcp any host 192.168.1.10 eq 443
access-group OUTSIDE_IN in interface outside

! Configure default route
route outside 0.0.0.0 0.0.0.0 203.0.113.254
```

### ASA Packet Flow
1. Decapsulation
2. NAT (if configured)
3. Security policy check
4. State check
5. NAT (outbound)
6. Encapsulation
7. Forwarding

---

## IPSec {#ipsec}

### Overview
IPSec (Internet Protocol Security) is a framework of protocols for securing IP communications through encryption and authentication.

### IPSec Protocols
- **AH (Authentication Header)**: Authentication only (IP protocol 51)
- **ESP (Encapsulating Security Payload)**: Encryption and authentication (IP protocol 50)

### IPSec Modes
- **Transport Mode**: Encrypts only payload (for host-to-host)
- **Tunnel Mode**: Encrypts entire packet (for site-to-site)

### IPSec Components

#### IKE (Internet Key Exchange)
**IKEv1 Phases**:
- **Phase 1**: Establish secure channel (ISAKMP SA)
  - Main Mode (6 messages)
  - Aggressive Mode (3 messages)
- **Phase 2**: Negotiate IPSec parameters (IPSec SA)
  - Quick Mode

**IKEv2**: Simplified, fewer exchanges (4 messages)

### IPSec Configuration Steps
1. **Configure ISAKMP Policy (Phase 1)**
2. **Configure IPSec Transform Set**
3. **Define Interesting Traffic (ACL)**
4. **Create Crypto Map**
5. **Apply to Interface**

### Site-to-Site VPN Configuration
```
! Phase 1 - ISAKMP Policy
crypto isakmp policy 10
 encryption aes 256
 hash sha256
 authentication pre-share
 group 14
 lifetime 86400

crypto isakmp key MySecretKey address 203.0.113.2

! Phase 2 - Transform Set
crypto ipsec transform-set MY_SET esp-aes 256 esp-sha256-hmac
 mode tunnel

! Interesting Traffic
access-list 100 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255

! Crypto Map
crypto map MY_MAP 10 ipsec-isakmp
 set peer 203.0.113.2
 set transform-set MY_SET
 match address 100

! Apply to Interface
interface GigabitEthernet0/1
 crypto map MY_MAP
```

### IPSec Security Associations
- **ISAKMP SA**: Bidirectional (one for both directions)
- **IPSec SA**: Unidirectional (two required)

### Verification Commands
```
show crypto isakmp sa
show crypto ipsec sa
show crypto session
debug crypto isakmp
debug crypto ipsec
```

---

## VPN (Virtual Private Network) {#vpn}

### Overview
VPN creates secure connections over public networks by encrypting traffic between endpoints.

### VPN Types

#### 1. Site-to-Site VPN
- Connects entire networks
- Always-on connection
- Uses IPSec or GRE over IPSec
- Router-to-router or firewall-to-firewall

#### 2. Remote Access VPN
- Individual users connect to network
- On-demand connection
- Technologies:
  - **SSL VPN (WebVPN)**: Browser-based
  - **IPSec VPN**: Client-based
  - **AnyConnect**: Cisco's modern client

### SSL VPN vs IPSec VPN
| Feature | SSL VPN | IPSec VPN |
|---------|---------|-----------|
| Protocol | SSL/TLS (TCP 443) | IPSec (ESP/AH) |
| Client | Browser or lightweight client | Dedicated client |
| Access | Typically application-level | Full network access |
| Firewall Friendly | Yes (uses port 443) | Sometimes blocked |
| Security | Strong | Very strong |

### VPN Technologies

#### DMVPN (Dynamic Multipoint VPN)
- Hub-and-spoke with dynamic spoke-to-spoke
- Uses NHRP (Next Hop Resolution Protocol)
- Phases: 1, 2, 3

**DMVPN Configuration**
```
! Hub Router
interface Tunnel0
 ip address 10.0.0.1 255.255.255.0
 tunnel source GigabitEthernet0/0
 tunnel mode gre multipoint
 ip nhrp network-id 1
 ip nhrp map multicast dynamic
 tunnel key 12345

! Spoke Router
interface Tunnel0
 ip address 10.0.0.2 255.255.255.0
 tunnel source GigabitEthernet0/0
 tunnel mode gre multipoint
 tunnel destination 203.0.113.1
 ip nhrp network-id 1
 ip nhrp nhs 10.0.0.1
 ip nhrp map 10.0.0.1 203.0.113.1
 ip nhrp map multicast 203.0.113.1
 tunnel key 12345
```

#### FlexVPN
- Modern, standards-based VPN
- Uses IKEv2
- Flexible deployment models

#### GET VPN (Group Encrypted Transport VPN)
- For trusted networks (MPLS)
- No encapsulation overhead
- Centralized key management

---

## GRE (Generic Routing Encapsulation) {#gre}

### Overview
GRE is a tunneling protocol that encapsulates a wide variety of network layer protocols inside virtual point-to-point links.

### Key Features
- **Protocol**: IP protocol 47
- **Overhead**: 24 bytes (20 IP + 4 GRE)
- **Multiprotocol Support**: Can tunnel any Layer 3 protocol
- **No Encryption**: Not secure by itself

### GRE Tunnel Types
- **Point-to-Point**: Simple GRE tunnel
- **Multipoint (mGRE)**: Used in DMVPN

### Point-to-Point GRE Configuration
```
! Router 1
interface Tunnel0
 ip address 10.0.0.1 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination 203.0.113.2

! Router 2
interface Tunnel0
 ip address 10.0.0.2 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination 203.0.113.1
```

### GRE over IPSec
Combines GRE's multiprotocol support with IPSec's security.

```
! After configuring GRE tunnel, add IPSec
crypto ipsec profile PROTECT_GRE
 set transform-set MY_SET

interface Tunnel0
 tunnel protection ipsec profile PROTECT_GRE
```

### Use Cases
- Connect non-contiguous networks
- Support multicast traffic over VPN
- Tunnel routing protocols
- Encapsulate non-IP protocols

### Limitations
- No built-in encryption
- No error handling
- Can be filtered by firewalls
- Recursive routing issues (tunnel destination via tunnel)

---

## Access Control

## Access-List (ACL) {#access-list-acl}

### Overview
ACLs are packet filters that control traffic flow based on defined criteria such as source/destination IP, protocol, and port.

### ACL Types

#### Standard ACL (1-99, 1300-1999)
- Filters based on source IP only
- Applied close to destination

```
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 deny any

! Apply to interface
interface GigabitEthernet0/0
 ip access-group 10 in
```

#### Extended ACL (100-199, 2000-2699)
- Filters based on source, destination, protocol, port
- Applied close to source

```
access-list 100 permit tcp 192.168.1.0 0.0.0.255 any eq 80
access-list 100 permit tcp 192.168.1.0 0.0.0.255 any eq 443
access-list 100 deny ip any any

! Apply to interface
interface GigabitEthernet0/0
 ip access-group 100 in
```

#### Named ACL
More flexible and easier to manage.

```
ip access-list extended WEB_FILTER
 permit tcp 192.168.1.0 0.0.0.255 any eq 80
 permit tcp 192.168.1.0 0.0.0.255 any eq 443
 deny ip any any log

interface GigabitEthernet0/0
 ip access-group WEB_FILTER in
```

### ACL Processing Rules
1. **Top-down processing**: Matches first entry that fits
2. **Implicit deny**: Denies everything not explicitly permitted
3. **One ACL per interface per direction**: In/Out
4. **New entries**: Added to the end (unless using sequence numbers)

### Wildcard Masks
- **0**: Must match exactly
- **255**: Don't care
- Examples:
  - `0.0.0.0` = exact match
  - `0.0.0.255` = /24 network
  - `0.0.255.255` = /16 network

### Advanced ACL Features

#### Reflexive ACL
Creates temporary entries for return traffic.
```
ip access-list extended OUTBOUND
 permit tcp any any reflect TCP_REFLECT
 permit udp any any reflect UDP_REFLECT

ip access-list extended INBOUND
 evaluate TCP_REFLECT
 evaluate UDP_REFLECT
```

#### Time-Based ACL
```
time-range BUSINESS_HOURS
 periodic weekdays 8:00 to 18:00

ip access-list extended TIME_FILTER
 permit tcp any any eq 80 time-range BUSINESS_HOURS
```

#### Object Groups
Simplify complex ACLs.
```
object-group network SERVERS
 host 192.168.1.10
 host 192.168.1.11
 host 192.168.1.12

object-group service WEB
 tcp eq 80
 tcp eq 443

ip access-list extended SERVER_ACCESS
 permit object-group WEB any object-group SERVERS
```

### Verification Commands
```
show access-lists
show ip access-lists
show ip interface GigabitEthernet0/0
clear access-list counters
```

### Best Practices
- Place most specific rules first
- Use named ACLs for better management
- Document ACL purpose
- Use sequence numbers for easier editing
- Review and audit regularly
- Log denied traffic for security monitoring

---

## Protocol Differences

## TCP vs UDP {#tcp-vs-udp}

### Overview
TCP and UDP are transport layer protocols with different characteristics and use cases.

### TCP (Transmission Control Protocol)

#### Characteristics
- **Connection-oriented**: Three-way handshake (SYN, SYN-ACK, ACK)
- **Reliable**: Guarantees delivery with acknowledgments
- **Ordered**: Maintains sequence of packets
- **Flow Control**: Windowing mechanism
- **Error Checking**: Checksum and retransmission
- **Congestion Control**: Adjusts sending rate
- **Overhead**: Higher (20-60 byte header)

#### TCP Header
- Source Port (16 bits)
- Destination Port (16 bits)
- Sequence Number (32 bits)
- Acknowledgment Number (32 bits)
- Flags: SYN, ACK, FIN, RST, PSH, URG
- Window Size (16 bits)
- Checksum (16 bits)
- Options (variable)

#### TCP Three-Way Handshake
1. **SYN**: Client sends SYN with initial sequence number
2. **SYN-ACK**: Server responds with SYN-ACK
3. **ACK**: Client sends ACK to complete connection

#### TCP Connection Termination
1. **FIN**: Initiator sends FIN
2. **ACK**: Receiver acknowledges FIN
3. **FIN**: Receiver sends FIN
4. **ACK**: Initiator acknowledges FIN

#### TCP Use Cases
- Web browsing (HTTP/HTTPS)
- Email (SMTP, POP3, IMAP)
- File transfer (FTP, SFTP)
- Remote access (SSH, Telnet)
- Database connections
- Any application requiring reliability

### UDP (User Datagram Protocol)

#### Characteristics
- **Connectionless**: No handshake or connection setup
- **Unreliable**: No delivery guarantees
- **Unordered**: Packets may arrive out of order
- **No Flow Control**: Sender transmits at full speed
- **Minimal Error Checking**: Basic checksum only
- **Low Overhead**: 8 byte header
- **Fast**: Less processing required

#### UDP Header
- Source Port (16 bits)
- Destination Port (16 bits)
- Length (16 bits)
- Checksum (16 bits)

#### UDP Use Cases
- Streaming media (video, audio)
- VoIP (Voice over IP)
- Online gaming
- DNS queries
- DHCP
- SNMP
- TFTP
- Real-time applications
- Broadcast/multicast applications

### TCP vs UDP Comparison Table

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Reliable | Unreliable |
| Ordering | Ordered | Unordered |
| Speed | Slower | Faster |
| Overhead | Higher | Lower |
| Header Size | 20-60 bytes | 8 bytes |
| Use Case | Accuracy important | Speed important |
| Flow Control | Yes | No |
| Congestion Control | Yes | No |
| Retransmission | Yes | No |
| Broadcasting | No | Yes |

### Common Port Numbers

#### TCP Ports
- **20/21**: FTP (Data/Control)
- **22**: SSH
- **23**: Telnet
- **25**: SMTP
- **80**: HTTP
- **110**: POP3
- **143**: IMAP
- **443**: HTTPS
- **3389**: RDP

#### UDP Ports
- **53**: DNS
- **67/68**: DHCP (Server/Client)
- **69**: TFTP
- **123**: NTP
- **161/162**: SNMP (Agent/Manager)
- **514**: Syslog

#### Both TCP and UDP
- **53**: DNS (TCP for zone transfers, UDP for queries)

### When to Choose TCP vs UDP

**Choose TCP when:**
- Data integrity is critical
- Order matters
- Delivery confirmation needed
- Example: Financial transactions, file downloads

**Choose UDP when:**
- Speed is critical
- Some packet loss acceptable
- Low latency required
- Example: Live streaming, gaming, VoIP

---

## HTTPS Communication Between Workstation and Server {#https-communication}

### Overview
HTTPS (HTTP Secure) provides secure communication over networks using encryption via TLS/SSL protocol.

### HTTPS Connection Process

#### 1. DNS Resolution
- Client resolves domain name to IP address
- DNS query (typically UDP port 53)

#### 2. TCP Three-Way Handshake
- Client sends SYN to server (port 443)
- Server responds with SYN-ACK
- Client sends ACK
- TCP connection established

#### 3. TLS Handshake (TLS 1.2)

**Step 1: Client Hello**
- Client sends supported TLS versions
- Supported cipher suites
- Random number (Client Random)
- Supported compression methods
- Extensions (SNI, etc.)

**Step 2: Server Hello**
- Server selects TLS version
- Selects cipher suite
- Random number (Server Random)
- Session ID

**Step 3: Server Certificate**
- Server sends X.509 certificate
- Contains public key
- Signed by Certificate Authority (CA)

**Step 4: Server Key Exchange (if needed)**
- For certain cipher suites (DHE, ECDHE)
- Server sends additional key exchange parameters

**Step 5: Certificate Request (optional)**
- Server requests client certificate
- For mutual TLS authentication

**Step 6: Server Hello Done**
- Server indicates completion of hello phase

**Step 7: Client Key Exchange**
- Client generates pre-master secret
- Encrypts with server's public key
- Sends to server

**Step 8: Client Certificate (if requested)**
- Client sends its certificate

**Step 9: Certificate Verify (if applicable)**
- Client proves it owns private key

**Step 10: Change Cipher Spec (Client)**
- Client notifies server to start encryption

**Step 11: Finished (Client)**
- Encrypted message verifying handshake

**Step 12: Change Cipher Spec (Server)**
- Server notifies client to start encryption

**Step 13: Finished (Server)**
- Encrypted message verifying handshake

#### 4. Encrypted Application Data
- HTTP requests/responses encrypted
- Uses symmetric encryption (AES, ChaCha20)
- Session keys derived from pre-master secret

#### 5. Connection Closure
- Either party sends TLS close_notify alert
- TCP connection terminates (FIN, ACK, FIN, ACK)

### TLS 1.3 Improvements
- Faster handshake (1-RTT or 0-RTT)
- Removed weak cipher suites
- Always uses perfect forward secrecy
- Encrypted more of the handshake

### TLS 1.3 Handshake (Simplified)
1. **Client Hello**: Includes key share
2. **Server Hello**: Selects parameters, sends key share
3. **Encrypted Extensions**: Server certificate and finish
4. **Client Finish**: Client confirmation
5. **Application Data**: Encrypted communication

### Certificate Validation
1. **Chain of Trust**: Certificate signed by trusted CA
2. **Validity Period**: Not expired
3. **Domain Match**: Certificate matches requested domain
4. **Revocation Check**: CRL or OCSP

### Cipher Suite Components
Format: `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`
- **Key Exchange**: ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)
- **Authentication**: RSA
- **Encryption**: AES-256-GCM
- **MAC/Hash**: SHA-384

### Common Cipher Suites
- `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`
- `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`
- `TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256`
- `TLS_AES_256_GCM_SHA384` (TLS 1.3)
- `TLS_AES_128_GCM_SHA256` (TLS 1.3)

### Perfect Forward Secrecy (PFS)
- Each session uses unique session keys
- Compromising long-term keys doesn't expose past sessions
- Achieved with ephemeral key exchange (DHE, ECDHE)

### HTTP/2 over HTTPS
- Binary protocol (vs. text in HTTP/1.1)
- Multiplexing: Multiple requests over single connection
- Header compression (HPACK)
- Server push capability
- Requires TLS 1.2+

### HTTPS Port
- **Default**: 443
- Can use any port, but 443 is standard

### Example HTTPS Request Flow
```
1. User types: https://www.example.com
2. DNS lookup: www.example.com → 93.184.216.34
3. TCP handshake to 93.184.216.34:443
4. TLS handshake (establish encryption)
5. Encrypted HTTP request:
   GET / HTTP/1.1
   Host: www.example.com
6. Encrypted HTTP response:
   HTTP/1.1 200 OK
   Content-Type: text/html
   [HTML content]
7. Page rendered in browser
8. Connection kept alive or closed
```

### Security Benefits
- **Confidentiality**: Encryption prevents eavesdropping
- **Integrity**: Detects tampering
- **Authentication**: Verifies server identity
- **Compliance**: Required for sensitive data (PCI-DSS, HIPAA)

### Tools for Analysis
- **Wireshark**: Packet capture and analysis
- **OpenSSL**: Testing TLS connections
- **Browser DevTools**: Inspect HTTPS connections
- **SSL Labs**: Test server configuration

### Common Issues
- **Certificate errors**: Expired, self-signed, domain mismatch
- **Mixed content**: HTTP resources on HTTPS page
- **Protocol version**: Old TLS versions disabled
- **Weak ciphers**: Insecure algorithms removed

---

## Security Concepts {#security-concepts}

### Defense in Depth
Multiple layers of security controls:
1. **Perimeter Security**: Firewalls, IPS
2. **Network Segmentation**: VLANs, ACLs
3. **Access Control**: Authentication, authorization
4. **Endpoint Security**: Antivirus, host firewall
5. **Application Security**: Input validation, secure coding
6. **Data Security**: Encryption, DLP
7. **Monitoring**: Logging, SIEM

### CIA Triad
- **Confidentiality**: Protect information from unauthorized access
- **Integrity**: Ensure data accuracy and completeness
- **Availability**: Ensure authorized users have access when needed

### AAA Framework
- **Authentication**: Verify identity (who are you?)
- **Authorization**: Grant permissions (what can you do?)
- **Accounting**: Track activities (what did you do?)

### Network Security Zones
- **Trusted**: Internal network
- **Untrusted**: Internet
- **DMZ**: Semi-trusted (public-facing services)

### Security Policies
- **Blacklist**: Block known bad (default allow)
- **Whitelist**: Allow known good (default deny)
- **Zero Trust**: Never trust, always verify

### Threat Types
- **Malware**: Viruses, worms, trojans, ransomware
- **Social Engineering**: Phishing, pretexting
- **DoS/DDoS**: Denial of service attacks
- **Man-in-the-Middle**: Intercept communications
- **SQL Injection**: Database attacks
- **XSS**: Cross-site scripting

### Security Best Practices
1. Principle of Least Privilege
2. Defense in Depth
3. Regular patching and updates
4. Strong authentication (MFA)
5. Encryption (data at rest and in transit)
6. Logging and monitoring
7. Incident response plan
8. Security awareness training
9. Regular security audits
10. Backup and disaster recovery

---

## Layer 2 Security {#layer-2-security}

### Layer 2 Threats

#### 1. MAC Flooding
- **Attack**: Overflow CAM table
- **Result**: Switch acts as hub (broadcasts all traffic)
- **Mitigation**: Port security

#### 2. MAC Spoofing
- **Attack**: Impersonate another device's MAC
- **Result**: Intercept traffic intended for victim
- **Mitigation**: Port security, DHCP snooping

#### 3. DHCP Spoofing
- **Attack**: Rogue DHCP server
- **Result**: Man-in-the-middle, wrong gateway
- **Mitigation**: DHCP snooping

#### 4. ARP Spoofing/Poisoning
- **Attack**: Send fake ARP responses
- **Result**: Man-in-the-middle attack
- **Mitigation**: Dynamic ARP Inspection (DAI)

#### 5. VLAN Hopping
**Switch Spoofing**:
- Attack: Trunk negotiation (DTP)
- Mitigation: Disable DTP, manually configure trunks

**Double Tagging**:
- Attack: Two VLAN tags
- Mitigation: Don't use native VLAN, prune unused VLANs

#### 6. STP Manipulation
- **Attack**: Become root bridge
- **Result**: Traffic redirection, DoS
- **Mitigation**: Root guard, BPDU guard

#### 7. CDP/LLDP Reconnaissance
- **Attack**: Gather network information
- **Result**: Information disclosure
- **Mitigation**: Disable on untrusted ports

### Layer 2 Security Features

#### Port Security
See dedicated section below.

#### DHCP Snooping
See dedicated section below.

#### Dynamic ARP Inspection (DAI)
```
ip dhcp snooping
ip arp inspection vlan 10,20

! Trust uplinks
interface GigabitEthernet0/1
 ip arp inspection trust

! Rate limit untrusted ports
interface range GigabitEthernet0/2-24
 ip arp inspection limit rate 15
```

#### IP Source Guard
Prevents IP spoofing.
```
ip dhcp snooping
interface GigabitEthernet0/2
 ip verify source
```

#### Storm Control
Prevents broadcast storms.
```
interface GigabitEthernet0/2
 storm-control broadcast level 50.00
 storm-control multicast level 50.00
 storm-control action shutdown
```

#### BPDU Guard
Shuts down port if BPDU received (prevents STP attacks).
```
spanning-tree portfast bpduguard default

! Or per interface
interface GigabitEthernet0/2
 spanning-tree bpduguard enable
```

#### Root Guard
Prevents unauthorized switch from becoming root.
```
interface GigabitEthernet0/1
 spanning-tree guard root
```

#### Best Practices
1. Enable port security on access ports
2. Configure DHCP snooping
3. Enable DAI on VLANs
4. Disable unused ports
5. Manually configure trunks (disable DTP)
6. Change native VLAN
7. Prune unused VLANs from trunks
8. Enable BPDU Guard on access ports
9. Disable CDP/LLDP on untrusted ports
10. Implement 802.1X for authentication

---

## Port-Security {#port-security}

### Overview
Port security restricts which devices can connect to switch ports based on MAC addresses.

### Port Security Modes

#### 1. Static Secure MAC
Manually configured, saved in running/startup config.

#### 2. Dynamic Secure MAC
Learned dynamically, removed on switch reload.

#### 3. Sticky Secure MAC
Learned dynamically but saved to config.

### Violation Actions

#### 1. Protect
- Drops packets from violating MAC
- No notification
- Port stays up

#### 2. Restrict
- Drops packets from violating MAC
- Logs violation
- Sends SNMP trap
- Port stays up

#### 3. Shutdown (Default)
- Port enters err-disabled state
- Logs violation
- Sends SNMP trap
- Requires manual intervention

### Configuration Examples

#### Basic Port Security
```
interface GigabitEthernet0/2
 switchport mode access
 switchport access vlan 10
 switchport port-security
 switchport port-security maximum 1
 switchport port-security violation shutdown
```

#### Sticky MAC Learning
```
interface GigabitEthernet0/2
 switchport mode access
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation restrict
```

#### Static MAC Address
```
interface GigabitEthernet0/2
 switchport mode access
 switchport port-security
 switchport port-security mac-address 0011.2233.4455
```

### Recovery from Err-Disabled

#### Manual Recovery
```
interface GigabitEthernet0/2
 shutdown
 no shutdown
```

#### Automatic Recovery
```
errdisable recovery cause psecure-violation
errdisable recovery interval 300
```

### Verification Commands
```
show port-security
show port-security interface GigabitEthernet0/2
show port-security address
show errdisable recovery
```

### Best Practices
1. Enable on all access ports
2. Use sticky MAC for workstations
3. Set appropriate maximum (consider phones + PCs)
4. Use restrict or shutdown mode
5. Configure err-disable recovery
6. Document static MAC assignments
7. Regular audit of port security status

---

## DHCP Snooping {#dhcp-snooping}

### Overview
DHCP snooping is a security feature that validates DHCP messages and builds a binding database of legitimate DHCP assignments.

### How It Works
1. **Trusted vs Untrusted Ports**:
   - Trusted: Uplinks to legitimate DHCP servers
   - Untrusted: Access ports (clients)

2. **Validation**:
   - DHCP OFFER/ACK only from trusted ports
   - DHCP RELEASE/DECLINE match binding table
   - MAC address matches source MAC

3. **Binding Database**:
   - MAC address
   - IP address
   - VLAN
   - Interface
   - Lease time

### Configuration

#### Basic DHCP Snooping
```
! Enable globally
ip dhcp snooping

! Enable per VLAN
ip dhcp snooping vlan 10,20,30

! Trust uplinks (to DHCP server)
interface GigabitEthernet0/1
 ip dhcp snooping trust

! Optional: Rate limiting
interface range GigabitEthernet0/2-24
 ip dhcp snooping limit rate 10

! Optional: Insert option 82
ip dhcp snooping information option
```

#### With Option 82
```
! Enable Option 82 (relay agent information)
ip dhcp snooping information option

! Allow untrusted option 82
ip dhcp snooping information option allow-untrusted
```

### DHCP Message Types
- **DISCOVER**: Client broadcasts to find DHCP server
- **OFFER**: Server offers IP address
- **REQUEST**: Client requests offered IP
- **ACKNOWLEDGE**: Server confirms assignment
- **RELEASE**: Client releases IP
- **DECLINE**: Client declines IP (duplicate detected)
- **NAK**: Server denies request

### What DHCP Snooping Blocks
1. DHCP OFFER from untrusted ports (rogue DHCP servers)
2. DHCP ACK from untrusted ports
3. RELEASE/DECLINE from clients not in binding table
4. Packets with mismatched source MAC

### Verification Commands
```
show ip dhcp snooping
show ip dhcp snooping binding
show ip dhcp snooping database
debug ip dhcp snooping
```

### Dependencies
- **DAI**: Uses DHCP snooping binding table
- **IP Source Guard**: Uses DHCP snooping binding table

### Best Practices
1. Enable on all access VLANs
2. Trust only uplinks to DHCP servers
3. Configure rate limiting on access ports
4. Save binding database to external location
5. Monitor logs for violations
6. Test thoroughly before deployment
7. Document trusted ports

### Common Issues
1. **Legitimate server marked untrusted**: Trust correct ports
2. **High CPU**: Adjust rate limits
3. **Database not persistent**: Configure database location
4. **Option 82 issues**: Configure allow-untrusted if needed

---

## AAA, TACACS+, and RADIUS {#aaa-tacacs-radius}

### AAA Framework

#### Authentication
- **Verify identity**: Username/password, certificates, biometrics
- **Methods**: Local, RADIUS, TACACS+, Kerberos, LDAP

#### Authorization
- **Define permissions**: What user can do after authentication
- **Types**: Command authorization, network access, privilege levels

#### Accounting
- **Track activities**: Login/logout, commands executed
- **Purpose**: Auditing, compliance, billing

### TACACS+ vs RADIUS

| Feature | TACACS+ | RADIUS |
|---------|---------|--------|
| **Developer** | Cisco | IETF Standard |
| **TCP/UDP** | TCP (port 49) | UDP (1812 auth, 1813 acct) |
| **Encryption** | Full packet | Password only |
| **AAA** | Separates AAA | Combines auth/authz |
| **Protocol** | Binary | ASCII |
| **Flexibility** | More granular | Less granular |
| **Network/Admin** | Admin access | Network access |
| **Multiprotocol** | Yes | IP only |
| **Reliability** | TCP (more reliable) | UDP (faster) |

### TACACS+ Configuration

#### Router/Switch as Client
```
! Define AAA
aaa new-model

! Define TACACS+ server
tacacs-server host 192.168.1.100 key SecretKey123

! Authentication
aaa authentication login default group tacacs+ local
aaa authentication enable default group tacacs+ enable

! Authorization
aaa authorization exec default group tacacs+ local
aaa authorization commands 15 default group tacacs+ local

! Accounting
aaa accounting exec default start-stop group tacacs+
aaa accounting commands 15 default start-stop group tacacs+

! Console doesn't use AAA (fallback)
line console 0
 login authentication default

! VTY uses AAA
line vty 0 4
 login authentication default
 authorization exec default
```

### RADIUS Configuration

#### Router/Switch as Client
```
! Define AAA
aaa new-model

! Define RADIUS server
radius-server host 192.168.1.101 auth-port 1812 acct-port 1813 key SecretKey456

! Authentication
aaa authentication login default group radius local
aaa authentication dot1x default group radius

! Authorization
aaa authorization network default group radius

! Accounting
aaa accounting network default start-stop group radius
```

### 802.1X with RADIUS
```
! Enable AAA
aaa new-model

! RADIUS configuration
radius-server host 192.168.1.101 key SecretKey789

! Authentication, authorization, accounting
aaa authentication dot1x default group radius
aaa authorization network default group radius
aaa accounting dot1x default start-stop group radius

! Enable 802.1X globally
dot1x system-auth-control

! Configure interface
interface GigabitEthernet0/2
 switchport mode access
 switchport access vlan 10
 authentication port-control auto
 dot1x pae authenticator
```

### Common AAA Methods
- **local**: Use local username database
- **group radius**: Use RADIUS server(s)
- **group tacacs+**: Use TACACS+ server(s)
- **enable**: Use enable password
- **none**: No authentication
- **line**: Use line password

### Method Lists
```
! Named method list
aaa authentication login CONSOLE local
aaa authentication login VTY group tacacs+ local

! Apply to lines
line console 0
 login authentication CONSOLE

line vty 0 4
 login authentication VTY
```

### Local User Database
```
username admin privilege 15 secret Cisco123
username user1 privilege 1 secret UserPass1
username user2 privilege 5 secret UserPass2
```

### Privilege Levels
- **Level 0**: Predefined (logout, enable, disable, help)
- **Level 1**: User EXEC mode (default)
- **Levels 2-14**: Customizable
- **Level 15**: Privileged EXEC mode (full access)

### Command Authorization Example
```
! Define privilege level 5 commands
privilege exec level 5 show running-config
privilege exec level 5 configure terminal
privilege configure level 5 interface

! Create user at level 5
username netadmin privilege 5 secret NetPass5
```

### Verification Commands
```
show aaa servers
show tacacs
show radius server-group all
debug aaa authentication
debug aaa authorization
debug aaa accounting
debug radius
debug tacacs
```

### Best Practices
1. Always include "local" as fallback
2. Use strong shared secrets
3. Encrypt communications (tacacs-server key, radius-server key)
4. Use named method lists for flexibility
5. Test thoroughly before deployment
6. Monitor authentication failures
7. Implement redundant AAA servers
8. Document all configurations
9. Regular password rotation
10. Principle of least privilege

---

## Summary

This guide covers essential networking technologies and security concepts:

### Routing & Switching
- **VRF**: Virtual routing instances for traffic isolation
- **Routing Protocols**: OSPF, EIGRP, BGP, IS-IS, RIP with different use cases
- **FHRP**: HSRP, GLBP for gateway redundancy and load balancing

### Advanced Technologies
- **Multicast**: Efficient one-to-many communication
- **NAT**: Address translation for IPv4 conservation
- **LISP**: Locator/ID separation for improved routing
- **MPLS**: Label switching for service provider networks

### Security
- **ASA**: Comprehensive security appliance
- **IPSec/VPN**: Secure communications
- **GRE**: Tunneling protocol
- **ACLs**: Traffic filtering
- **Layer 2 Security**: Port security, DHCP snooping, DAI
- **AAA**: Authentication, authorization, accounting with TACACS+/RADIUS

### Key Takeaways
1. Choose routing protocols based on network size and requirements
2. Implement defense in depth with multiple security layers
3. Use encryption for sensitive communications (HTTPS, IPSec)
4. Enable Layer 2 security features to prevent common attacks
5. Implement proper AAA for administrative access control
6. Regular monitoring and auditing are essential
7. Document all configurations and changes
8. Test security controls in lab before production deployment

---

**End of Network Technologies and Protocols Guide**
