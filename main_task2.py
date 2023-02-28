"""
Script works with
SPotify API and helps
users with finding
information about artists
"""
import os
import base64
import json
from requests import post, get
from dotenv import load_dotenv
import pycountry

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    """
    Function
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    """
    Functiion
    """
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    """
    Function
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    """
    Function
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_available_markets(token: str, song_id: str):
    """
    Function
    """
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['available_markets']

print("choose the artist")
artist_name = input("enter - ")
print("\n")

def result(artist_name: str):
    """
    function....
    """
    print("possible requests: artist, songs, available markets ")
    pos_req = input("enter - ")
    token = get_token()
    artist = search_for_artist(token, artist_name)
    songs = get_songs_by_artist(token, artist['id'])
    gam = get_available_markets(token, songs[0]['id'])
    if pos_req == "artist":
        print("\n")
        del artist['external_urls']
        del artist['href']
        del artist['images']
        del artist['uri']
        for key_a, value_a in artist.items():
            if key_a == 'followers':
                print(f"{key_a} -- {value_a['total']}")
            elif key_a == "genres":
                print(f'{key_a} -- {" ".join(value_a)}')
            else:
                print(f"{key_a} -- {value_a}")
        return "\n"

    if pos_req == "songs":
        print("\n")
        son = []
        for song in songs:
            son.append(song["name"])
        res_song = ", ".join(son)
        return(f"The most popular songs of {artist_name} -- {res_song}\n")

    if pos_req == "available markets":
        print("\n")
        res = []
        for aval_mark in gam:
            name = pycountry.countries.get(alpha_2 = aval_mark)
            if name:
                res.append(name.name)
        return (f'Available song markets -- {",".join(res)}')
    else:
        return "invalid enter"
print(result(artist_name))
