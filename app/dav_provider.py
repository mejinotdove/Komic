import os
import re
import time
import pathlib

from wsgidav.dav_provider import DAVProvider, DAVCollection, DAVNonCollection
from wsgidav.util import join_uri
from wsgidav.dav_error import DAVError, HTTP_FORBIDDEN

from app.config import MANKA_PATH
from app.models import Comic, Tag

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}


def _get_session():
    from app.database import SessionLocal
    return SessionLocal()


def _comic_member_name(comic):
    return comic.title


class KomicDAVProvider(DAVProvider):
    def get_resource_inst(self, path, environ):
        root = RootCollection(environ)
        return root.resolve(self.mount_path, path)

    def _get_comic_resource(self, comic_id, path, environ):
        db = _get_session()
        try:
            comic = db.query(Comic).filter(Comic.id == int(comic_id)).first()
            if comic:
                return _comic_resource(comic, path, environ)
            return None
        finally:
            db.close()


class RootCollection(DAVCollection):
    def __init__(self, environ):
        super().__init__("/", environ)

    def get_member_names(self):
        return ["all", "rating", "tag"]

    def get_member(self, name):
        if name == "all":
            return AllCollection(join_uri(self.path, name), self.environ)
        elif name == "rating":
            return RatingCollection(join_uri(self.path, name), self.environ)
        elif name == "tag":
            return TagRootCollection(join_uri(self.path, name), self.environ)
        return None

    def get_display_name(self):
        return "Komic"


class AllCollection(DAVCollection):
    def get_member_names(self):
        db = _get_session()
        try:
            comics = db.query(Comic).order_by(Comic.title).all()
            return [_comic_member_name(c) for c in comics]
        finally:
            db.close()

    def get_member(self, name):
        db = _get_session()
        try:
            comic = db.query(Comic).filter(Comic.title == name).first()
            if comic:
                return _comic_resource(comic, join_uri(self.path, name), self.environ)
            return None
        finally:
            db.close()

    def get_display_name(self):
        return "all"


class RatingCollection(DAVCollection):
    def get_member_names(self):
        return ["0", "1", "2", "3", "4", "5"]

    def get_member(self, name):
        return RatingValueCollection(join_uri(self.path, name), self.environ, name)

    def get_display_name(self):
        return "rating"


class RatingValueCollection(DAVCollection):
    def __init__(self, path, environ, rating):
        super().__init__(path, environ)
        self.rating = rating

    def get_member_names(self):
        db = _get_session()
        try:
            comics = db.query(Comic).filter(Comic.rating == int(self.rating)).order_by(Comic.title).all()
            return [_comic_member_name(c) for c in comics]
        finally:
            db.close()

    def get_member(self, name):
        db = _get_session()
        try:
            comic = db.query(Comic).filter(Comic.title == name).first()
            if comic:
                return _comic_resource(comic, join_uri(self.path, name), self.environ)
            return None
        finally:
            db.close()

    def get_display_name(self):
        labels = {"0": "unrated", "1": "1-star", "2": "2-star", "3": "3-star", "4": "4-star", "5": "5-star"}
        return labels.get(self.rating, self.rating)


class TagRootCollection(DAVCollection):
    def get_member_names(self):
        db = _get_session()
        try:
            tags = db.query(Tag).order_by(Tag.name).all()
            return [t.name for t in tags]
        finally:
            db.close()

    def get_member(self, name):
        return TagValueCollection(join_uri(self.path, name), self.environ, name)

    def get_display_name(self):
        return "tag"


class TagValueCollection(DAVCollection):
    def __init__(self, path, environ, tag_name):
        super().__init__(path, environ)
        self.tag_name = tag_name

    def get_member_names(self):
        db = _get_session()
        try:
            tag = db.query(Tag).filter(Tag.name == self.tag_name).first()
            if not tag:
                return []
            return [_comic_member_name(c) for c in tag.comics]
        finally:
            db.close()

    def get_member(self, name):
        db = _get_session()
        try:
            comic = db.query(Comic).filter(Comic.title == name).first()
            if comic:
                return _comic_resource(comic, join_uri(self.path, name), self.environ)
            return None
        finally:
            db.close()

    def get_display_name(self):
        return self.tag_name


def _comic_resource(comic, path, environ):
    if comic.format == "dir":
        return ComicDirResource(path, environ, comic)
    else:
        return ComicArchiveResource(path, environ, comic)


class ComicDirResource(DAVCollection):
    def __init__(self, path, environ, comic):
        super().__init__(path, environ)
        self.comic = comic
        self._dir_path = os.path.join(MANKA_PATH, comic.path)

    def get_display_name(self):
        return self.comic.title

    def get_creation_date(self):
        try:
            return os.path.getctime(self._dir_path)
        except OSError:
            return 0

    def get_last_modified(self):
        try:
            return os.path.getmtime(self._dir_path)
        except OSError:
            return 0

    def get_etag(self):
        return f"c{self.comic.id}"

    def handle_move(self, dest_path):
        m = re.match(r"^/rating/(\d)/", dest_path)
        if not m:
            return False
        rating = int(m.group(1))
        if rating < 0 or rating > 5:
            raise DAVError(HTTP_FORBIDDEN)
        db = _get_session()
        try:
            comic = db.query(Comic).filter(Comic.id == self.comic.id).first()
            if comic:
                comic.rating = rating
                db.commit()
            return True
        finally:
            db.close()

    def get_member_names(self):
        try:
            names = sorted(os.listdir(self._dir_path))
            return [n for n in names if pathlib.Path(n).suffix.lower() in IMAGE_EXTENSIONS]
        except OSError:
            return []

    def get_member(self, name):
        file_path = os.path.join(self._dir_path, name)
        if os.path.isfile(file_path):
            return ComicFileResource(join_uri(self.path, name), self.environ, file_path, name)
        return None


class ComicArchiveResource(DAVNonCollection):
    def __init__(self, path, environ, comic):
        super().__init__(path, environ)
        self.comic = comic
        self.file_path = os.path.join(MANKA_PATH, comic.path)

    def get_display_name(self):
        return os.path.basename(self.comic.path)

    def get_content_length(self):
        try:
            return os.path.getsize(self.file_path)
        except OSError:
            return 0

    def get_creation_date(self):
        try:
            return os.path.getctime(self.file_path)
        except OSError:
            return 0

    def get_last_modified(self):
        try:
            return os.path.getmtime(self.file_path)
        except OSError:
            return 0

    def get_etag(self):
        return f"a{self.comic.id}"

    def handle_move(self, dest_path):
        m = re.match(r"^/rating/(\d)/", dest_path)
        if not m:
            return False
        rating = int(m.group(1))
        if rating < 0 or rating > 5:
            raise DAVError(HTTP_FORBIDDEN)
        db = _get_session()
        try:
            comic = db.query(Comic).filter(Comic.id == self.comic.id).first()
            if comic:
                comic.rating = rating
                db.commit()
            return True
        finally:
            db.close()

    def get_content_type(self):
        ext = pathlib.Path(self.file_path).suffix.lower()
        return {
            ".zip": "application/zip",
            ".7z": "application/x-7z-compressed",
        }.get(ext, "application/octet-stream")

    def support_ranges(self):
        return True

    def get_content(self):
        return open(self.file_path, "rb")

    def support_etag(self):
        return True

    def read_block(self, offset, size):
        with open(self.file_path, "rb") as f:
            f.seek(offset)
            return f.read(size)


class ComicFileResource(DAVNonCollection):
    def __init__(self, path, environ, file_path, name):
        super().__init__(path, environ)
        self.file_path = file_path
        self._name = name

    def get_display_name(self):
        return self._name

    def get_content_length(self):
        try:
            return os.path.getsize(self.file_path)
        except OSError:
            return 0

    def get_last_modified(self):
        try:
            return os.path.getmtime(self.file_path)
        except OSError:
            return 0

    def get_etag(self):
        return f"f{os.path.getmtime(self.file_path)}"

    def get_content_type(self):
        ext = pathlib.Path(self.file_path).suffix.lower()
        return {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }.get(ext, "application/octet-stream")

    def support_ranges(self):
        return True

    def get_content(self):
        return open(self.file_path, "rb")

    def support_etag(self):
        return True

    def read_block(self, offset, size):
        with open(self.file_path, "rb") as f:
            f.seek(offset)
            return f.read(size)