import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


"""
    Creates and returns a Spotify client using the Spotipy library.
    This function sets up the OAuth authentication with Spotify using 
    the client ID, client secret, and redirect URI from environment variables.
"""
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

"""
    Prompts the user to input 3 seed tracks (artist and track name).
    Searches for these tracks on Spotify and returns a list of their track IDs.
"""
def get_seed_tracks(client):

    seed_track_ids = []
    for i in range(3):
        artist = input(f"Enter the artist for seed track {i + 1}: ")
        track_name = input(f"Enter the track name for seed track {i + 1}: ")
        
        search_result = client.search(q=f'artist:{artist} track:{track_name}')
        track_id = search_result['tracks']['items'][0]['id']
        seed_track_ids.append(track_id)
    return seed_track_ids

"""
    Creates a curated playlist based on the provided seed tracks.
    Retrieves song recommendations from Spotify and creates a new playlist 
    for the user with these recommended tracks.
"""

def create_curated_playlist(client, tracks):
    
    recommendations = client.recommendations(seed_tracks=tracks, limit=50)
    track_uris = [track['uri'] for track in recommendations['tracks']]
    
    user_id = client.current_user()['id']
    playlist_name = "My Playlist"
    playlist = client.user_playlist_create(user_id, playlist_name, public=True)
    
    client.playlist_add_items(playlist['id'], track_uris)

"""
    Main function that orchestrates the process:
    - Creates a Spotify client
    - Fetches seed tracks from the user
    - Creates a curated playlist based on the seed tracks
"""
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
