from PIL import Image, ImageDraw, ImageFont


def create_word_cloud(words: list, color: str):
    """Рисует облако слов и записывает его в файл (не больше 8 слов)"""
    size = 400, 400
    im = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(im)

    x = 25
    step_y = 50
    kol = min(len(words), 8)
    first_y = (size[1] - step_y * kol) / 2

    for i in range(kol):
        draw.text((x, first_y + step_y * i), words[i],
                  'black' if color == 'white' else 'white',
                  font=ImageFont.truetype("arial.ttf", size=52 - i * 6))

    im.save('word_cloud.png')

    return im
