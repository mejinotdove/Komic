import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from wsgidav.wsgidav_app import WsgiDAVApp

from app.config import DAV_PREFIX
from app.database import init_db
from app.routers import api
from app.dav_provider import KomicDAVProvider

app = FastAPI(title="Komic")

app.include_router(api.router)

dav_config = {
    "provider_mapping": {"/": KomicDAVProvider()},
    "mount_path": DAV_PREFIX,
    "http_authenticator": {"accept_basic": True, "accept_digest": False, "default_to_desktop": True},
    "simple_dc": {"user_mapping": {"*": True}},
    "verbose": 1,
}
dav_app = WsgiDAVApp(dav_config)


@app.on_event("startup")
def on_startup():
    os.makedirs(os.path.dirname(os.environ.get("DB_PATH", "/data/komic.db")), exist_ok=True)
    init_db()


@app.on_event("shutdown")
def on_shutdown():
    from app.database import checkpoint_wal
    checkpoint_wal()


from fastapi.middleware.wsgi import WSGIMiddleware
app.mount(DAV_PREFIX, WSGIMiddleware(dav_app))

frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
assets_dir = os.path.join(frontend_dist, "assets")
if os.path.isdir(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="spa_assets")


@app.get("/")
@app.get("/{full_path:path}")
def serve_spa(full_path: str = ""):
    if full_path.startswith("api/") or full_path.startswith("dav/"):
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(os.path.join(frontend_dist, "index.html"))
