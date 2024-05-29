import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.
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
    SPOTIFY_REDIRECT_URI = 'http://localhost:8080/callback'
    
    SCOPE = "user-library-read playlist-modify-public"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE
    ))

def spotify_login(request):
    sp_oauth = SpotifyOAuth(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                            scope="user-library-read playlist-modify-public")
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    sp_oauth = SpotifyOAuth(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                            scope="user-library-read playlist-modify-public")
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session['token_info'] = token_info
    return redirect('/')

def create_playlist(request):
    token_info = request.session.get('token_info')
    if not token_info:
        return redirect('/login')
    
    client = spotipy.Spotify(auth=token_info['access_token'])
    seed_tracks = get_seed_tracks(request, client)
    playlist_length = int(request.POST.get('num_songs'))
    playlist_name = request.POST.get('playlist_name')
    playlist_url = create_curated_playlist(client, seed_tracks, playlist_length, playlist_name)
    return JsonResponse({'playlist_url': playlist_url})

"""
    Prompts the user to input 3 seed tracks (artist and track name).
    Searches for these tracks on Spotify and returns a list of their track IDs.
"""
def get_seed_tracks(request, client):
    """
    Retrieves seed tracks based on user input from the frontend.
    """
    seed_track_ids = []
    for i in range(5):
        artist = request.POST.get(f'artist_{i + 1}')
        track_name = request.POST.get(f'track_name_{i + 1}')
        
        search_result = client.search(q=f'artist:{artist} track:{track_name}')
        track_id = search_result['tracks']['items'][0]['id']
        seed_track_ids.append(track_id)
    return seed_track_ids
"""
    Creates a curated playlist based on the provided seed tracks.
    Retrieves song recommendations from Spotify and creates a new playlist 
    for the user with these recommended tracks.
"""

def create_curated_playlist(client, tracks, playlist_length, playlist_name):
    recommendations = client.recommendations(seed_tracks=tracks, limit=playlist_length)
    track_uris = [track['uri'] for track in recommendations['tracks']]
    
    user_id = client.current_user()['id']
    playlist = client.user_playlist_create(user_id, playlist_name, public=True)
    
    client.playlist_add_items(playlist['id'], track_uris)
    return playlist['external_urls']['spotify']

