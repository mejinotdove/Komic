import os
import io
import pathlib
import zipfile

from fastapi.responses import Response
from sqlalchemy.orm import Session
from PIL import Image
from PIL.Image import Resampling

from app.models import Comic
from app.config import MANKA_PATH

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}


def list_images(comic_path: str, comic_format: str) -> list[str]:
    if comic_format == "dir":
        base = pathlib.Path(comic_path)
        if not base.is_dir():
            return []
        return sorted(
            e.name for e in base.iterdir()
            if e.is_file() and e.suffix.lower() in IMAGE_EXTENSIONS
        )
    reader = {
        "zip": _list_from_zip,
        "7z": _list_from_7z,
        "rar": _list_from_rar,
    }.get(comic_format)
    if reader is None:
        return []
    return reader(comic_path)


def _list_from_zip(zip_path: str) -> list[str]:
    try:
        with zipfile.ZipFile(zip_path) as zf:
            return sorted(
                n for n in zf.namelist()
                if pathlib.Path(n).suffix.lower() in IMAGE_EXTENSIONS
                and not n.endswith("/")
            )
    except Exception:
        return []


def _list_from_7z(seven_zip_path: str) -> list[str]:
    try:
        import py7zr
        with py7zr.SevenZipFile(seven_zip_path, "r") as szf:
            return sorted(
                n for n in szf.getnames()
                if pathlib.Path(n).suffix.lower() in IMAGE_EXTENSIONS
                and not n.endswith("/")
            )
    except Exception:
        return []


def _list_from_rar(rar_path: str) -> list[str]:
    try:
        import rarfile
        with rarfile.RarFile(rar_path) as rf:
            return sorted(
                n for n in rf.namelist()
                if pathlib.Path(n).suffix.lower() in IMAGE_EXTENSIONS
                and not n.endswith("/")
            )
    except Exception:
        return []


def read_image_at_index(comic_path: str, comic_format: str, index: int) -> bytes | None:
    names = list_images(comic_path, comic_format)
    if index < 0 or index >= len(names):
        return None

    if comic_format == "dir":
        base = pathlib.Path(comic_path)
        try:
            return (base / names[index]).read_bytes()
        except Exception:
            return None

    reader = {
        "zip": _read_from_zip,
        "7z": _read_from_7z,
        "rar": _read_from_rar,
    }.get(comic_format)
    if reader is None:
        return None
    return reader(comic_path, names[index])


def _read_from_zip(zip_path: str, name: str) -> bytes | None:
    try:
        with zipfile.ZipFile(zip_path) as zf:
            return zf.read(name)
    except Exception:
        return None


def _read_from_7z(seven_zip_path: str, name: str) -> bytes | None:
    try:
        import py7zr
        with py7zr.SevenZipFile(seven_zip_path, "r") as szf:
            return szf.read([name])[name].read()
    except Exception:
        return None


def _read_from_rar(rar_path: str, name: str) -> bytes | None:
    try:
        import rarfile
        with rarfile.RarFile(rar_path) as rf:
            return rf.read(name)
    except Exception:
        return None


def _resize_image(image_bytes: bytes, width: int) -> bytes:
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        w, h = img.size
        if w > width:
            new_h = int(h * width / w)
            img = img.resize((width, new_h), Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=80, optimize=True)
        return buf.getvalue()
    except Exception:
        return image_bytes


def get_page_image(comic_id: int, page_num: int, db: Session, width: int = 150) -> Response:
    comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not comic:
        return Response(status_code=404)

    from app.cover import _ensure_page_count
    _ensure_page_count(comic, db)

    full_path = os.path.join(MANKA_PATH, comic.path)
    data = read_image_at_index(full_path, comic.format, page_num)
    if data is None:
        return Response(status_code=404)

    data = _resize_image(data, width)
    return Response(content=data, media_type="image/jpeg")
