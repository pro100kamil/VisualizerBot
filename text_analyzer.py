from collections import Counter
from create_word_cloud import create_word_cloud


class TextAnalyzer:
    def __init__(self, text: str):
        # все слова
        self.words = list(map(str.lower,
                              filter(lambda el: el.isalpha(), text.split())))
        # слова с их частотой
        self.counter = Counter(self.words)

        # средняя частота
        avg = sum(self.counter.values()) / len(self.counter)
        # стандартное отклонение
        st_dev = (sum([(el - avg) ** 2
                       for el in self.counter.values()])
                  / (len(self.words) - 1)) ** 0.5
        # слова-выбросы
        self.stop_words_ = [word for word, v in self.counter.items() if
                            abs(v - avg) > st_dev * 3]

        # слова по частоте использования c выбросами
        self.top = sorted(self.counter,
                          key=lambda el: self.counter[el], reverse=True)
        # слова по частоте использования без выбросов
        self.top_asc = sorted(set(self.counter) - set(self.stop_words_),
                              key=lambda el: self.counter[el], reverse=True)
        # слова по редкости использования без выбросов
        self.top_desc = self.top_asc[::-1]
        # длины слов с общим кол-вом таких длин
        self.lengths_words = Counter(map(lambda el: len(el), self.words))

        # длина самого длинного слова и само слово
        self.longest_word = [max(self.lengths_words.elements())]
        self.longest_word += [word for word in self.words
                              if len(word) == self.longest_word[0]][0]

    def top_words(self, kol: int, asc: bool) -> list:
        return self.top_asc[:kol] if asc else self.top_desc[:kol]

    def stop_words(self) -> list:
        return self.stop_words_

    def word_cloud(self, color: str):
        create_word_cloud(self.top[:8], color)

    def describe(self) -> str:
        most_common_length = self.lengths_words.most_common(1)[0]
        rarest_length = self.lengths_words.most_common()[-1]

        lengths = list(map(lambda el: str(el[0]),
                           self.lengths_words.most_common()))
        return f'Всего слов: {len(self.words)}\n' \
               f'Самое популярное слово: {self.top_asc[0]}\n' \
               f'Длины слов по попярности: {", ".join(lengths)}\n' \
               f'Самая частая длина слова: {most_common_length[0]} ' \
               f'(кол-во слов с такой длиной: {most_common_length[1]})\n' \
               f'Самая редкая длина слова: {rarest_length[0]} ' \
               f'(кол-во слов с такой длиной: {rarest_length[1]})'

    def describe_word(self, word: str) -> str:
        if word in self.counter:
            if word in self.stop_words_:
                return f'Всего в тексте: {self.counter[word]}\n' \
                       f'Слово-выброс\n' \
                       f'Количество слов с такой длиной: ' \
                       f'{self.lengths_words[len(word)]}'
            else:
                return f'Всего в тексте: {self.counter[word]}\n' \
                       f'Место по частоте: {self.top_asc.index(word) + 1}\n' \
                       f'Количество слов с такой длиной: ' \
                       f'{self.lengths_words[len(word)]}'
        else:
            return 'Этого слова нет в тексте'
