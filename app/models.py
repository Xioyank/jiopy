import json
from typing import List, Optional, Any
from pydantic import BaseModel, model_validator
from app.core.helpers import create_download_links, create_image_links

class QualityUrl(BaseModel):
    quality: str
    url: str

class SongModel(BaseModel):
    id: str
    title: str
    subtitle: str
    type: str
    image: List[QualityUrl]
    play_count: Optional[str] = None
    explicit_content: Optional[str] = None
    download_links: List[QualityUrl]

    @model_validator(mode='before')
    @classmethod
    def transform_raw_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            image_raw = data.get("image", "")
            image_links = create_image_links(image_raw)
            
            more_info = data.get("more_info", {})
            if isinstance(more_info, str):
                try:
                    more_info = json.loads(more_info)
                except json.JSONDecodeError:
                    more_info = {}
            
            encrypted_media_url = more_info.get("encrypted_media_url", "")
            download_links = create_download_links(encrypted_media_url)
            
            return {
                "id": data.get("id", ""),
                "title": data.get("title", ""),
                "subtitle": data.get("subtitle", ""),
                "type": data.get("type", "song"),
                "play_count": data.get("play_count"),
                "explicit_content": data.get("explicit_content"),
                "image": image_links,
                "download_links": download_links
            }
        return data

class AlbumModel(BaseModel):
    id: str
    title: str
    subtitle: Optional[str] = None
    year: Optional[str] = None
    language: Optional[str] = None
    image: List[QualityUrl]
    songs: List[SongModel] = []
    @model_validator(mode='before')
    @classmethod
    def transform_raw_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                "id": data.get("id", ""),
                "title": data.get("title", ""),
                "subtitle": data.get("subtitle"),
                "year": data.get("year"),
                "language": data.get("language"),
                "image": create_image_links(data.get("image", "")),
                "songs": data.get("songs", [])
            }
        return data

class ArtistModel(BaseModel):
    id: str
    name: str
    image: List[QualityUrl]
    follower_count: Optional[str] = None
    is_verified: Optional[bool] = None
    dominant_language: Optional[str] = None
    top_songs: List[SongModel] = []
    top_albums: List[AlbumModel] = []
    @model_validator(mode='before')
    @classmethod
    def transform_raw_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                "id": data.get("artistId", data.get("id", "")),
                "name": data.get("name", ""),
                "image": create_image_links(data.get("image", "")),
                "follower_count": data.get("follower_count"),
                "is_verified": data.get("isVerified"),
                "dominant_language": data.get("dominantLanguage"),
                "top_songs": data.get("topSongs", []),
                "top_albums": data.get("topAlbums", [])
            }
        return data

class PlaylistModel(BaseModel):
    id: str
    title: str
    subtitle: Optional[str] = None
    image: List[QualityUrl]
    track_count: Optional[str] = None
    songs: List[SongModel] = []
    @model_validator(mode='before')
    @classmethod
    def transform_raw_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                "id": data.get("id", ""),
                "title": data.get("title", ""),
                "subtitle": data.get("subtitle"),
                "image": create_image_links(data.get("image", "")),
                "track_count": data.get("list_count"),
                "songs": data.get("list", [])
            }
        return data

class SearchResponseBase(BaseModel):
    total: int
    start: int
class SearchSongModel(SearchResponseBase):
    results: List[SongModel]
class SearchAlbumModel(SearchResponseBase):
    results: List[AlbumModel]
class SearchArtistModel(SearchResponseBase):
    results: List[ArtistModel]
class SearchPlaylistModel(SearchResponseBase):
    results: List[PlaylistModel]
class GlobalSearchModel(BaseModel):
    songs: SearchSongModel
    albums: SearchAlbumModel
    artists: SearchArtistModel
    playlists: SearchPlaylistModel
