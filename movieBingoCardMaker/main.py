import random
from jinja2 import Environment, FileSystemLoader
import csv
from pathlib import Path


# TODO getopts to set parameters
# TODO menu for selecting movie (set by csv title)
# TODO read quotes from csv files (seperate for center (freebie), reg cliches, movie specific)
# TODO options for amount of movie vs cliches
# TODO options for how many bingo cards
# TODO set title depending on movie
def load_quotes_csv(csv_file: Path) -> list:
    """
    Load quotes from csv file and returns a flattened list
    :param csv_file: path object for csv file
    :return:
    """
    with csv_file.open('r') as f:
        csv_reader = csv.reader(f)
        quotes = [str(q).strip() for row in csv_reader for q in row]

    print(quotes)

    return quotes


def shuffle_quotes(quotes: list, length: int) -> list:
    """
    shuffles quotes and returns a list of the requested length
    :param quotes:
    :param length:
    :return:
    """
    random.shuffle(quotes)

    return quotes[:length]


def generate_bingo_card():

    # Create a 5x5 grid with quotes
    card = [quotes[i:i+5] for i in range(0, 25, 5)]

    return card


def draw_bingo_card_html(card):
    env = Environment(loader=FileSystemLoader('..'))
    template = env.get_template('movieBingoCardMaker/assets/card.html')

    html_content = template.render(card=card)

    with open("bingo_card.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print("Bingo card saved as bingo_card.html")


if __name__ == "__main__":
    # card = generate_bingo_card()
    # draw_bingo_card_html(card)
    files = Path('./data').glob('*.csv')
    for file in files:
        print(file.name)
        cards = load_quotes_csv(file)
