from bs4 import BeautifulSoup
import requests
from config import *

def fetch_palylist_id(url) -> str:
    """Extracts the playlist id from the url
    Args:
        url (str): The url of the playlist
    Returns:
        str: The playlist id
    """ 
    share_link = SHARE_LINK_URL.format(url)
    # request the share link, and record the url after redeirection
    response = requests.get(share_link, headers=HEADER, allow_redirects=False)
    # trace until the final url
    while response.status_code == 302 or response.status_code == 301:
        print(response.headers["Location"])
        response = requests.get(response.headers["Location"], headers=HEADER, allow_redirects=False)
    
    playlist_url = response.url
    # extract the playlist id from the url
    playlist_id = playlist_url.split("/")[-1]
    # check if the playlist id is in number format
    if playlist_id.isdigit():
        return playlist_id
    else:
        return None
    

def fetch_playlist_soup(id):
    """Fetches the soup of the playlist page
    Args:
        id (str): The playlist id
    Returns:
        BeautifulSoup: The soup of the playlist page
    """
    playlist_url = PLAYLIST_DETAIL_URL.format(id)
    response = requests.get(playlist_url)
    return BeautifulSoup(response.text, "html.parser")

def analyse_playlist(soup):
    """Analyse the playlist and returns the list of musics
    Args:
        soup (BeautifulSoup): The soup of the playlist page
    Returns:
        list: The list of musics
    """
    musics = []
    for music in soup.find_all("a", class_="yt-simple-endpoint style-scope ytd-playlist-music-renderer"):
        title = music.find("yt-formatted-string", class_="style-scope ytd-playlist-music-renderer").text
        url = "https://www.youtube.com" + music["href"]
        musics.append({"title": title, "url": url})
    return musics

def generate_report(musics):
    """Generates the report of the playlist
    Args:
        musics (list): The list of musics
    """
    for music in musics:
        print(f"Title: {music['title']}")
        print(f"URL: {music['url']}")
        print("\n")

if __name__ == "__main__":
    playlist_id = fetch_palylist_id(PLAYLIST_TOKEN)
    
    if not playlist_id:
        print("Invalid playlist token{}".format(PLAYLIST_TOKEN))
        print("Please provide a valid playlist token and try again.")
        exit(1)
    soup = fetch_playlist_soup(playlist_id)
    musics = analyse_playlist(soup)
    generate_report(musics)