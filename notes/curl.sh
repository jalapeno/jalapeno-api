#! /bin/bash

curl http://198.18.133.104:30800/api/v1/collections
curl http://198.18.133.104:30800/api/v1/collections/igpv4_graph
curl http://198.18.133.104:30800/api/v1/collections/igpv6_graph
curl http://198.18.133.104:30800/api    
curl http://198.18.133.104:30800/api/v1/collections/ipv6_graph

curl http://198.18.133.104:30800/api/v1/collections/ipv6_graph/edges
curl http://198.18.133.104:30800/api/v1/collections/ipv4_graph/edges
curl http://198.18.133.104:30800/api/v1/collections/igpv6_graph/edges
curl http://198.18.133.104:30800/api/v1/collections/igpv4_graph/edges


curl http://198.18.133.104:30800/api/v1/collections/ipv6_graph/vertices
curl http://198.18.133.104:30800/api/v1/collections/ipv4_graph/vertices
curl http://198.18.133.104:30800/api/v1/collections/igpv6_graph/vertices
curl http://198.18.133.104:30800/api/v1/collections/igpv4_graph/vertices


curl "http://198.18.133.104:30800/api/v1/collections/ls_node"
curl "http://198.18.133.104:30800/api/v1/collections/ls_link"
curl "http://198.18.133.104:30800/api/v1/collections/ls_prefix"
curl "http://198.18.133.104:30800/api/v1/collections/ls_srv6_sid"


curl "http://198.18.133.104:30800/api/v1/collections/bgp_node"
curl "http://198.18.133.104:30800/api/v1/collections/igp_node"
curl "http://198.18.133.104:30800/api/v1/collections/ebgp_prefix_v4"
curl "http://198.18.133.104:30800/api/v1/collections/ebgp_prefix_v6"

curl "http://198.18.133.104:30800/api/v1/collections/peer/keys"
curl "http://198.18.133.104:30800/api/v1/collections/bgp_node/search?asn=65001"

# shortest path
curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path?source=ebgp_prefix_v6/fc00:0:f800:1::_64&destination=ebgp_prefix_v6/fc00:0:f800:800d::_64"
curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path?source=ebgp_prefix_v6/fc00:0:f800:1::_64&destination=ebgp_prefix_v6/fc00:0:f800:800d::_64&direction=any"
curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path?source=ebgp_prefix_v6/fc00:0:f800:1::_64&destination=ebgp_prefix_v6/fc00:0:f800:800d::_64&direction=outbound"
curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path?source=ebgp_prefix_v6/fc00:0:f800:1::_64&destination=ebgp_prefix_v6/fc00:0:f800:800d::_64&direction=inbound"

curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path?source=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&destination=ls_prefix/2_0_2_0_0_fc00:0:701:1003::_64_0000.0002.0067&direction=any"

curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/traverse/simple?source=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&destination=igp_node/2_0_0_0000.0002.0067"
curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/traverse/simple?start_node=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&target_node=ls_prefix/2_0_2_0_0_fc00:0:701:1003::_64_0000.0002.0067&max_depth=6"

curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/traverse/simple?source=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&max_depth=5"


#### Get neighbors
curl "http://198.18.133.112:30800/api/v1/graphs/ipv6_graph/neighbors?source=igp_node/2_0_0_0000.0000.0001"

#### Get neighbors with greater depth
curl "http://198.18.133.112:30800/api/v1/graphs/ipv6_graph/neighbors?source=igp_node/2_0_0_0000.0000.0001&depth=2"

#### Basic usage
curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/vertices/summary

#### With limit
curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/vertices/summary?limit=25


curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/vertices/summary
curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/vertices/summary?vertex_collection=igp_node 
curl http://198.18.133.112:30800/api/v1/graphs/ipv6_graph/vertices/summary?vertex_collection=igp_node&limit=10


# Get all collections

curl http://198.18.133.104:30800/api/v1/collections

# Get only graph collections
curl http://198.18.133.104:30800/api/v1/collections?filter_graphs=true

# Get only non-graph collections
curl http://198.18.133.104:30800/api/v1/collections?filter_graphs=false

curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/topology
curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/topology | jq 
curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/topology?limit=50

# Get all node-to-node connections
curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/topology/nodes

# latency weighted shortest path
curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path/latency?source=gpus/host08-gpu02&destination=gpus/host12-gpu02"

curl "http://198.18.133.104:30800/api/v1/collections/ipv6_graph/shortest_path/latency?source=gpus/host08-gpu02&destination=gpus/host12-gpu02&direction=outbound"

curl "http://198.18.133.111:30800/api/v1/graphs/ipv6_graph/shortest_path/utilization?source=gpus/host08-gpu02&destination=gpus/host12-gpu02&direction=outbound"

curl "http://198.18.133.111:30800/api/v1/graphs/ipv6_graph/shortest_path/utilization?source=gpus/host08-gpu02&destination=gpus/host12-gpu02&direction=inbound"


# shortest path with country exclusion
curl -X GET "http://198.18.128.101:30800/api/v1/graphs/ipv6_graph/shortest_path/sovereignty?source=hosts/berlin-k8s&destination=hosts/rome&excluded_countries=FRA&direction=outbound" | jq .


# load
curl "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path/load?source=gpus/host01-gpu02&destination=gpus/host12-gpu02&direction=any"


# best path
curl -X GET "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path/best-paths?source=hosts/amsterdam&destination=hosts/rome&direction=outbound" | jq .

curl -X GET "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path/best-paths?source=hosts/amsterdam&destination=hosts/rome&direction=outbound&limit=6" | jq .

# next best path
curl -X GET "http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/shortest_path/next-best-path?source=hosts/berlin-k8s&destination=hosts/rome&direction=outbound"



