# Post Service

## Setup
1. Run Neo4j:
```bash
docker compose up
```

2. Create graph:
```bash
python -m scripts.create-graph
```

3. Populate table:
```bash
python -m scripts.etl
```

4. Run the app:
```bash
export FLASK_APP=follows/app.py && flask run --host=0.0.0.0 --port=5005
```
