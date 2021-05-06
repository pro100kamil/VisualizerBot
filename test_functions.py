from parse import get_links_from_pages
from create_word_cloud import create_word_cloud

if __name__ == '__main__':
    # тестирование парсинга
    links = get_links_from_pages('Python', 2)
    print(len(links))
    links = get_links_from_pages('Земля', 2)
    print(len(links))
    links = get_links_from_pages('Солнце', 1)
    print(len(links))
    # тестирование создания облака слов
    create_word_cloud(["Test", "Test123", "Test153",
                       "Test Test", "Test123", "Test153",
                       "Test", "Test123", "Test153",
                       "Test Test", "Test123", "Test153",
                       "Test", "Test123", "Test153"], 'green')
