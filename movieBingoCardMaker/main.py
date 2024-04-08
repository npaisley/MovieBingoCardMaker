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


def shuffle_quotes(quotes: list[list[str]], ratios: list[int], length: int) -> list:
    """
    Randomly shuffle the provided quotes according to the ratio between the two and return a list of the
    desired length
    :param quotes:
    :param ratios:
    :param length:
    :return:
    """
    # TODO clean up.
    #  Split into two functions (calc amount required from each list, shuffle and return required amount)
    #  comment code
    #  refactor so names make sense (items instead of quotes)
    # ensure ratio list is the same length as the quotes list
    if len(quotes) != len(ratios):
        raise ValueError('insufficient ratios supplied to shuffle quotes')

    # check if there are enough quotes to return the requested amount
    if length > (total := sum([len(i) for i in quotes])):
        raise ValueError(f'insufficient quotes supplied. {total} found but {length} required')

    # determine the number of quotes that are needed from each list
    requested = [round(length * (i / sum(ratios))) for i in ratios]
    available = [len(i) for i in quotes]

    amount = [r if r <= a else a for r, a in zip(requested, available)]
    diff = sum(requested) - sum(amount)

    iteration = 0
    while diff != 0:
        change_bools = [0 if r > n else 1 for r, n in zip(requested, amount)]
        total_changes = sum(change_bools)

        diff_split = [diff // total_changes + (1 if x < diff % total_changes else 0) for x in range(total_changes)]
        amount = [i + diff_split.pop() if f == 1 else i for i, f in zip(amount, change_bools)]
        diff = sum(requested) - sum(amount)

        if (iteration := iteration + 1) > 5:  # TODO make max scale with length of quotes (figure out theory max iterantions for list of length n)
            break


    # check if there are enough quotes
    # ratios_count = [r if r <= len(q) else len(q) for r, q in zip(ratios_count, quotes)]
    #
    # print(ratios_count)
    #
    # for i, r in zip(quotes, ratios):
    #     random.shuffle(i)

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


def title_from_file_name(file_path: Path) -> str:
    """
    takes the file name and outputs a title formatted in title case
    :param file_path: Path object of the file
    :return:
    """
    title_replace = {
        '-': ' ',
        '_': ' '
    }

    formatted_title = ''.join([title_replace.get(ch, ch) for ch in file_path.stem]).title() if file_path is not None else None

    return formatted_title


if __name__ == "__main__":
    # TODO put in own function
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
    path_movie = path_base.joinpath(f'{args.file}') if args.file is not None else None  # TODO put movies in subfolder

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

    title = title_from_file_name(path_movie)

    shuffled_quotes = shuffle_quotes([quotes_free, quotes_cliches, quotes_movie], [50, 50, 50], 24)
    print(shuffled_quotes, len(shuffled_quotes), sep='\n')
    # TODO loop over required cards
    # for count in args.count:


    # TODO shuffle quotes
    # TODO make card
    # TODO export card

    # card = generate_bingo_card()
    # draw_bingo_card_html(card)
    # TODO set title depending on movie
