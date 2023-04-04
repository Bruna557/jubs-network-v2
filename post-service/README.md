# Post Service

## Setup
1. Run Cassandra:
```bash
docker compose up
```

2. Create table:
```bash
python -m scripts.create-tables
```

3. Populate table:
```bash
python -m scripts.etl
```

To test if everything is ok, connect to CQLSH:
```bash
docker exec -it cassandra bash -c "cqlsh -u cassandra -p cassandra"
```

Then run a query:
```bash
cassandra@cqlsh> select * from jubs.posts where username = 'jubs' allow filtering;
```

4. Run the app:
```bash
export FLASK_APP=posts/app.py && flask run --host=0.0.0.0 --port=5005
```

## References
https://github.com/caitlincjohnson/cassandra-noshowappts