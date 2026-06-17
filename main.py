from fastapi import FastAPI
from app.routers import songs, search, albums, artists, playlists

app = FastAPI(title="JioSaavn API Wrapper")

app.include_router(songs.router)
app.include_router(search.router)
app.include_router(albums.router)
app.include_router(artists.router)
app.include_router(playlists.router)
