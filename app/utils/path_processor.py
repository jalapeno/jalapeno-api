from math import ceil
from typing import List, Dict, Any
import json

def process_path_data(
    path_data: List[Dict[Any, Any]], 
    source: str, 
    destination: str,
    usid_block: str = 'fc00:0:'
) -> Dict:
    """
    Process shortest path data to extract SRv6 information
    """
    #print("path_data", path_data)
    try:
        # Debug logging
        print("=== Debug Path Processor ===")
        print(f"Received path_data type: {type(path_data)}")
        print(f"Received path_data: {json.dumps(path_data, indent=2)}")
        
        # Calculate path metrics
        hopcount = len(path_data)
        print(f"Hopcount: {hopcount}")
        
        # Extract SID locators
        locators = []
        for node in path_data:
            print(f"Processing node: {json.dumps(node, indent=2)}")
            # Check for vertex and sids in the vertex object
            if 'vertex' in node and 'sids' in node['vertex']:
                vertex_sids = node['vertex']['sids']
                if isinstance(vertex_sids, list) and len(vertex_sids) > 0:
                    sid = vertex_sids[0].get('srv6_sid')
                    if sid:
                        locators.append(sid)
                        print(f"Added SID: {sid}")
        
        print(f"Collected locators: {locators}")
        
        # Process USID information
        usid = []
        for sid in locators:
            if sid and usid_block in sid:
                usid_list = sid.split(usid_block)
                sid_value = usid_list[1]
                usid_int = sid_value.split(':')
                usid.append(usid_int[0])
                print(f"Processed USID: {usid_int[0]}")
        
        # Build SRv6 USID carrier
        sidlist = ":".join(usid) + ":"
        srv6_sid = usid_block + sidlist
        print(f"Final SRv6 SID: {srv6_sid}")
        
        result = {
            'srv6_sid_list': locators,
            'srv6_usid': srv6_sid
        }
        print(f"Returning result: {json.dumps(result, indent=2)}")
        return result
        
    except Exception as e:
        print(f"Error in path_processor: {str(e)}")
        return {
            'error': str(e),
            'srv6_sid_list': [],
            'srv6_usid': ''
        } 