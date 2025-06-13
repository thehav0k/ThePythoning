## Music video player using webbrowser and requests
import webbrowser
import requests
from urllib.parse import quote

def search_youtube(query):
    """Search YouTube for a query and return the first video URL."""
    search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
    resp = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        return None
    # Find video IDs in the HTML
    import re
    matches = re.findall(r"/watch\?v=([\w-]{11})", resp.text)
    if matches:
        return f"https://www.youtube.com/watch?v={matches[0]}"
    return None

def play_youtube_video(url_or_query):
    """Open a YouTube video in the default web browser. Accepts URL, video ID, or search query."""
    if url_or_query.startswith("http"):
        url = url_or_query
    elif len(url_or_query) == 11 and url_or_query.isalnum():
        url = f"https://www.youtube.com/watch?v={url_or_query}"
    else:
        url = search_youtube(url_or_query)
        if not url:
            print("No results found.")
            return
    webbrowser.open(url)

if __name__ == "__main__":
    video_input = input("Enter YouTube video URL, ID, or song name: ")
    play_youtube_video(video_input)
