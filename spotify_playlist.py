import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


load_dotenv()


    
def create_spotify_client():
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI = 'http://localhost:8080'
    
    SCOPE = "user-library-read playlist-modify-public"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE
    ))

def get_seed_tracks(client):
    seed_track_ids = []
    for i in range(3):
        artist = input(f"Enter the artist for seed track: ")
        track_name = input(f"Enter the track name for seed track: ")
        
        search_result = client.search(q=f'artist:{artist} track:{track_name}')
        track_id = search_result['tracks']['items'][0]['id']
        seed_track_ids.append(track_id)
    return seed_track_ids

def create_curated_playlist(client, tracks):
    reccomendations = client.recommendations(seed_tracks=tracks, limit=50)
    track_uris = [track['uri'] for track in reccomendations['tracks']]
    
    user_id = client.current_user()['id']
    playlist_name = "My Playlist"
    playlist  = client.user_playlist_create(user_id, playlist_name, public=True)
    
    client.playlist_add_items(playlist['id'], track_uris)
    
def main():
    try:
        print("Creating Spotify client...")
        client = create_spotify_client()
        print("Fetching seed tracks...")
        tracks_to_create_playlist = get_seed_tracks(client)
        print("Creating curated playlist...")
        create_curated_playlist(client, tracks_to_create_playlist)
        print("Done!")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
if __name__ == '__main__':
    main()