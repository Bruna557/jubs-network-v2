# Post Service

## Setup
1. Run Neo4j and the App:
```bash
docker compose up
```

2. Populate the graph:
```bash
python -m scripts.etl
```

3. To test that everything is ok, you can connect cypher to the container
```bash
docker exec -it neo4j bash
cypher-shell -u neo4j -p 12345678
```