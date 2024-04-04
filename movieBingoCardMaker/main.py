import random
from jinja2 import Environment, FileSystemLoader
import csv
from pathlib import Path
import argparse


def load_quotes_csv(csv_file: Path) -> list:
    """
    Load quotes from csv file and returns a flattened list
    :param csv_file: path object for csv file
    :return:
    """
    with csv_file.open('r') as f:
        csv_reader = csv.reader(f)
        quotes = [str(q).strip() for row in csv_reader for q in row]

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
    # command line options for specific movie quotes, the amount of bingo cards, and percentage of movie vs cliches
    parser = argparse.ArgumentParser(
        prog='movieBingoCardMaker',
        description='Makes html bingo cards using movie cliches and movie specific quotes'
    )
    parser.add_argument(
        '-f',
        '--file',
        help="csv with movie specific quotes, must be placed in the data directory. "
             "If not provided only movie cliches will be used"
    )
    parser.add_argument(
        '-c',
        '--count',
        type=int,
        default=3,
        help="number of bingo cards to generate"
    )
    parser.add_argument(
        '-q',
        '--quotes',
        type=int,
        default=50,
        help='Percentage of bingo squares to use movie specific quotes'
    )
    args = parser.parse_args()

    # load quotes and cliches
    path_base = Path(__file__).parent.joinpath('data')
    path_free = path_base.joinpath('free.csv')
    path_cliches = path_base.joinpath('cliches.csv')
    path_movie = path_base.joinpath(f'{args.file}') if args.file is not None else None

    # ensure all required files exist
    for f in [path_free, path_cliches, path_movie]:
        if f is not None:
            if not f.exists():
                raise FileNotFoundError(
                    f"{f.name} does not exist. Please make sure {f.name} is placed in the data directory."
                )

    quotes_free = load_quotes_csv(path_free)
    quotes_cliches = load_quotes_csv(path_cliches)
    quotes_movie = load_quotes_csv(path_movie) if args.file is not None else []

    print(quotes_free, quotes_cliches, quotes_movie, sep='\n')
    title_replace = {
        '-': ' ',
        '_': ' '
    }
    title = ''.join([title_replace.get(ch, ch) for ch in path_movie.stem]).title() if args.file is not None else None
    print(title)
    # TODO loop over required cards
    # TODO shuffle quotes
    # TODO make card
    # TODO export card

    # card = generate_bingo_card()
    # draw_bingo_card_html(card)
    # TODO set title depending on movie
