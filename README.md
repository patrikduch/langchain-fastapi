# fastapi-be-template


## Dependencies

slowapi  - rate limiter
pymongo  - MongoDB access

python-jose
passlib
PyJWT


## Project startup

Prepare virtualenv
```bash
python -m venv myvenv  
```

in case of compatibility issues

```bash
py -3.12 -m venv myvenv
```


Go to virtualevn

On Windows:
```bash
myvenv\Scripts\activate
```

On macOS and Linux:
```bash
source myvenv/bin/activate
```


Install the dependencies
```bash
pip install -r requirements.txt
```


Export local dependencies

```bash
pip freeze > requirements.txt
```


## Run the application

```bash
uvicorn main:app --reload
```


uvicorn main:app --reload --log-level debug




