
```
FOR doc IN hosts
    FILTER doc._key == "amsterdam"
    RETURN {
        _id: doc._id,
        _key: doc._key,
        cpu_utilization: doc.cpu_utilization,
        gpu_utilization: doc.gpu_utilization,
        memory_utilization: doc.memory_utilization,
        time_to_first_token: doc.time_to_first_token,
        cost_per_million_tokens: doc.cost_per_million_tokens,
        cost_per_hour: doc.cost_per_hour,
        gpu_model: doc.gpu_model,
        language_model: doc.language_model,
        available_capacity: doc.available_capacity,
        response_time: doc.response_time
    }
```


```
FOR doc IN hosts
    FILTER doc.gpu_utilization != null
    SORT doc.gpu_utilization ASC
    LIMIT 1
    RETURN {
        _id: doc._id,
        _key: doc._key,
        name: doc.name,
        gpu_utilization: doc.gpu_utilization
    }
```

```
FOR doc IN hosts
    FILTER doc.gpu_utilization != null
    SORT doc.gpu_utilization ASC
    LIMIT 1
    RETURN {
        _id: doc._id,
        _key: doc._key,
        name: doc.name,
        gpu_utilization: doc.gpu_utilization
    }
```