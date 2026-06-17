from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.core.helpers import use_fetch
from app.models import AlbumModel

router = APIRouter(prefix="/albums", tags=["Albums"])

@router.get("")
async def get_albums(id: Optional[str] = None, link: Optional[str] = None):
    if not id and not link: raise HTTPException(400, "Either album 'id' or 'link' is required")
    if link:
        token = link.split("/")[-1]
        response = await use_fetch("webapi.get", {"token": token, "type": "album"})
    else:
        response = await use_fetch("content.getAlbumDetails", {"albumid": id})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Album not found")
    return {"success": True, "data": AlbumModel.model_validate(response["data"])}
