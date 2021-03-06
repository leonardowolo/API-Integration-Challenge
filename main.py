import requests, json
import base64
from columnar import columnar
from requests.api import get


authentication_url = "https://accounts.spotify.com/api/token"
authentication_header = {}
authentication_data = {}


def getAccessToken(clientID, clientSecret):
    # Encode Client ID & Client Secret
    message = clientID + ":" + clientSecret
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    # Create URL and get response status
    authentication_header["Authorization"] = "Basic " + base64_message
    authentication_data["grant_type"] = "client_credentials"
    url_response = requests.post(authentication_url, headers=authentication_header, data=authentication_data)

    # Return useful data (access token or None)
    if url_response.status_code != 200:
        return None
    else:
        # Get Access Token
        url_data = url_response.json()
        access_token = url_data["access_token"]
        return access_token


# Function to get the playlist by athenticating with the access token
def getPlaylistTracks(access_token, playlistID):
    # Create Endpoint URL
    playlistEndpoint = "https://api.spotify.com/v1/playlists/" + playlistID

    # Create GET Header
    getHeader = {"Authorization": "Bearer " + access_token}

    # Get the Response
    url_request = requests.get(playlistEndpoint, headers=getHeader)

    # Save json Data
    url_data = url_request.json()
    return url_data




################################################
##     Main Programe                          ##
################################################

# API Requests + Check User Authentication
user_clientID = input("Enter your Spotify Client ID: ")
user_ClientSecret = input("Enter your Spotify Client Secret code: ")
access_token = getAccessToken(user_clientID, user_ClientSecret)


# Check for return value of getAccesToken()
if not access_token:
    print("Authentication Failed!")
else:
    # Get user playlist
    user_playlist_url = input("Enter the playlist url (enter 'quit' or 'exit' to stop): ")

    # While user doesn't enter "quit" or "exit" keep asking for a playlist url
    while user_playlist_url:
        if user_playlist_url.lower() in ["quit", "exit"]:
            user_playlist_url = False
        else:
            # Check for valid urls
            check_playlist_url = user_playlist_url.find("https://open.spotify.com/playlist/")
            if check_playlist_url == -1:
                print("Playlist not found! \n")
                user_playlist_url = input("Enter the playlist url (enter 'quit' or 'exit' to stop): ")
            else:
                # If user url is valid strip first part and store the playlist ID
                playlistID = user_playlist_url.lstrip("https://open.spotify.com/playlist/")

                # Json Data from playlist
                trackList = getPlaylistTracks(access_token, playlistID)

                # Create data table
                headers = ["NUMBER", "TITLE", "ARTIST", "ALBUM", "TIME"]
                track_counter = 0
                data = []

                for track in trackList["tracks"]["items"]:
                    track_counter += 1
                    song_name = track["track"]["name"].capitalize()
                    artist_name = track["track"]["artists"][0]["name"].capitalize()
                    album_name = track["track"]["album"]["name"].capitalize()
                    time = track["track"]["duration_ms"]
                    time_min = (int(time) / 1000) / 60
                    current_data = [track_counter, song_name, artist_name, album_name, "{:.2f}".format(time_min) + " min"]
                    data.append(current_data)

                table = columnar(data, headers, no_borders=False)
                print(table)
                print()
                user_playlist_url = input("Enter the playlist url (enter 'quit' or 'exit' to stop): ")


# End
print("\nBye, see you soon!")
