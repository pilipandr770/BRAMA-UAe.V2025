import sys
import os
# ensure project root is on sys.path so `import app` works when running this script
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app

app = create_app()
client = app.test_client()
resp = client.get('/')
print('GET / =>', resp.status_code)
