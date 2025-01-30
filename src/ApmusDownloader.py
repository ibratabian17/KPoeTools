import requests
import argparse
import json
import os

TOKEN_FILE = "tokens.json"
current_storefront = ""

def save_tokens(dev_token, music_token):
    """Save tokens to a file."""
    tokens = {
        "dev_token": dev_token,
        "music_token": music_token
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

def load_tokens():
    """Load tokens from a file."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            tokens = json.load(f)
            return tokens.get("dev_token"), tokens.get("music_token")
    else:
        with open(TOKEN_FILE, "w") as f:
            json.dump({}, f)
    return None, None

def get_headers(dev_token=None, music_token=None):
    """Return consolidated headers for API requests"""
    headers = {
        "Origin": "https://music.apple.com",
        "Referer": "https://music.apple.com/",
        "Referrer-Policy": "strict-origin",
    }
    if dev_token:
        headers["Authorization"] = f"Bearer {dev_token}"
    if music_token:
        headers["Music-User-Token"] = music_token
    else:
        print("No music token found")
    return headers

def get_developer_token():
    """Get developer token for Apple Music API."""
    url = "https://amuseic.prjktla.workers.dev/getAppleMusicAuth"
    try:
        response = requests.get(url)
        return response.json().get("dev_token")
    except:
        return None

def get_storefront(dev_token, music_token):
    """Get storefront ID using developer token."""
    global current_storefront
    url = "https://amp-api.music.apple.com/v1/me/storefront"
    if not current_storefront == "":
        return current_storefront
    response = requests.get(url, headers=get_headers(dev_token=dev_token, music_token=music_token))
    print('Getting Storefront ID...')
    if response.status_code == 200:
        data = response.json()
        current_storefront = data.get("data", [{}])[0].get("id", "US")
        print('Using Region: ', current_storefront)
        return current_storefront
    return "US"
        
def search_apple_music(music_term, dev_token, music_token, search_type="songs", limit=10):
    """Search for songs on Apple Music."""
    storefront = get_storefront(dev_token, music_token)
    url = f"https://amp-api.music.apple.com/v1/catalog/{storefront}/search"
    params = {
        "term": music_term,
        "types": search_type,
        "limit": limit
    }
    
    response = requests.get(url, headers=get_headers(dev_token=dev_token, music_token=music_token), params=params)
    if response.status_code == 200:
        data = response.json()
        return data["results"]["songs"]["data"]
    return []

def get_syllable_lyrics(dev_token, music_token, song_id):
    storefront = get_storefront(dev_token, music_token)
    """Get syllable-timed lyrics for a song."""
    url = f"https://amp-api.music.apple.com/v1/catalog/{storefront}/songs/{song_id}/syllable-lyrics"
    response = requests.get(url, headers=get_headers(dev_token=dev_token,music_token=music_token))
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            return data['data'][0].get('attributes', {}).get('ttml')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download syllable-timed lyrics from Apple Music")
    parser.add_argument("music_term", type=str, help="Song title or artist to search")
    args = parser.parse_args()
    
    dev_token, music_token = load_tokens()
    if not dev_token:
        dev_token = get_developer_token()
        save_tokens(dev_token, music_token)
        if not dev_token:
            print("Failed to get developer token")
            exit(1)

    if not music_token:
        print('Please enter your Music User Token into tokens.json')
        print('Do not share this token with anyone, or they can access your Apple Music account.')
        exit(1)
    
    songlist = search_apple_music(args.music_term, dev_token, music_token)
    song_ids = [song["id"] for song in songlist]  # get song IDs from search results
    if song_ids:
        song = songlist[0]
        song_id = song["id"]
        song_title = song["attributes"]["name"]
        artist_name = song["attributes"]["artistName"]
        album_name = song["attributes"]["albumName"]
        print(f"Song Title: {song_title}")
        print(f"Artist: {artist_name}")
        print(f"Album: {album_name}\n")
        song_title = ''.join(song_title.split())  # remove spaces
        if any(not char.isalnum() for char in song_title):
            song_title = song_id  # use song ID if title contains non-alphanumeric characters
        elif len(song_title) > 20:
            if ' ' in song_title[:20]:
                song_title = song_title[:20].rsplit(' ', 1)[0]  # cut to the last word within 20 characters
            else:
                song_title = song_title[:20]  # cut to 20 characters if no spaces

        lyrics = get_syllable_lyrics(dev_token, music_token, song_id)
        if lyrics:
            output_dir = f"output/{song_id}"
            os.makedirs(output_dir, exist_ok=True)
            with open(f"{output_dir}/{song_title}.ttml", "w", encoding="utf-8") as f:
                f.write(lyrics)
                print(f"Lyrics saved to {output_dir}/{song_title}.ttml")
        else:
            print("No lyrics found")
    else:
        print("No songs found")
