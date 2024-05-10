from bs4 import BeautifulSoup

WEBPAGE_PATH = './webpage/playlist.html'

def fetch_playlist_soup():
    """Fetches the soup of the playlist webpage
    Args:
        None
    Returns:
        BeautifulSoup: The soup of the playlist page
    """
    # read the playlist webpage content form the file
    with open(WEBPAGE_PATH, "r", encoding='utf8') as file:
        content = file.read()
    return BeautifulSoup(content, "html.parser")

def analyse_playlist(soup):
    """Analyse the playlist and returns the list of musics
    Args:
        soup (BeautifulSoup): The soup of the playlist page
    Returns:
        list: The list of musics
    """
    musics = []
    music_div_list = soup.find_all("div", class_="songlist__item c_b_normal")
    for music in music_div_list:
        # 1. 歌曲名称: songlist__name
        name_span = music.find("span", class_="songlist__name")
        name_a = name_span.find("a", class_="mod_songname__name")
        name = name_a.text
        # 2. 歌手列表：songlist__singer
        single_span = music.find("span", class_="songlist__singer")
        single_a_list = single_span.find_all("a", class_="singer_name")
        singers = [single_a.text for single_a in single_a_list]
        # 3. 所在专辑：songlist_album
        album_span = music.find("span", class_="songlist__album")
        album_a = album_span.find("a", class_="album_name")
        album = album_a.text
        musics.append({
            "title": name,
            "singers": singers,
            "album": album
        }
        )
    return musics

def generate_report(musics):
    """Generates the report of the playlist
    Args:
        musics (list): The list of musics
    """
    singer_count = {}
    album_count = {}
    for music in musics:
        for singer in music["singers"]:
            singer_count[singer] = singer_count.get(singer, 0) + 1
        if music["album"] != "":
            album_count[music["album"]] = album_count.get(music["album"], 0) + 1
    # 根据出现次数进行排序，得到元组
    singer_count = sorted(singer_count.items(), key=lambda x: x[1], reverse=True)
    album_count = sorted(album_count.items(), key=lambda x: x[1], reverse=True)

    print("你的自建歌单分析报告")
    print("=====================================")
    print("在你的歌单里，现在还有{}首歌曲还可以畅听。".format(len(musics)))
    print("=====================================")

    singer_num = min(20, len(singer_count))
    print("你最喜爱的{}位歌手是:".format(singer_num))
    for singer, count in singer_count[:singer_num]:
        print(f"{singer}: {count}首歌曲。")
    
    print("=====================================")
    
    album_num = min(20, len(album_count))
    print("你最喜欢的{}张专辑是:".format(album_num))
    for album, count in album_count[:album_num]:
        print(f"{album}: {count}首歌曲。")

    print("=====================================")

if __name__ == "__main__":
    soup = fetch_playlist_soup()
    if not soup:
        print("Invalid webpages file. Please provide a valid file and try again.")
        exit(1)
    musics = analyse_playlist(soup)
    generate_report(musics)