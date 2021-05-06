from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler

from text_analyzer import TextAnalyzer
from parse import get_links_from_pages, get_all_text

TOKEN = '1861188889:AAGu61Kgfh6CNbFuqKP6o4o38tLerG4lngM'

print('Происходит парсинг, подождите')

# name, depth = 'Python', 1
name, depth = 'Задача', 2
res = get_links_from_pages(name, depth)
text = get_all_text(res)
analyzer = TextAnalyzer(text)


def text_handler(update, context):
    update.message.reply_text(f'Я реагирую только на команды')


def start(update, context):
    update.message.reply_text(
        "Привет! Нажми /help, чтобы узнать мои команды и возможности.",
        reply_markup=ReplyKeyboardMarkup(
            [['/help', '/stop_words', '/describe']],
            resize_keyboard=True))


def help(update, context):
    update.message.reply_text("""
/top N (asc | desc) - топ самых часто (редко) используемых слов, но без учета выбросов;
/stop_words - слова-выбросы;
/word_cloud COLOR - нарисовать облако слов;
/describe - выводит статистику по данным;
/describe WORD - выводит статистику по данному слову в тексту""")


def top(update, context):
    if len(context.args) == 2:
        n, criterion = context.args[:2]
        if not (n.isdigit() and criterion in {'asc', 'desc'} and n != '0'):
            update.message.reply_text('Неправильное использование')
        elif int(n) > 100:
            update.message.reply_text('Слишком большое число')
        else:
            lst = analyzer.top_words(int(n), criterion == 'asc')
            update.message.reply_text('\n'.join(lst))
    else:
        update.message.reply_text('Неправильное использование')


def stop_words(update, context):
    if analyzer.stop_words():
        update.message.reply_text('Слова-выбросы:\n' +
                                  ', '.join(analyzer.stop_words()))
    else:
        update.message.reply_text('Слова-выбросы не найдены')


def word_cloud(update, context):
    if len(context.args) == 1:
        color = context.args[0]
        try:
            analyzer.word_cloud(color)
            update.message.reply_photo(
                open('word_cloud.png', 'rb'),
                caption='Облако слов'
            )
        except Exception as e:
            print(e)
            update.message.reply_text('Неправильный цвет')
    else:
        update.message.reply_text('Неправильное использование')


def describe(update, context):
    if len(context.args) == 0:
        update.message.reply_text(analyzer.describe())
    elif len(context.args) == 1:
        word = context.args[0]
        update.message.reply_text(analyzer.describe_word(word))
    else:
        update.message.reply_text('Неправильное использование')


def start_bot():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("top", top, pass_args=True))
    dp.add_handler(CommandHandler("stop_words", stop_words))
    dp.add_handler(CommandHandler("word_cloud", word_cloud, pass_args=True))
    dp.add_handler(CommandHandler("describe", describe, pass_args=True))

    dp.add_handler(MessageHandler(Filters.text, text_handler))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print('Бот запущен')
    start_bot()
