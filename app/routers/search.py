from fastapi import APIRouter, HTTPException, Query
from app.core.helpers import use_fetch
from app.models import (SearchSongModel, SearchAlbumModel, SearchArtistModel, SearchPlaylistModel)

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("")
async def global_search(query: str = Query(...)):
    response = await use_fetch("autocomplete.get", {"query": query})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Search results not found")
    return {"success": True, "data": response["data"]}

@router.get("/songs")
async def search_songs(query: str = Query(...), page: int = Query(0), limit: int = Query(10)):
    response = await use_fetch("search.getResults", {"q": query, "p": page, "n": limit})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Song search results not found")
    return {"success": True, "data": SearchSongModel.model_validate(response["data"])}

@router.get("/albums")
async def search_albums(query: str = Query(...), page: int = Query(0), limit: int = Query(10)):
    response = await use_fetch("search.getAlbumResults", {"q": query, "p": page, "n": limit})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Album search results not found")
    return {"success": True, "data": SearchAlbumModel.model_validate(response["data"])}

@router.get("/artists")
async def search_artists(query: str = Query(...), page: int = Query(0), limit: int = Query(10)):
    response = await use_fetch("search.getArtistResults", {"q": query, "p": page, "n": limit})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Artist search results not found")
    return {"success": True, "data": SearchArtistModel.model_validate(response["data"])}

@router.get("/playlists")
async def search_playlists(query: str = Query(...), page: int = Query(0), limit: int = Query(10)):
    response = await use_fetch("search.getPlaylistResults", {"q": query, "p": page, "n": limit})
    if not response["ok"] or not response["data"]: raise HTTPException(404, "Playlist search results not found")
    return {"success": True, "data": SearchPlaylistModel.model_validate(response["data"])}
