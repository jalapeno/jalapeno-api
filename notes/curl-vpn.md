## Get all VPN collections
```
curl http://localhost:8000/api/v1/vpns
curl http://localhost:8000/api/v1/vpns/l3vpn_v4_prefix | jq 
curl http://localhost:8000/api/v1/vpns/l3vpn_v4_prefix/summary | jq
curl http://localhost:8000/api/v1/vpns/l3vpn_v4_prefix/pe-routers | jq
curl http://localhost:8000/api/v1/vpns/l3vpn_v4_prefix/route-targets | jq
```

## Get prefixes
```
curl "http://localhost:8000/api/v1/vpns/l3vpn_v4_prefix/prefixes/by-rt?route_target=9:9" | jq
curl "http://localhost:8000/api/v1/vpns/l3vpn_v4_prefix/prefixes/by-pe?pe_router=fc00:0:7::1" | jq
```