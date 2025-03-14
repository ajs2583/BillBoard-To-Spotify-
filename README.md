# Billboard to Spotify Playlist Generator

This project scrapes the Billboard Hot 100 chart for a given date and creates a corresponding playlist on Spotify.

## Features
- Scrapes the Billboard Hot 100 chart for a specified date
- Searches for songs on Spotify
- Creates a Spotify playlist with the retrieved songs
- Uses Spotipy for Spotify API interactions

## Requirements
- Python 3.x
- Spotify Developer account
- Billboard Hot 100 website access

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/ajs2583/billboard-spotify-playlist.git
   cd billboard-spotify-playlist
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Create a Spotify Developer App:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Log in with your Spotify account
   - Click **Create an App**, name it, and set a description
   - Copy your `Client ID` and `Client Secret`
   - Set the **Redirect URI** to `http://example.com` (or your preferred URI)

4. Create a `.env` file in the project root and add your Spotify credentials:
   ```ini
   CLIENT_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret
   REDIRECT_URI=http://example.com
   USERNAME=your_spotify_username
   ```

## Usage

Run the script:
```sh
python main.py
```

Follow the prompts to enter a date in `YYYY-MM-DD` format. The script will:
- Scrape the Billboard Hot 100 songs for the given date
- Search for the songs on Spotify
- Create a private Spotify playlist and add the found songs

## Troubleshooting

- Ensure your Spotify credentials are correct.
- If songs are not found, the Billboard page structure may have changed.
- If authentication fails, delete `token.txt` and re-run the script.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to open issues or submit pull requests!

---

Happy coding!

