## Base queries

#### Get all collections
curl http://localhost:8000/api/v1/collections

## Graphs
#### Get specific graph data
curl http://localhost:8000/api/v1/collections/igpv4_graph
curl http://localhost:8000/api/v1/collections/igpv6_graph
curl http://localhost:8000/api/v1/collections/ipv4_graph
curl http://localhost:8000/api/v1/collections/ipv6_graph

#### Get graph info
curl http://localhost:8000/api/v1/collections/igpv4_graph/info
curl http://localhost:8000/api/v1/collections/igpv6_graph/info

#### Get just the edge connections for a graph
curl http://localhost:8000/api/v1/collections/ipv6_graph/edges
curl http://localhost:8000/api/v1/collections/ipv4_graph/edges
curl http://localhost:8000/api/v1/collections/igpv6_graph/edges
curl http://localhost:8000/api/v1/collections/igpv4_graph/edges

#### Get just the vertices for a graph
curl http://localhost:8000/api/v1/collections/ipv6_graph/vertices
curl http://localhost:8000/api/v1/collections/ipv4_graph/vertices
curl http://localhost:8000/api/v1/collections/igpv6_graph/vertices
curl http://localhost:8000/api/v1/collections/igpv4_graph/vertices

#### Get vertex keys
curl http://localhost:8000/api/v1/collections/ipv6_graph/vertices/keys
curl http://localhost:8000/api/v1/collections/ipv4_graph/vertices/keys

#### Get vertex ids
curl http://localhost:8000/api/v1/collections/ipv6_graph/vertices/ids
curl http://localhost:8000/api/v1/collections/ipv4_graph/vertices/ids

## Collections

#### Get data from any collection
curl "http://localhost:8000/api/v1/collection/ls_node"
curl "http://localhost:8000/api/v1/collection/ls_link"
curl "http://localhost:8000/api/v1/collection/ls_prefix"
curl "http://localhost:8000/api/v1/collection/ls_srv6_sid"

curl "http://localhost:8000/api/v1/collection/bgp_node"
curl "http://localhost:8000/api/v1/collection/igp_node"
curl "http://localhost:8000/api/v1/collection/ebgp_prefix_v4"
curl "http://localhost:8000/api/v1/collection/ebgp_prefix_v6"

#### Get data with limits
curl "http://localhost:8000/api/v1/collection/bgp_node?limit=10"
curl "http://localhost:8000/api/v1/collection/igp_node?limit=10"

#### Get data with a specific key
curl "http://localhost:8000/api/v1/collection/bgp_node?filter_key=some_key"

#### Get just the keys from a collection
curl "http://localhost:8000/api/v1/collection/peer/keys"


## Search

#### Search by ASN only
curl "http://localhost:8000/api/v1/collection/ls_node_extended/search?asn=65001"

#### Search by protocol only
curl "http://localhost:8000/api/v1/collection/ls_node_extended/search?protocol=IS-IS%20Level%202"

#### Search with multiple filters
curl "http://localhost:8000/api/v1/collection/ls_node_extended/search?asn=65001&srv6_enabled=true"

## Graphs

#### Find shortest path
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path?from_node=ls_node_extended/2_0_0_0000.0001.0065&to_node=ls_node_extended/2_0_0_0000.0002.0067"

#### For outbound (default)
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path?source=ls_node_extended/2_0_0_0000.0001.0065&destination=ls_node_extended/2_0_0_0000.0002.0067"

#### For inbound
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path?source=ls_node_extended/2_0_0_0000.0001.0065&destination=ls_node_extended/2_0_0_0000.0002.0067&direction=inbound"

#### For any direction
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path?source=ls_node_extended/2_0_0_0000.0001.0065&destination=ls_node_extended/2_0_0_0000.0002.0067&direction=any"

curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path?source=ls_node_extended/2_0_0_0000.0001.0065&destination=ls_node_extended/2_0_0_0000.0002.0067"

#### prefix to prefix
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path?source=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&destination=ls_prefix/2_0_2_0_0_fc00:0:701:1003::_64_0000.0002.0067&direction=any"



#### simple traverse graph
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/traverse/simple?source=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&destination=ls_node_extended/2_0_0_0000.0002.0067"

curl "http://localhost:8000/api/v1/graphs/ipv6_graph/traverse/simple?start_node=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&target_node=ls_prefix/2_0_2_0_0_fc00:0:701:1003::_64_0000.0002.0067&max_depth=6"

curl "http://localhost:8000/api/v1/graphs/ipv6_graph/traverse/simple?source=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&max_depth=5"



#### Complex traverse graph

curl "http://localhost:8000/api/v1/graphs/ipv6_graph/traverse?source=ls_node_extended/2_0_0_0000.0001.0065&max_depth=3"


curl "http://localhost:8000/api/v1/graphs/ipv6_graph/traverse?source=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&destination=ls_node_extended/2_0_0_0000.0002.0067&max_depth=5&direction=any"



#### Get neighbors
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/neighbors?node=ls_node_extended/2_0_0_0000.0001.0001"

#### Get immediate neighbors
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/neighbors?source=ls_node_extended/2_0_0_0000.0001.0065"

#### Get neighbors with specific direction
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/neighbors?source=ls_node_extended/2_0_0_0000.0001.0065&direction=any"

#### Get neighbors with greater depth
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/neighbors?source=ls_node_extended/2_0_0_0000.0001.0065&depth=2"


### Graph summary
#### Basic usage
curl http://localhost:8000/api/v1/graphs/ipv6_graph/vertices/summary

#### With limit
curl http://localhost:8000/api/v1/graphs/ipv6_graph/vertices/summary?limit=25

#### Works with any graph
curl http://localhost:8000/api/v1/graphs/ipv4_graph/vertices/summary
curl http://localhost:8000/api/v1/graphs/igpv4_graph/vertices/summary
curl http://localhost:8000/api/v1/graphs/igpv6_graph/vertices/summary

curl http://localhost:8000/api/v1/graphs/ipv6_graph/vertices/summary
curl http://localhost:8000/api/v1/graphs/ipv6_graph/vertices/summary?vertex_collection=igp_node 
curl http://localhost:8000/api/v1/graphs/ipv6_graph/vertices/summary?vertex_collection=igp_node&limit=10


# Get all collections
curl http://localhost:8000/api/v1/collections

# Get only graph collections
curl http://localhost:8000/api/v1/collections?filter_graphs=true

# Get only non-graph collections
curl http://localhost:8000/api/v1/collections?filter_graphs=false


curl http://localhost:8000/api/v1/graphs/ipv6_graph/edges | jq .
curl http://198.18.133.104:30800/api/v1/graphs/ipv6_graph/vertices/summary | jq .
curl http://localhost:8000/api/v1/graphs/ipv6_graph/topology
curl http://localhost:8000/api/v1/graphs/ipv6_graph/topology | jq . | more
curl http://localhost:8000/api/v1/graphs/ipv6_graph/topology?limit=50


# Get all node-to-node connections
curl http://localhost:8000/api/v1/graphs/ipv6_graph/topology/nodes

# Get limited node-to-node connections
curl http://localhost:8000/api/v1/graphs/ipv6_graph/topology/nodes?limit=50


# shortest path
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path?source=gpus/host01-gpu01&destination=gpus/host12-gpu02"


curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path?source=gpus/host08-gpu02&destination=gpus/host12-gpu02&direction=any"

# latency weighted shortest path
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path/latency?source=gpus/host08-gpu02&destination=gpus/host12-gpu02"

curl "http://localhost:8000/api/v1/collections/ipv6_graph/shortest_path/latency?source=gpus/host08-gpu02&destination=gpus/host12-gpu02&direction=outbound"

curl "http://198.18.133.111:30800/api/v1/graphs/ipv6_graph/shortest_path/utilization?source=gpus/host08-gpu02&destination=gpus/host12-gpu02&direction=outbound"

curl "http://198.18.133.111:30800/api/v1/graphs/ipv6_graph/shortest_path/utilization?source=gpus/host08-gpu02&destination=gpus/host12-gpu02&direction=inbound"


# load
curl "http://localhost:8000/api/v1/graphs/ipv6_graph/shortest_path/load?source=gpus/host01-gpu02&destination=gpus/host12-gpu02&direction=any"

# reset load with AQL
FOR edge IN ipv6_graph
  UPDATE edge WITH { load: 0 } IN ipv6_graph

## or with curl
curl -X POST "http://localhost:8000/api/v1/graphs/ipv6_graph/edges" \
     -H "Content-Type: application/json" \
     -d '{"attribute": "load", "value": 0}'