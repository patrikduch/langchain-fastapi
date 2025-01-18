# fastapi-be-template

# Project startup

Prepare virtualenv
```bash
python -m venv myvenv  
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

Run the application

uvicorn main:app --reload