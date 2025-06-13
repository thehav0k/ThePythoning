import requests
from bs4 import BeautifulSoup
import json

def scrape_cnn_news():
    url = "https://edition.cnn.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    } # Pretending to be a browser to avoid blocking
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        articles = []
        seen = set()

        # Selectors for different article titles and links
        selectors = ['h3.cd__headline a','a.container__link','a.card','h2 span a']
        for selector in selectors:
            for a in soup.select(selector):
                title = a.get_text(strip=True)
                link = a.get('href')
                if not title or title in seen:
                    continue
                seen.add(title)
                if link and link.startswith('/'):
                    link = 'https://edition.cnn.com' + link
                articles.append({'title': title, 'link': link, 'subtitle': None})

        return articles

    except requests.RequestException as e:
        print(f"HTTP error: {e}")
        return []

if __name__ == "__main__": # absolute main function
    news = scrape_cnn_news()
    print(f"Found {len(news)} articles\n")
    for i, art in enumerate(news[:10], 1):
        print(f"{i}. {art['title']}")
        print(f"   {art['link']}\n")

    with open('cnn_news.json', 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print("Saved to cnn_news.json")
