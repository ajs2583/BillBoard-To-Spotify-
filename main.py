import os
import requests
import logging
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
SPOTIPY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("REDIRECT_URI", "http://example.com")
SPOTIPY_USERNAME = os.getenv("USERNAME")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Validate essential environment variables
if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI]):
    logging.error(
        "Missing required Spotify API credentials. Please check your .env file."
    )
    exit(1)

# Initialize the Spotify client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)


def get_date():
    """Prompt the user to enter a valid date in YYYY-MM-DD format."""
    while True:
        user_input = input(
            "Enter a date (YYYY-MM-DD) to retrieve the Billboard Hot 100: "
        ).strip()
        if len(user_input) == 10 and user_input[4] == "-" and user_input[7] == "-":
            return user_input
        logging.warning("Invalid format. Please enter the date in YYYY-MM-DD format.")


def construct_url(date):
    """Construct the Billboard Hot 100 chart URL for the given date."""
    return f"https://www.billboard.com/charts/hot-100/{date}"


def scrape_data(date):
    """Scrape the Billboard Hot 100 chart for song names."""
    url = construct_url(date)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Billboard chart: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    song_name_elements = soup.select("li ul li h3")

    song_names = [song.getText().strip() for song in song_name_elements]
    if not song_names:
        logging.warning("No songs found. The page structure may have changed.")

    return song_names


def search_songs_on_spotify(song_names, year):
    """Search for songs on Spotify and return a list of valid song URIs."""
    song_uris = []
    for song in song_names:
        try:
            result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
            if result["tracks"]["items"]:
                song_uris.append(result["tracks"]["items"][0]["uri"])
            else:
                logging.info(f"Song not found on Spotify: {song}")
        except Exception as e:
            logging.error(f"Error searching for song '{song}': {e}")

    return song_uris


def create_playlist():
    """Create a Spotify playlist and add songs to it."""
    try:
        user_id = sp.current_user()["id"]
    except Exception as e:
        logging.error(f"Error retrieving user ID: {e}")
        return

    date = get_date()
    playlist_name = f"{date} Billboard 100"

    try:
        playlist = sp.user_playlist_create(
            user=user_id, name=playlist_name, public=False
        )
    except Exception as e:
        logging.error(f"Error creating playlist: {e}")
        return

    song_names = scrape_data(date)
    if not song_names:
        logging.error("No songs retrieved. Exiting.")
        return

    song_uris = search_songs_on_spotify(song_names, date.split("-")[0])

    if song_uris:
        try:
            sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
            logging.info(
                f"Successfully added {len(song_uris)} songs to playlist '{playlist_name}'."
            )
        except Exception as e:
            logging.error(f"Error adding songs to playlist: {e}")
    else:
        logging.warning("No valid songs were found on Spotify to add to the playlist.")


if __name__ == "__main__":
    create_playlist()
