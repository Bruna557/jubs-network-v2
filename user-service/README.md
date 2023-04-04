# Post Service

## Setup
1. Run MongoDB:
```bash
docker compose up
```

1. Populate collection:
```bash
python -m scripts.etl
```

3. Run the app:
```bash
export FLASK_APP=users/app.py && flask run --host=0.0.0.0 --port=5005
```

## References
https://github.com/caitlincjohnson/cassandra-noshowappts
