import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# define the required scopes
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-library-read'

# authenticate and create a spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# test authentication by fetching the current user's profile
user = sp.current_user()
print(f"Authenticated as: {user['display_name']} ({user['id']})")

# function to fetch all albums and singles of an artist
def fetch_artist_albums(artist_name):
    search_results = sp.search(q=artist_name, type='artist', limit=1)
    if not search_results['artists']['items']:
        print(f"Artist '{artist_name}' not found.")
        return None, None

    artist = search_results['artists']['items'][0]
    artist_id = artist['id']
    print(f"\nArtist: {artist['name']}")

    # fetch artist's albums and singles
    results = sp.artist_albums(artist_id, include_groups='album,single')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    album_list = []
    for album in albums:
        album_list.append(album['name'])

    print("\nAlbums and Singles:")
    for idx, album in enumerate(album_list):
        print(f"{idx + 1}. {album}")

    return artist, albums

# function to fetch tracks from selected albums
def fetch_tracks_from_albums(albums):
    all_tracks = []
    for album in albums:
        album_tracks = sp.album_tracks(album['id'])['items']
        for track in album_tracks:
            track_details = sp.track(track['uri'])
            popularity = track_details['popularity']
            all_tracks.append({
                "uri": track['uri'],
                "name": track['name'],
                "album": album['name'],
                "artist": album['artists'][0]['name'],
                "popularity": popularity
            })
    return all_tracks

# function to play sorted tracks directly, effectively clearing the existing queue
def play_sorted_tracks(tracks):
    # sort tracks by popularity
    sorted_tracks = sorted(tracks, key=lambda x: x['popularity'], reverse=True)

    # get the active playback device
    devices = sp.devices()['devices']
    if not devices:
        print("No active playback device found.")
        return

    device_id = devices[0]['id']  # Use the first available device

    # play the sorted tracks directly, replacing the current queue
    track_uris = [track['uri'] for track in sorted_tracks]
    sp.start_playback(device_id=device_id, uris=track_uris)
    print("\nPlaying sorted tracks directly on the current device...")

# main execution
all_tracks = []
while True:
    artist_name = input("Enter an artist's name: ")
    artist, albums = fetch_artist_albums(artist_name)
    if not albums:
        continue

    choice = input("Do you want to include the entire discography or specific albums? (entire/specific): ").lower()
    if choice == 'entire':
        all_tracks.extend(fetch_tracks_from_albums(albums))
    elif choice == 'specific':
        selected = input("Enter album numbers separated by commas: ").split(',')
        selected_albums = [albums[int(num) - 1] for num in selected if num.isdigit() and 1 <= int(num) <= len(albums)]
        all_tracks.extend(fetch_tracks_from_albums(selected_albums))
    else:
        print("Invalid choice. Skipping this artist.")

    more_artists = input("Do you want to add another artist? (y/n): ").lower()
    if more_artists != 'y':
        break

if all_tracks:
    print("\nSorting tracks by popularity and playing them...")
    play_sorted_tracks(all_tracks)
