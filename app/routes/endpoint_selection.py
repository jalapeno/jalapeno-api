from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any, Union
from arango import ArangoClient
from ..config.settings import Settings
import logging

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

@router.get("/endpoint-selection")
async def get_endpoint_selection_info():
    """
    Get information about endpoint selection capabilities
    """
    return {
        'supported_metrics': SUPPORTED_METRICS,
        'description': 'Endpoint selection API for intelligent destination selection'
    }

@router.get("/endpoint-selection/{collection_name}")
async def get_collection_endpoints(
    collection_name: str,
    limit: Optional[int] = None
):
    """
    Get all endpoints from a specific collection with their metrics
    """
    try:
        db = get_db()
        
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        # Query all endpoints from the collection
        endpoints_query = f"""
        FOR doc IN {collection_name}
            RETURN doc
        """
        
        if limit:
            endpoints_query = f"""
            FOR doc IN {collection_name}
                LIMIT {limit}
                RETURN doc
            """
        
        cursor = db.aql.execute(endpoints_query)
        endpoints = [doc for doc in cursor]
        
        return {
            'collection': collection_name,
            'type': 'collection',
            'count': len(endpoints),
            'data': endpoints
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting collection endpoints: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/endpoint-selection/{collection_name}/select-optimal")
async def select_optimal_endpoint(
    collection_name: str,
    source: str = Query(..., description="Source endpoint ID"),
    metric: str = Query(..., description="Metric to optimize for"),
    value: Optional[str] = Query(None, description="Required value for exact match metrics")
):
    """
    Select optimal destination endpoint from a collection based on metrics
    """
    try:
        db = get_db()
        
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        if metric not in SUPPORTED_METRICS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported metric: {metric}. Supported metrics: {list(SUPPORTED_METRICS.keys())}"
            )
        
        # Get all endpoints from the collection
        endpoints_query = f"""
        FOR doc IN {collection_name}
            RETURN doc
        """
        
        cursor = db.aql.execute(endpoints_query)
        endpoints = [doc for doc in cursor]
        
        if not endpoints:
            raise HTTPException(
                status_code=404,
                detail=f"No endpoints found in collection {collection_name}"
            )
        
        # Filter endpoints with valid metric values
        metric_config = SUPPORTED_METRICS[metric]
        optimization_strategy = metric_config['optimize']
        
        if optimization_strategy == 'exact_match':
            if not value:
                raise HTTPException(
                    status_code=400,
                    detail=f"Value required for exact match metric: {metric}"
                )
            
            # Find endpoints that match the exact value
            valid_endpoints = [
                ep for ep in endpoints
                if ep.get(metric) == value
            ]
            
            if not valid_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with {metric} = {value}"
                )
            
            selected_endpoint = valid_endpoints[0]
            
        elif optimization_strategy == 'minimize':
            # Find endpoint with minimum value for the metric (excluding null values)
            valid_endpoints = [
                ep for ep in endpoints 
                if ep.get(metric) is not None
            ]
            
            if not valid_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with valid {metric} values"
                )
            
            selected_endpoint = min(
                valid_endpoints,
                key=lambda x: x.get(metric)
            )
            
        elif optimization_strategy == 'maximize':
            # Find endpoint with maximum value for the metric (excluding null values)
            valid_endpoints = [
                ep for ep in endpoints 
                if ep.get(metric) is not None
            ]
            
            if not valid_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with valid {metric} values"
                )
            
            selected_endpoint = max(
                valid_endpoints,
                key=lambda x: x.get(metric)
            )
        
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Unknown optimization strategy: {optimization_strategy}"
            )
        
        return {
            'collection': collection_name,
            'source': source,
            'selected_endpoint': selected_endpoint,
            'optimization_metric': metric,
            'metric_value': selected_endpoint.get(metric),
            'optimization_strategy': optimization_strategy,
            'total_endpoints_evaluated': len(endpoints),
            'valid_endpoints_count': len(valid_endpoints) if 'valid_endpoints' in locals() else len(endpoints)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in select_optimal_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/endpoint-selection/{collection_name}/select-from-list")
async def select_from_specific_endpoints(
    collection_name: str,
    source: str = Query(..., description="Source endpoint ID"),
    destinations: str = Query(..., description="Comma-separated list of destination endpoint IDs"),
    metric: str = Query(..., description="Metric to optimize for"),
    value: Optional[str] = Query(None, description="Required value for exact match metrics")
):
    """
    Select optimal destination from a specific list of endpoints
    """
    try:
        db = get_db()
        
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        if metric not in SUPPORTED_METRICS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported metric: {metric}. Supported metrics: {list(SUPPORTED_METRICS.keys())}"
            )
        
        # Parse destination list
        destination_list = [dest.strip() for dest in destinations.split(',')]
        
        # Get endpoint details for each destination
        endpoints = []
        for dest_id in destination_list:
            # Extract collection and key from dest_id (e.g., "hosts/amsterdam" -> collection="hosts", key="amsterdam")
            if '/' in dest_id:
                dest_collection, key = dest_id.split('/', 1)
            else:
                dest_collection = collection_name
                key = dest_id
            
            # Try to get the endpoint from the specific collection
            if db.has_collection(dest_collection):
                try:
                    endpoint = db.collection(dest_collection).get(key)
                    if endpoint:
                        endpoints.append(endpoint)
                    else:
                        logger.warning(f"Could not find endpoint: {dest_id}")
                except Exception as e:
                    logger.warning(f"Error getting endpoint {dest_id}: {str(e)}")
            else:
                logger.warning(f"Collection {dest_collection} not found for endpoint: {dest_id}")
        
        if not endpoints:
            raise HTTPException(
                status_code=404,
                detail="No valid endpoints found in the provided list"
            )
        
        # Apply selection logic
        metric_config = SUPPORTED_METRICS[metric]
        optimization_strategy = metric_config['optimize']
        
        if optimization_strategy == 'exact_match':
            if not value:
                raise HTTPException(
                    status_code=400,
                    detail=f"Value required for exact match metric: {metric}"
                )
            
            valid_endpoints = [
                ep for ep in endpoints
                if ep.get(metric) == value
            ]
            
            if not valid_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with {metric} = {value}"
                )
            
            selected_endpoint = valid_endpoints[0]
            
        elif optimization_strategy == 'minimize':
            valid_endpoints = [
                ep for ep in endpoints 
                if ep.get(metric) is not None
            ]
            
            if not valid_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with valid {metric} values"
                )
            
            selected_endpoint = min(
                valid_endpoints,
                key=lambda x: x.get(metric)
            )
            
        elif optimization_strategy == 'maximize':
            valid_endpoints = [
                ep for ep in endpoints 
                if ep.get(metric) is not None
            ]
            
            if not valid_endpoints:
                raise HTTPException(
                    status_code=404,
                    detail=f"No endpoints found with valid {metric} values"
                )
            
            selected_endpoint = max(
                valid_endpoints,
                key=lambda x: x.get(metric)
            )
        
        return {
            'collection': collection_name,
            'source': source,
            'selected_endpoint': selected_endpoint,
            'optimization_metric': metric,
            'metric_value': selected_endpoint.get(metric),
            'optimization_strategy': optimization_strategy,
            'total_candidates': len(endpoints),
            'valid_endpoints_count': len(valid_endpoints) if 'valid_endpoints' in locals() else len(endpoints)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in select_from_specific_endpoints: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )