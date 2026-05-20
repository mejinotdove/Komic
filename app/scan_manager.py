import threading
import time

from app.database import SessionLocal


class ScanStatus:
    def __init__(self):
        self.running = False
        self.total = 0
        self.processed = 0
        self.created = 0
        self.updated = 0
        self.deleted = 0
        self.error = None
        self.lock = threading.Lock()

    def as_dict(self):
        with self.lock:
            return {
                "running": self.running,
                "total": self.total,
                "processed": self.processed,
                "created": self.created,
                "updated": self.updated,
                "deleted": self.deleted,
                "error": self.error,
            }


_scan_status = None
_scan_lock = threading.Lock()


def start_scan() -> bool:
    global _scan_status, _scan_lock
    with _scan_lock:
        if _scan_status and _scan_status.running:
            return False
        status = ScanStatus()
        status.running = True
        _scan_status = status

    def _run():
        db = SessionLocal()
        try:
            from app.scanner import scan_manka
            result = scan_manka(db, status)
            with status.lock:
                status.running = False
                status.created = result.get("created", 0)
                status.updated = result.get("updated", 0)
                status.deleted = result.get("deleted", 0)
                status.error = result.get("error")
        except Exception as e:
            with status.lock:
                status.running = False
                status.error = str(e)
        finally:
            db.close()

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return True


def get_scan_status() -> dict:
    global _scan_status
    if _scan_status is None:
        return {"running": False, "total": 0, "processed": 0,
                "created": 0, "updated": 0, "deleted": 0, "error": None}
    return _scan_status.as_dict()
