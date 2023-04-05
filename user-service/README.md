# User Service

## Setup
1. Run MongoDB:
```bash
docker compose up
```

2. Drop the collections (if you want a clean database):
```bash
python -m scripts.drop-collections
```

3. Create the indexes:
```bash
python -m scripts.create-index
```

4. Populate collection:
```bash
python -m scripts.etl
```

5. Run the app:
```bash
export FLASK_APP=users/app.py && flask run --host=0.0.0.0 --port=5008
```
