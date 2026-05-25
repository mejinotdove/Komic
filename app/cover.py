import os
import io
import zipfile
import pathlib

from fastapi.responses import Response
from sqlalchemy.orm import Session
from PIL import Image
from PIL.Image import Resampling

from app.models import Comic
from app.config import MANKA_PATH

COVER_WIDTH = 400
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}


def _read_image_bytes(comic_path: str, comic_format: str):
    if comic_format == "dir":
        base = pathlib.Path(comic_path)
        if not base.is_dir():
            return None
        for entry in sorted(base.iterdir()):
            if entry.is_file() and entry.suffix.lower() in IMAGE_EXTENSIONS:
                return entry.read_bytes()
        return None

    reader = {
        "zip": _read_from_zip,
        "7z": _read_from_7z,
        "rar": _read_from_rar,
    }.get(comic_format)
    if reader is None:
        return None
    return reader(comic_path)


def _read_from_zip(zip_path: str):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            names = sorted(zf.namelist())
            for name in names:
                if pathlib.Path(name).suffix.lower() in IMAGE_EXTENSIONS and not name.endswith("/"):
                    return zf.read(name)
    except Exception:
        pass
    return None


def _read_from_7z(seven_zip_path: str):
    try:
        import py7zr
        with py7zr.SevenZipFile(seven_zip_path, "r") as szf:
            names = sorted(szf.getnames())
            for name in names:
                if pathlib.Path(name).suffix.lower() in IMAGE_EXTENSIONS and not name.endswith("/"):
                    return szf.read([name])[name].read()
    except Exception:
        pass
    return None


def _read_from_rar(rar_path: str):
    try:
        import rarfile
        with rarfile.RarFile(rar_path) as rf:
            names = sorted(rf.namelist())
            for name in names:
                if pathlib.Path(name).suffix.lower() in IMAGE_EXTENSIONS and not name.endswith("/"):
                    return rf.read(name)
    except Exception:
        pass
    return None


def _ensure_page_count(comic, db):
    if comic.page_count_valid:
        return
    from app.scanner import count_images_in_dir, count_images_in_zip, count_images_in_7z, count_images_in_rar
    from app.config import MANKA_PATH
    full_path = os.path.join(MANKA_PATH, comic.path)
    if comic.format == "dir":
        comic.page_count = count_images_in_dir(full_path)
    elif comic.format == "zip":
        comic.page_count = count_images_in_zip(full_path)
    elif comic.format == "7z":
        comic.page_count = count_images_in_7z(full_path)
    elif comic.format == "rar":
        comic.page_count = count_images_in_rar(full_path)
    else:
        comic.page_count = 0
    comic.page_count_valid = True
    db.commit()


def _resize_cover(image_bytes: bytes) -> bytes:
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        w, h = img.size
        if w > COVER_WIDTH:
            new_h = int(h * COVER_WIDTH / w)
            img = img.resize((COVER_WIDTH, new_h), Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85, optimize=True)
        return buf.getvalue()
    except Exception:
        return image_bytes


def get_cover_response(comic_id: int, db: Session):
    comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not comic:
        return Response(status_code=404)

    _ensure_page_count(comic, db)
    full_path = os.path.join(MANKA_PATH, comic.path)

    data = _read_image_bytes(full_path, comic.format)
    if data is None:
        return Response(status_code=404)

    data = _resize_cover(data)
    return Response(content=data, media_type="image/jpeg")
