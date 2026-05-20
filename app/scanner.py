import os
import re
import zipfile
import pathlib

from sqlalchemy.orm import Session

from app.config import MANKA_PATH
from app.models import Comic

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}
ARCHIVE_EXTENSIONS = {".zip", ".7z", ".rar"}

DATE_PREFIX_RE = re.compile(r"^(\d{8})\s*[_-]?\s*(.*)")


def clean_title(name: str) -> str:
    stem = pathlib.Path(name).stem
    m = DATE_PREFIX_RE.match(stem)
    if m:
        return m.group(2).strip() or m.group(1)
    return stem


def count_images_in_dir(dir_path: str) -> int:
    count = 0
    with os.scandir(dir_path) as it:
        for entry in it:
            if entry.is_file() and pathlib.Path(entry.name).suffix.lower() in IMAGE_EXTENSIONS:
                count += 1
    return count


def count_images_in_zip(zip_path: str) -> int:
    try:
        with zipfile.ZipFile(zip_path) as zf:
            return sum(1 for n in zf.namelist() if pathlib.Path(n).suffix.lower() in IMAGE_EXTENSIONS)
    except Exception:
        return 0


def count_images_in_7z(seven_zip_path: str) -> int:
    try:
        import py7zr
        with py7zr.SevenZipFile(seven_zip_path, "r") as szf:
            return sum(1 for n in szf.getnames() if pathlib.Path(n).suffix.lower() in IMAGE_EXTENSIONS)
    except Exception:
        return 0


def count_images_in_rar(rar_path: str) -> int:
    try:
        import rarfile
        with rarfile.RarFile(rar_path) as rf:
            return sum(1 for n in rf.namelist() if pathlib.Path(n).suffix.lower() in IMAGE_EXTENSIONS)
    except Exception:
        return 0


def scan_manka(db: Session):
    base = pathlib.Path(MANKA_PATH)
    if not base.exists():
        return {"error": f"MANKA_PATH ({MANKA_PATH}) does not exist"}

    created = 0
    updated = 0
    found_paths = set()

    date_dirs = sorted(base.iterdir())

    for date_dir in date_dirs:
        if not date_dir.is_dir():
            continue

        for entry in sorted(date_dir.iterdir()):
            title = clean_title(entry.name)
            rel_path = str(entry.relative_to(base))

            existing = db.query(Comic).filter(Comic.path == rel_path).first()

            if entry.is_dir():
                page_count = count_images_in_dir(str(entry))
                fmt = "dir"
            elif entry.suffix.lower() == ".zip":
                page_count = count_images_in_zip(str(entry))
                fmt = "zip"
            elif entry.suffix.lower() == ".7z":
                page_count = count_images_in_7z(str(entry))
                fmt = "7z"
            elif entry.suffix.lower() == ".rar":
                page_count = count_images_in_rar(str(entry))
                fmt = "rar"
            else:
                continue

            found_paths.add(rel_path)

            if existing:
                existing.title = title
                existing.format = fmt
                existing.page_count = page_count
                updated += 1
            else:
                comic = Comic(title=title, path=rel_path, format=fmt, page_count=page_count)
                db.add(comic)
                created += 1

    deleted = 0
    orphans = db.query(Comic).filter(~Comic.path.in_(found_paths)).all()
    for orphan in orphans:
        db.delete(orphan)
        deleted += 1

    db.commit()
    return {"created": created, "updated": updated, "deleted": deleted}