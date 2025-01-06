
# imports and data passed from arango query

    path = [doc for doc in cursor]
    # print(json.dumps(path, indent=4))

    # Update edge documents with load value
    for doc in path:
        if doc.get('edge'):  # Only process if edge key exists
            # Get current edge document
            edge_doc = db.collection('collection_name').get({'_key': doc['edge']})
            # Get current load value, default to 0 if it doesn't exist
            current_load = edge_doc.get('load', 0)
            # Update with incremented load
            db.collection('collection_name').update_match(
                {'_key': doc['edge']},
                {'load': current_load + 10}
            )   
            #print("load updated for edge: ", doc['edge'])

    # Calculate average load after updates
    total_load = 0
    edge_count = 0
    for doc in path:
        if doc.get('edge'):  # Only count edges
            edge_doc = db.collection('collection_name').get({'_key': doc['edge']})
            total_load += edge_doc.get('load', 0)  # This will now get the updated load values
            edge_count += 1
    
    avg_load = total_load / edge_count if edge_count > 0 else 0
    print(f"Average load across path: {avg_load}\n")