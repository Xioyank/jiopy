from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Any
from app.core.helpers import use_fetch
from app.models import SongModel

router = APIRouter(prefix="/songs", tags=["Songs"])

def parse_songs_response(raw_data: Any) -> List[SongModel]:
    songs_raw = []
    if isinstance(raw_data, dict):
        if "songs" in raw_data:
            songs_raw = raw_data["songs"]
        else:
            songs_raw = list(raw_data.values())
    elif isinstance(raw_data, list):
        songs_raw = raw_data
    return [SongModel.model_validate(song) for song in songs_raw]

@router.get("")
async def get_songs(ids: Optional[str] = None, link: Optional[str] = None):
    if not link and not ids: raise HTTPException(400, "Either song IDs or link is required")
    if link:
        token = link.split("/")[-1]
        response = await use_fetch("webapi.get", {"token": token, "type": "song"})
    else:
        response = await use_fetch("song.getDetails", {"pids": ids})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Songs not found")
    return {"success": True, "data": parse_songs_response(response["data"])}

@router.get("/{id}")
async def get_song_by_id(id: str):
    response = await use_fetch("song.getDetails", {"pids": id})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Song not found")
    return {"success": True, "data": parse_songs_response(response["data"])}

@router.get("/{id}/suggestions")
async def get_song_suggestions(id: str, limit: int = Query(10)):
    response = await use_fetch("webradio.getSong", {"stationid": id, "k": limit})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Suggestions not found")
    raw_data = response["data"]
    if isinstance(raw_data, dict) and id in raw_data: raw_data = raw_data[id]
    return {"success": True, "data": parse_songs_response(raw_data)}
