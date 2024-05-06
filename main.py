from os import environ
from time import sleep

import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials


def get_playlist_items(playlist_id):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = spotify.playlist_items(
        playlist_id,
        fields="next,total,items(track(name,external_urls.spotify,external_ids.isrc,artists(name)))"
    )

    while results:
        for item in results['items']:
            yield item

        sleep(5)
        results = spotify.next(results)


def main():
    output = []

    for env in [
        "SPOTIPY_CLIENT_ID",
        "SPOTIPY_CLIENT_SECRET",
        "PLAYLIST_ID",
        "OUTPUT_FILE"
    ]:
        if env not in environ:
            raise Exception(f"Environment variable {env} not set")

    for item in get_playlist_items(environ["PLAYLIST_ID"]):
        print(item['track']['external_urls'])
        output.append({
            "title": item['track']['name'],
            "artist": " | ".join(a['name'] for a in item['track']['artists']),
            "url": item['track']['external_urls'].get('spotify', ''),
            "isrc": item['track']['external_ids'].get('isrc'),
        })

    with open(environ['OUTPUT_FILE'], 'w') as f:
        yaml.dump(output, f)


if __name__ == '__main__':
    main()
