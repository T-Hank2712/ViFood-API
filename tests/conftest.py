import os
import sys
from dotenv import load_dotenv

# Ensure project root is on sys.path so tests can import `app`
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Load .env if present (useful for local dev). In CI the file may be missing,
# so provide sensible defaults required by Settings to avoid import-time errors.
load_dotenv(os.path.join(ROOT, '.env'))

# Minimal defaults to allow pytest collection when .env isn't available.
os.environ.setdefault('NEO4J_URI', 'bolt://127.0.0.1:7687')
os.environ.setdefault('NEO4J_USERNAME', 'neo4j')
os.environ.setdefault('NEO4J_PASSWORD', 'neo4j')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('ACCESS_TOKEN_EXPIRE_MINUTES', '15')
os.environ.setdefault('REFRESH_TOKEN_EXPIRE_DAYS', '30')
os.environ.setdefault('ALGORITHM', 'HS256')
