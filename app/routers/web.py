from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comic, Tag

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


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
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
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
    q = q.order_by(Comic.title).offset((page - 1) * page_size).limit(page_size)
    comics = q.all()

    return templates.TemplateResponse(request, "_comic_grid.html", {
        "comics": comics,
        "total": total,
        "page": page,
        "page_size": page_size,
        "rating": rating,
        "tag": tag,
        "search": search,
    })