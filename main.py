from bs4 import BeautifulSoup
import requests
import os



date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
Client_ID = os.environ.get("Your_Client_ID")
Client_Status = os.environ.get("Your_Client_Status")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
for i in song_names:
    print(i)
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Spotify_User_ID = os.environ.get("Your_Spotify_User_ID")
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Status,
        show_dialog=True,
        cache_path="token.txt",
        username=Spotify_User_ID,
    ))
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"Added {len(song_uris)} songs to {date} Old Time 100 playlist.")
