from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any, Union
from arango import ArangoClient
from ..config.settings import Settings
import logging
from ..utils.path_processor import process_path_data
from .graphs import get_shortest_path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
settings = Settings()

# Supported metric types and their optimization strategies
SUPPORTED_METRICS = {
    'cpu_utilization': {'type': 'numeric', 'optimize': 'minimize'},
    'gpu_utilization': {'type': 'numeric', 'optimize': 'minimize'},
    'memory_utilization': {'type': 'numeric', 'optimize': 'minimize'},
    'time_to_first_token': {'type': 'numeric', 'optimize': 'minimize'},
    'cost_per_million_tokens': {'type': 'numeric', 'optimize': 'minimize'},
    'cost_per_hour': {'type': 'numeric', 'optimize': 'minimize'},
    'gpu_model': {'type': 'string', 'optimize': 'exact_match'},
    'language_model': {'type': 'string', 'optimize': 'exact_match'},
    'available_capacity': {'type': 'numeric', 'optimize': 'maximize'},
    'response_time': {'type': 'numeric', 'optimize': 'minimize'}
}

def get_db():
    client = ArangoClient(hosts=settings.database_server)
    try:
        db = client.db(
            settings.database_name,
            username=settings.username,
            password=settings.password
        )
        return db
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not connect to database: {str(e)}"
        )

def get_endpoint_metrics(endpoint_id: str, db) -> Dict[str, Any]:
    """
    Get current metrics for a specific endpoint from the hosts collection
    """
    try:
        # Extract collection and key from endpoint_id (e.g., "hosts/amsterdam" -> collection="hosts", key="amsterdam")
        if '/' in endpoint_id:
            collection_name, key = endpoint_id.split('/', 1)
        else:
            # Fallback: assume it's in hosts collection
            collection_name = 'hosts'
            key = endpoint_id
        
        if not db.has_collection(collection_name):
            logger.warning(f"Collection {collection_name} not found")
            return {}
        
        # Get the endpoint document
        endpoint_doc = db.collection(collection_name).get(key)
        if not endpoint_doc:
            logger.warning(f"Endpoint {endpoint_id} not found in collection {collection_name}")
            return {}
        
        # Extract metrics from the endpoint document
        metrics = {
            'endpoint_id': endpoint_id,
            'cpu_utilization': endpoint_doc.get('cpu_utilization'),
            'gpu_utilization': endpoint_doc.get('gpu_utilization'),
            'memory_utilization': endpoint_doc.get('memory_utilization'),
            'time_to_first_token': endpoint_doc.get('time_to_first_token'),
            'cost_per_million_tokens': endpoint_doc.get('cost_per_million_tokens'),
            'cost_per_hour': endpoint_doc.get('cost_per_hour'),
            'gpu_model': endpoint_doc.get('gpu_model'),
            'language_model': endpoint_doc.get('language_model'),
            'available_capacity': endpoint_doc.get('available_capacity'),
            'response_time': endpoint_doc.get('response_time')
        }
        
        # Remove None values to clean up the response
        return {k: v for k, v in metrics.items() if v is not None}
        
    except Exception as e:
        logger.warning(f"Could not fetch metrics for {endpoint_id}: {str(e)}")
        return {}

def select_optimal_endpoint(
    endpoints: List[Dict[str, Any]], 
    metric: str, 
    value: Optional[Union[str, float]] = None,
    db = None
) -> Dict[str, Any]:
    """
    Select the optimal endpoint based on the specified metric and criteria
    """
    try:
        if metric not in SUPPORTED_METRICS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported metric: {metric}. Supported metrics: {list(SUPPORTED_METRICS.keys())}"
            )
        
        metric_config = SUPPORTED_METRICS[metric]
        optimization_strategy = metric_config['optimize']
        
        # Get metrics for all endpoints
        endpoint_metrics = []
        for endpoint in endpoints:
            metrics = get_endpoint_metrics(endpoint['_id'], db)
            if metrics:
                endpoint_metrics.append({
                    'endpoint': endpoint,
                    'metrics': metrics
                })
        
        if not endpoint_metrics:
            raise HTTPException(
                status_code=404,
                detail="No metrics found for any endpoints"
            )
        
        # Apply selection logic based on optimization strategy
        if optimization_strategy == 'exact_match':
            if not value:
                raise HTTPException(
                    status_code=400,
                    detail=f"Value required for exact match metric: {metric}"
                )
            
            # Find endpoints that match the exact value
            matching_endpoints = [
                em for em in endpoint_metrics
                if em['metrics'].get(metric) == value
            ]
            
            if not matching_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with {metric} = {value}"
                )
            
            # If multiple matches, select the first one (could add tie-breaking logic)
            selected = matching_endpoints[0]
            
        elif optimization_strategy == 'minimize':
            # Find endpoint with minimum value for the metric (excluding null values)
            valid_endpoints = [
                em for em in endpoint_metrics 
                if em['metrics'].get(metric) is not None
            ]
            
            if not valid_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with valid {metric} values"
                )
            
            selected = min(
                valid_endpoints,
                key=lambda x: x['metrics'].get(metric)
            )
            
        elif optimization_strategy == 'maximize':
            # Find endpoint with maximum value for the metric (excluding null values)
            valid_endpoints = [
                em for em in endpoint_metrics 
                if em['metrics'].get(metric) is not None
            ]
            
            if not valid_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with valid {metric} values"
                )
            
            selected = max(
                valid_endpoints,
                key=lambda x: x['metrics'].get(metric)
            )
        
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Unknown optimization strategy: {optimization_strategy}"
            )
        
        return {
            'selected_endpoint': selected['endpoint'],
            'selection_metrics': selected['metrics'],
            'selection_reason': f"Selected based on {optimization_strategy} {metric}",
            'metric_value': selected['metrics'].get(metric),
            'total_endpoints_evaluated': len(endpoint_metrics)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error selecting optimal endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error selecting optimal endpoint: {str(e)}"
        )

@router.get("/endpoint-selection/supported-metrics")
async def get_supported_metrics():
    """
    Get list of supported metrics and their optimization strategies
    """
    return {
        'supported_metrics': SUPPORTED_METRICS
    }

@router.get("/endpoint-selection/select-optimal-endpoint")
async def select_optimal_endpoint_endpoint(
    source: str = Query(..., description="Source endpoint ID"),
    collection_name: str = Query(..., description="Collection name containing destination endpoints"),
    metric: str = Query(..., description="Metric to optimize for"),
    value: Optional[str] = Query(None, description="Required value for exact match metrics"),
    graph_collection: str = Query("igpv4_graph", description="Graph collection to use for path finding"),
    direction: str = Query("outbound", description="Direction for path finding")
):
    """
    Select optimal destination endpoint from a collection and return shortest path to it
    """
    try:
        db = get_db()
        
        # Step 1: Get all endpoints from the specified collection
        logger.info(f"Getting endpoints from collection: {collection_name}")
        
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        # Query all endpoints from the collection
        endpoints_query = f"""
        FOR doc IN {collection_name}
            RETURN {{
                _id: doc._id,
                _key: doc._key,
                name: doc.name,
                prefix: doc.prefix,
                router_id: doc.router_id,
                sids: doc.sids
            }}
        """
        
        cursor = db.aql.execute(endpoints_query)
        endpoints = [doc for doc in cursor]
        
        if not endpoints:
            raise HTTPException(
                status_code=404,
                detail=f"No endpoints found in collection {collection_name}"
            )
        
        # Step 2: Select optimal endpoint
        logger.info(f"Selecting optimal endpoint based on {metric}...")
        selection_result = select_optimal_endpoint(
            endpoints, 
            metric, 
            value, 
            db
        )
        
        selected_endpoint = selection_result['selected_endpoint']
        destination = selected_endpoint['_id']
        
        # Step 3: Find shortest path to selected endpoint
        logger.info(f"Finding shortest path from {source} to {destination}...")
        
        # Call the existing shortest path functionality
        path_result = await get_shortest_path(
            collection_name=graph_collection,
            source=source,
            destination=destination,
            direction=direction
        )
        
        # Step 4: Combine results
        return {
            'endpoint_selection': selection_result,
            'path_result': path_result,
            'summary': {
                'source': source,
                'selected_destination': destination,
                'destination_name': selected_endpoint.get('name', 'Unknown'),
                'optimization_metric': metric,
                'metric_value': selection_result['metric_value'],
                'path_found': path_result.get('found', False),
                'hop_count': path_result.get('hopcount', 0)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in select_optimal_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/endpoint-selection/select-from-list")
async def select_from_specific_endpoints(
    source: str = Query(..., description="Source endpoint ID"),
    destinations: str = Query(..., description="Comma-separated list of destination endpoint IDs"),
    metric: str = Query(..., description="Metric to optimize for"),
    value: Optional[str] = Query(None, description="Required value for exact match metrics"),
    graph_collection: str = Query("igpv4_graph", description="Graph collection to use for path finding"),
    direction: str = Query("outbound", description="Direction for path finding")
):
    """
    Select optimal destination from a specific list of endpoints
    """
    try:
        db = get_db()
        
        # Parse destination list
        destination_list = [dest.strip() for dest in destinations.split(',')]
        
        # Get endpoint details for each destination
        endpoints = []
        for dest_id in destination_list:
            # Extract collection and key from dest_id (e.g., "hosts/amsterdam" -> collection="hosts", key="amsterdam")
            if '/' in dest_id:
                collection_name, key = dest_id.split('/', 1)
                # Try to get the endpoint from the specific collection
                if db.has_collection(collection_name):
                    try:
                        endpoint = db.collection(collection_name).get(key)
                        if endpoint:
                            endpoints.append({
                                '_id': endpoint['_id'],
                                '_key': endpoint['_key'],
                                'name': endpoint.get('name', 'Unknown'),
                                'prefix': endpoint.get('prefix'),
                                'router_id': endpoint.get('router_id'),
                                'sids': endpoint.get('sids', [])
                            })
                        else:
                            logger.warning(f"Could not find endpoint: {dest_id}")
                    except Exception as e:
                        logger.warning(f"Error getting endpoint {dest_id}: {str(e)}")
                else:
                    logger.warning(f"Collection {collection_name} not found for endpoint: {dest_id}")
            else:
                # Try to find the endpoint in any collection
                found = False
                all_collections = db.collections()
                for collection_info in all_collections:
                    collection_name = collection_info['name']
                    if not collection_name.startswith('_'):
                        try:
                            endpoint = db.collection(collection_name).get(dest_id)
                            if endpoint:
                                endpoints.append({
                                    '_id': endpoint['_id'],
                                    '_key': endpoint['_key'],
                                    'name': endpoint.get('name', 'Unknown'),
                                    'prefix': endpoint.get('prefix'),
                                    'router_id': endpoint.get('router_id'),
                                    'sids': endpoint.get('sids', [])
                                })
                                found = True
                                break
                        except:
                            continue
                
                if not found:
                    logger.warning(f"Could not find endpoint: {dest_id}")
        
        if not endpoints:
            raise HTTPException(
                status_code=404,
                detail="No valid endpoints found in the provided list"
            )
        
        # Select optimal endpoint
        selection_result = select_optimal_endpoint(
            endpoints, 
            metric, 
            value, 
            db
        )
        
        selected_endpoint = selection_result['selected_endpoint']
        destination = selected_endpoint['_id']
        
        # Find shortest path
        path_result = await get_shortest_path(
            collection_name=graph_collection,
            source=source,
            destination=destination,
            direction=direction
        )
        
        return {
            'endpoint_selection': selection_result,
            'path_result': path_result,
            'summary': {
                'source': source,
                'selected_destination': destination,
                'destination_name': selected_endpoint.get('name', 'Unknown'),
                'optimization_metric': metric,
                'metric_value': selection_result['metric_value'],
                'path_found': path_result.get('found', False),
                'hop_count': path_result.get('hopcount', 0),
                'total_candidates': len(endpoints)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in select_from_specific_endpoints: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/test")
async def test_endpoint():
    """
    Simple test endpoint to verify routing is working
    """
    return {"message": "Endpoint selection API is working", "status": "ok"}

# Add this at the bottom of the file
print("\nRegistered routes in endpoint_selection.py:")
for route in router.routes:
    print(f"  {route.methods} {route.path}")

print("=" * 50)
print("ENDPOINT SELECTION ROUTES:")
for route in router.routes:
    print(f"  {route.methods} {route.path}")
print("=" * 50)