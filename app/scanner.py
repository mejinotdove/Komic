import os
import pathlib

from sqlalchemy.orm import Session

from app.config import MANKA_PATH, EXCLUDE_DIRS
from app.models import Comic


def _detect_format(entry):
    if entry.is_dir():
        return "dir"
    suffix = entry.suffix.lower() if hasattr(entry, "suffix") else pathlib.Path(entry.name).suffix.lower()
    if suffix == ".zip":
        return "zip"
    elif suffix == ".7z":
        return "7z"
    elif suffix == ".rar":
        return "rar"
    return None


def clean_title(name: str) -> str:
    stem = pathlib.Path(name).stem
    import re
    m = re.match(r"^(\d{8})\s*[_-]?\s*(.*)", stem)
    if m:
        return m.group(2).strip() or m.group(1)
    return stem


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}


def count_images_in_dir(dir_path: str) -> int:
    count = 0
    with os.scandir(dir_path) as it:
        for entry in it:
            if entry.is_file() and pathlib.Path(entry.name).suffix.lower() in IMAGE_EXTENSIONS:
                count += 1
    return count


def count_images_in_zip(zip_path: str) -> int:
    try:
        import zipfile
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


def _count_total_entries(base: pathlib.Path) -> int:
    total = 0
    try:
        for date_dir in base.iterdir():
            if not date_dir.is_dir():
                continue
            if date_dir.name in EXCLUDE_DIRS:
                continue
            total += sum(1 for _ in date_dir.iterdir())
    except OSError:
        pass
    return total


def scan_manka(db: Session, status=None):
    base = pathlib.Path(MANKA_PATH)
    if not base.exists():
        return {"error": f"MANKA_PATH ({MANKA_PATH}) does not exist"}

    created = 0
    updated = 0
    deleted = 0

    date_dirs = sorted(base.iterdir())

    if status:
        status.total = _count_total_entries(base)
        status.processed = 0

    processed = 0

    for date_dir in date_dirs:
        if not date_dir.is_dir():
            continue
        if date_dir.name in EXCLUDE_DIRS:
            continue

        prefix = date_dir.name + "/"

        existing_map = {
            c.path: c for c in db.query(Comic)
            .filter(Comic.path.like(f"{prefix}%"))
            .all()
        }

        for entry in sorted(date_dir.iterdir()):
            try:
                rel_path = str(entry.relative_to(base))
            except ValueError:
                continue

            fmt = _detect_format(entry)
            if fmt is None:
                continue

            title = clean_title(entry.name)
            current_mtime = entry.stat().st_mtime
            existing = existing_map.pop(rel_path, None)

            if existing:
                if existing.file_mtime is not None and existing.file_mtime == current_mtime:
                    processed += 1
                    if status:
                        with status.lock:
                            status.processed = processed
                    continue

                existing.title = title
                existing.format = fmt
                existing.file_mtime = current_mtime
                existing.page_count = None
                existing.page_count_valid = False
                updated += 1
            else:
                comic = Comic(
                    title=title,
                    path=rel_path,
                    format=fmt,
                    file_mtime=current_mtime,
                    page_count=None,
                    page_count_valid=False,
                )
                db.add(comic)
                created += 1

            processed += 1
            if status:
                with status.lock:
                    status.processed = processed

        for orphan in existing_map.values():
            db.delete(orphan)
            deleted += 1

        db.commit()

    if status:
        with status.lock:
            status.running = False
            status.created = created
            status.updated = updated
            status.deleted = deleted

    return {"created": created, "updated": updated, "deleted": deleted}
