from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.core.helpers import use_fetch
from app.models import ArtistModel, SongModel, AlbumModel

router = APIRouter(prefix="/artists", tags=["Artists"])

@router.get("")
async def get_artist_by_query(id: Optional[str] = None, link: Optional[str] = None, page: int = Query(0), songCount: int = Query(10), albumCount: int = Query(10), sortBy: str = Query("popularity"), sortOrder: str = Query("asc")):
    if not id and not link: raise HTTPException(400, "Either artist 'id' or 'link' is required")
    if link:
        token = link.split("/")[-1]
        response = await use_fetch("webapi.get", {"token": token, "type": "artist", "p": page, "n_song": songCount, "n_album": albumCount, "category": sortBy, "sort_order": sortOrder})
    else:
        response = await use_fetch("artist.getArtistPageDetails", {"artistId": id, "p": page, "n_song": songCount, "n_album": albumCount, "category": sortBy, "sort_order": sortOrder})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Artist not found")
    return {"success": True, "data": ArtistModel.model_validate(response["data"])}

@router.get("/{id}")
async def get_artist_by_id(id: str, page: int = Query(0), songCount: int = Query(10), albumCount: int = Query(10), sortBy: str = Query("popularity"), sortOrder: str = Query("asc")):
    response = await use_fetch("artist.getArtistPageDetails", {"artistId": id, "p": page, "n_song": songCount, "n_album": albumCount, "category": sortBy, "sort_order": sortOrder})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Artist not found")
    return {"success": True, "data": ArtistModel.model_validate(response["data"])}

@router.get("/{id}/songs")
async def get_artist_songs(id: str, page: int = Query(0), sortBy: str = Query("popularity"), sortOrder: str = Query("desc")):
    response = await use_fetch("artist.getArtistMoreSong", {"artistId": id, "p": page, "category": sortBy, "sort_order": sortOrder})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Artist songs not found")
    raw_songs = response["data"].get("topSongs", response["data"]) if isinstance(response["data"], dict) else response["data"]
    return {"success": True, "data": [SongModel.model_validate(song) for song in raw_songs]}

@router.get("/{id}/albums")
async def get_artist_albums(id: str, page: int = Query(0), sortBy: str = Query("popularity"), sortOrder: str = Query("desc")):
    response = await use_fetch("artist.getArtistMoreAlbum", {"artistId": id, "p": page, "category": sortBy, "sort_order": sortOrder})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Artist albums not found")
    raw_albums = response["data"].get("topAlbums", response["data"]) if isinstance(response["data"], dict) else response["data"]
    return {"success": True, "data": [AlbumModel.model_validate(album) for album in raw_albums]}
