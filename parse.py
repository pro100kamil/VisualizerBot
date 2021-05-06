from requests import request
from bs4 import BeautifulSoup

WIKI_URL = 'https://ru.wikipedia.org/wiki/'


def get_text(url: str) -> str:
    """Возвращает текст со страницы"""
    html = request(
        method='GET',
        url=WIKI_URL + url
    ).content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.find('div', class_='mw-parser-output')
    return content.text if content else ''


def get_links_from_page(url: str) -> set:
    """Возвращает все ссылки со страницы"""
    links = set()  # все ссылки
    html = request(
        method='GET',
        url=WIKI_URL + url
    ).content.decode('utf-8')

    soup = BeautifulSoup(html, 'html.parser')

    content = soup.find('div', class_='mw-parser-output')
    if content:
        for link in content.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/wiki/'):
                links.add(link.get('href').replace('/wiki/', ''))
    return links


def get_links_from_pages(url: str, depth: int) -> set:
    """Возвращает все ссылки со страниц с конкретной глубиной от основной"""
    if depth == 1:
        return {url}
    last_links = get_links_from_page(url)  # ссылки на текущей глубине
    all_links = last_links.copy()  # все ссылки

    for i in range(2, depth):
        cur_links = set()  # ссылки на текущей глубине
        for link in last_links:
            tmp = get_links_from_page(link)
            for link1 in tmp:
                if link1 not in all_links:
                    cur_links.add(link1)
                    all_links.add(link1)
        last_links = cur_links.copy()

    return all_links


def get_all_text(links: set) -> str:
    text = ''
    for link in links:
        text += get_text(link)
    return text
