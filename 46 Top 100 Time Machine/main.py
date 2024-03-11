from spotipy.oauth2 import SpotifyOAuth
import requests as req
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import spotipy


load_dotenv()

SPOTIFY_ID = os.environ["SPOTIFY_ID"]
SPOTIFY_SECRET = os.environ["SPOTIFY_SECRET"]
SPOTIFY_API_URL = "https://api.spotify.com/v1"

date = input("What year would you like to travel to? (YYYY-MM-DD) ")
print("Preparing your playlist")
# date = "2011-12-04"

url = f"https://www.billboard.com/charts/hot-100/{date}/"

res = req.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

songs = soup.select("li ul li h3")
songs = [song.getText().strip() for song in songs]


# Allow from user
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


# Create playlist
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard Top 100",
    description=f"A playlist of the Billboard Top 100 on {
        date}. Made with the Top 100 Time Machine.",
    public=False
)

# Add songs to playlist
song_uris = []
for song in songs:
    res = sp.search(
        q=f"track:{song} year:{date.split("-")[0]}", type="track"
    )
    try:
        uri = res["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

print(f"View playlist here: {playlist["external_urls"]["spotify"]}")
