from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.core.helpers import use_fetch
from app.models import PlaylistModel

router = APIRouter(prefix="/playlists", tags=["Playlists"])

@router.get("")
async def get_playlists(id: Optional[str] = None, link: Optional[str] = None, page: int = Query(0), limit: int = Query(10)):
    if not id and not link: raise HTTPException(400, "Either playlist 'id' or 'link' is required")
    if link:
        token = link.split("/")[-1]
        response = await use_fetch("webapi.get", {"token": token, "type": "playlist", "p": page, "n": limit})
    else:
        response = await use_fetch("playlist.getDetails", {"listid": id, "p": page, "n": limit})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Playlist not found")
    return {"success": True, "data": PlaylistModel.model_validate(response["data"])}
