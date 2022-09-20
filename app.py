import os
import spotipy
import requests
import base64
from slugify import slugify
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from lib.image import compress_img
from data.tracks import albums

"""
.env file should contain the following:

SPOTIFY_USERNAME='your-spotify-username'

SPOTIPY_CLIENT_ID='your-spotify-client-id'
SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
SPOTIPY_REDIRECT_URI='your-app-redirect-url'
"""
load_dotenv()

scopes = [
    "playlist-modify-public",
    "user-read-currently-playing",
    "user-modify-playback-state",
    "playlist-read-private",
    "playlist-modify-private",
    "user-library-read",
    "user-read-playback-state",
    "ugc-image-upload",
    "playlist-modify-public",
    "playlist-modify-private",
]

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=" ".join(scopes), username=os.environ.get("SPOTIFY_USERNAME")
    )
)

print(f"Olá {spotify.me()['display_name']}!")
print("Seja bem-vindo ao SESPG ou Summer Eletrohits Spotify Playlist Generator!")
print(
    "Você está prestes a criar todos os álbums do Summer Eletrohits na sua conta do Spotify!"
)
print(
    "Lembrando que as playlists criadas serão privadas, logo, somente você poderá vê-las."
)

q = input("Vamos começar? [S/n] ")
if q.lower() == "n" or (q.lower() != "n" and q.lower() != "s"):
    print("Ok, até a próxima!")
    exit(0)

print("Criando playlists...")

print("-" * 10, "\n\n")

for album in albums:
    # Prints the album name centered in a text box
    print("=" * 10)
    print(f"{album['albumName']:^10}")
    print("=" * 10, "\n")

    # Verifica se a playlist já existe
    playlists = spotify.current_user_playlists()
    playlist_exists = False
    for playlist in playlists["items"]:
        if playlist["name"] == album["albumName"]:
            playlist_exists = True
            print(f"~> Playlist '{album['albumName']}' já existe.")
            break

    if playlist_exists:
        continue

    playlist_data = {
        "name": album["albumName"],
        "songs": [],
        "description": f"Playlist do álbum {album['albumName']}, lançado em {album['albumDate']} e um clássico da era pré-streaming no Brasil. Esse álbum foi gerado automaticamente e por isso pode conter músicas erradas! Gerado por: https://github.com/luizfx22/SESPG"[
            0:300
        ],
    }

    print(f"~> Buscando músicas...")
    for track in album["tracks"]:
        res = spotify.search(track, limit=50, type="track")
        if res["tracks"]["total"] == 0:
            print(f"~> Nenhuma música encontrada para '{track}'")
            continue

        playlist_data["songs"].append(res["tracks"]["items"][0]["uri"])

    print(f"~> Baixando imagem do álbum...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    res = requests.get(album["albumCover"], headers=headers)

    extension = album["albumCover"].split(".")[-1]
    album_cover_image_path = (
        f"album-covers/{slugify(album['albumName'], True)}.{extension}"
    )

    if not os.path.exists(album_cover_image_path):
        with open(album_cover_image_path, "wb") as f:
            f.write(res.content)
            f.close()
        res.close()

    print(f"~> Criando playlist...")

    playlist = spotify.user_playlist_create(
        os.environ.get("SPOTIFY_USERNAME"),
        name=playlist_data["name"],
        description=playlist_data["description"],
        public=False,
    )

    with open(album_cover_image_path, "rb") as f1:
        image = f1.read()

        if os.path.getsize(album_cover_image_path) / 1024 >= 200:
            album_cover_image_path = compress_img(
                album_cover_image_path, new_size_ratio=5.5
            )
            f1.close()

        with open(album_cover_image_path, "rb") as f:
            image = f.read()
            f.close()

        image_64_encode = base64.b64encode(image)
        image_64_encode = image_64_encode.decode("utf-8")

        spotify.playlist_upload_cover_image(playlist["id"], image_b64=image_64_encode)

    print(f"~> Adicionando músicas...")
    spotify.playlist_add_items(playlist["id"], playlist_data["songs"])

    print(f"~> Playlist criada com sucesso: {playlist['external_urls']['spotify']}")
    print("-" * 10, "\n\n")

print("~> Fim!")
