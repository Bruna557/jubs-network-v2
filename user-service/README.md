# User Service

## Setup
1. Run MongoDB and the App:
```bash
docker compose up
```

2. Drop the collections (if you want a clean database):
```bash
python -m scripts.drop-collections
```

3. Create the indexes:
```bash
python -m scripts.create-indexes
```

4. Populate collection:
```bash
python -m scripts.etl
```
