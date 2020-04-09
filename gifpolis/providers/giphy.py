from gifpolis.provider import GifProvider
from gifpolis.file import RemoteFile

import requests

GIPHY_URL = "https://api.giphy.com/v1/gifs/search"
API_KEY = "krtZXvFiQw838hz4R8Z3zwu4ZJFx5BHh"

class GiphyProvider(GifProvider):
    def __init__(self):
        pass

    def search(query):
        params = {
            "q": query,
            "limit": 25,
            "offset": 0,
            "rating": "G",
            "lang": "en"
        }
        r = requests.get(GIPHY_URL,params=params)
        if r.status_code == 200:
            r = r.json()
            if r["meta"]["status"] != 200:
                raise Exception()

            gif_list = list()
            for gif_data in r["data"]:
                gif = RemoteFile(
                    description=gif_data["title"],
                )

        else:
            raise Exception()