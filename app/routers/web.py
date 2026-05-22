import math

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comic, Tag

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")

WINDOW = 5


def _page_window(page, total, window=WINDOW):
    if total <= 1:
        return []
    start = max(1, page - window)
    end = min(total, page + window)
    pages = []
    if start > 1:
        pages.append(1)
        if start > 2:
            pages.append(None)
    pages.extend(range(start, end + 1))
    if end < total:
        if end < total - 1:
            pages.append(None)
        pages.append(total)
    return pages


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    tags = db.query(Tag).order_by(Tag.name).all()
    return templates.TemplateResponse(request, "index.html", {"tags": tags})


@router.get("/comics", response_class=HTMLResponse)
def comic_grid(
    request: Request,
    rating: int | None = Query(None),
    tag: str | None = Query(None),
    search: str | None = Query(None),
    sort_by: str = Query("title", pattern=r"^(title|file_mtime)$"),
    sort_dir: str = Query("asc", pattern=r"^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(Comic)
    if rating is not None:
        q = q.filter(Comic.rating == rating)
    if tag:
        q = q.join(Comic.tags).filter(Tag.name == tag)
    if search:
        q = q.filter(Comic.title.ilike(f"%{search}%"))

    total = q.count()
    total_pages = math.ceil(total / page_size)

    sort_col = getattr(Comic, sort_by)
    q = q.order_by(sort_col if sort_dir == "asc" else sort_col.desc())
    q = q.offset((page - 1) * page_size).limit(page_size)
    comics = q.all()

    return templates.TemplateResponse(request, "_comic_grid.html", {
        "comics": comics,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "pages": _page_window(page, total_pages),
        "rating": rating,
        "tag": tag,
        "search": search,
        "sort_by": sort_by,
        "sort_dir": sort_dir,
    })