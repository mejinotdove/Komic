import os

MANKA_PATH = os.environ.get("MANKA_PATH", "/manka")
DB_PATH = os.environ.get("DB_PATH", "/data/komic.db")
DAV_PREFIX = os.environ.get("DAV_PREFIX", "/dav")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
EXCLUDE_DIRS = {d.strip() for d in os.environ.get("EXCLUDE_DIRS", "").split(",") if d.strip()}