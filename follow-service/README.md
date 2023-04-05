# Post Service

## Setup
1. Run Neo4j:
```bash
docker compose up
```

1. Populate the graph:
```bash
python -m scripts.etl
```

1. Run the app:
```bash
export FLASK_APP=app/app.py && flask run --host=0.0.0.0 --port=5005
```
