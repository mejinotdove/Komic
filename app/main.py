import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from wsgidav.wsgidav_app import WsgiDAVApp

from app.config import DAV_PREFIX
from app.database import init_db
from app.routers import api, web
from app.dav_provider import KomicDAVProvider

app = FastAPI(title="Komic")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api.router)
app.include_router(web.router)

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