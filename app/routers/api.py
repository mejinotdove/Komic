from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models import Comic, Tag
from app.scanner import scan_manka
from app.cover import get_cover_response

router = APIRouter(prefix="/api", tags=["api"])


class ComicOut(BaseModel):
    id: int
    title: str
    path: str
    format: str
    rating: int
    page_count: Optional[int] = None
    tags: list[str] = []

    class Config:
        from_attributes = True


class TagOut(BaseModel):
    id: int
    name: str
    color: Optional[str] = None
    comic_count: int = 0

    class Config:
        from_attributes = True


@router.get("/comics")
def list_comics(
    rating: Optional[int] = Query(None),
    tag: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
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

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            ComicOut(
                id=c.id,
                title=c.title,
                path=c.path,
                format=c.format,
                rating=c.rating,
                page_count=c.page_count,
                tags=[t.name for t in c.tags],
            )
            for c in comics
        ],
    }


@router.get("/comics/{comic_id}")
def get_comic(comic_id: int, db: Session = Depends(get_db)):
    comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not comic:
        return {"error": "not found"}, 404
    return ComicOut(
        id=comic.id,
        title=comic.title,
        path=comic.path,
        format=comic.format,
        rating=comic.rating,
        page_count=comic.page_count,
        tags=[t.name for t in comic.tags],
    )


@router.get("/comics/{comic_id}/cover")
def comic_cover(comic_id: int, db: Session = Depends(get_db)):
    return get_cover_response(comic_id, db)


@router.post("/comics/{comic_id}/rating")
def set_rating(comic_id: int, rating: int = Query(..., ge=0, le=5), request: Request = None, db: Session = Depends(get_db)):
    comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not comic:
        return {"error": "not found"}, 404
    comic.rating = rating
    db.commit()

    is_htmx = request and request.headers.get("HX-Request") == "true"
    if is_htmx:
        from app.routers.web import templates
        return templates.TemplateResponse(request, "_stars.html", {"comic": comic})
    return {"id": comic.id, "rating": comic.rating}


class TagAction(BaseModel):
    action: str
    tag: str


@router.post("/comics/{comic_id}/tags")
def update_tags(comic_id: int, body: TagAction, db: Session = Depends(get_db)):
    comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not comic:
        return {"error": "not found"}, 404

    tag = db.query(Tag).filter(Tag.name == body.tag).first()
    if not tag:
        tag = Tag(name=body.tag)
        db.add(tag)
        db.flush()

    if body.action == "add":
        if tag not in comic.tags:
            comic.tags.append(tag)
    elif body.action == "remove":
        if tag in comic.tags:
            comic.tags.remove(tag)

    db.commit()
    return {"id": comic.id, "tags": [t.name for t in comic.tags]}


@router.get("/tags")
def list_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).order_by(Tag.name).all()
    return [
        TagOut(id=t.id, name=t.name, color=t.color, comic_count=len(t.comics))
        for t in tags
    ]


@router.delete("/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        return {"error": "not found"}, 404
    db.delete(tag)
    db.commit()
    return {"ok": True}


@router.post("/scan")
def trigger_scan(db: Session = Depends(get_db)):
    result = scan_manka(db)
    return JSONResponse(content=result, headers={"HX-Trigger": "scan-complete"})