import os
import zipfile
import pathlib

from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session

from app.models import Comic
from app.config import MANKA_PATH

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}


def _cover_from_dir(comic_path: str):
    base = pathlib.Path(comic_path)
    if not base.is_dir():
        return None
    for entry in sorted(base.iterdir()):
        if entry.is_file() and entry.suffix.lower() in IMAGE_EXTENSIONS:
            return entry
    return None


def _cover_from_zip(zip_path: str):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            names = sorted(zf.namelist())
            for name in names:
                if pathlib.Path(name).suffix.lower() in IMAGE_EXTENSIONS and not name.endswith("/"):
                    data = zf.read(name)
                    ext = pathlib.Path(name).suffix.lower()
                    return data, ext
    except Exception:
        pass
    return None


def _cover_from_7z(seven_zip_path: str):
    try:
        import py7zr
        with py7zr.SevenZipFile(seven_zip_path, "r") as szf:
            names = sorted(szf.getnames())
            for name in names:
                if pathlib.Path(name).suffix.lower() in IMAGE_EXTENSIONS and not name.endswith("/"):
                    data = szf.read([name])[name].read()
                    ext = pathlib.Path(name).suffix.lower()
                    return data, ext
    except Exception:
        pass
    return None


def get_cover_response(comic_id: int, db: Session):
    comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not comic:
        return Response(status_code=404)

    full_path = os.path.join(MANKA_PATH, comic.path)

    if comic.format == "dir":
        found = _cover_from_dir(full_path)
        if found:
            ext = found.suffix.lower()
            mime = mimetype_from_ext(ext)
            return StreamingResponse(open(found, "rb"), media_type=mime)
    elif comic.format == "zip":
        result = _cover_from_zip(full_path)
        if result:
            data, ext = result
            mime = mimetype_from_ext(ext)
            return Response(content=data, media_type=mime)
    elif comic.format == "7z":
        result = _cover_from_7z(full_path)
        if result:
            data, ext = result
            mime = mimetype_from_ext(ext)
            return Response(content=data, media_type=mime)

    return Response(status_code=404)


def mimetype_from_ext(ext: str) -> str:
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
        ".avif": "image/avif",
    }.get(ext, "application/octet-stream")