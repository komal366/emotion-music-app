import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Replace with your actual Spotify credentials
client_id = "your_id"
client_secret = "your_key"


# Spotify authentication
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Emotion to multiple query terms
emotion_queries = {
    "Happy": ["happy", "party", "feel good", "energetic"],
    "Sad": ["sad", "acoustic", "emotional", "slow songs"],
    "Angry": ["angry", "hard rock", "metal", "intense", "punk"],
    "Neutral": ["lo-fi", "chill", "instrumental", "ambient"],
    "Surprise": ["celebration", "dance", "exciting", "pop"],
    "Fear": ["dark ambient", "suspense", "cinematic", "tense piano"],
    "Disgust": ["calm", "indie", "healing", "meditative"]
}

def get_songs(emotion):
    # Pick a random keyword for the given emotion
    query_list = emotion_queries.get(emotion, ["pop"])
    query = random.choice(query_list)

    # Random offset for freshness
    offset = random.randint(0, 30)

    # Search tracks with random offset and query
    results = sp.search(q=query, type='track', limit=10, offset=offset)

    songs = []
    for item in results['tracks']['items']:
        songs.append({
            'name': item['name'] + " - " + item['artists'][0]['name'],
            'url': item['external_urls']['spotify']
        })

    return songs
