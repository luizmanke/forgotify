from typing import Dict

from fastapi import FastAPI

from server import media

app = FastAPI()


@app.get("/playlists/{user_id}")
def get_playlists(user_id: str) -> Dict:
    return {
        "playlists": media.get_playlists(user_id)
    }
