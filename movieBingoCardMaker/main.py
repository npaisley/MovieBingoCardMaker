import random
from jinja2 import Environment, FileSystemLoader
import csv
from pathlib import Path
import argparse

# make parameter Enum


def load_quotes_csv(csv_file: Path) -> list:
    """
    Load quotes from csv file and returns a flattened list
    :param csv_file: path object for csv file
    :return:
    """
    with csv_file.open('r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        quotes = [str(q).strip() for row in csv_reader for q in row]

    return quotes


def calc_quote_amount(quotes: list[list[str]], ratios: list[int], length: int) -> list[int]:
    """
    Calculate amount of quotes needed from each quote list to give the required amount of quotes
    but also satify the requested quote ratio as best as possible
    :param quotes: list of quote lists
    :param ratios: Must be same length as quotes
    :param length: total number of quotes required
    :return: list of int corresponding the amount of quotes needed from each list in `quotes`
    """
    # ensure ratio list is the same length as the quotes list
    if len(quotes) != len(ratios):
        raise ValueError('insufficient ratios supplied to shuffle quotes')

    # check if there are enough quotes to return the requested amount
    if length > (total := sum([len(i) for i in quotes])):
        raise ValueError(f'insufficient quotes supplied. {total} found but {length} required')

    # determine the number of quotes that are needed from each list
    requested = [round(length * (i / sum(ratios))) for i in ratios]
    available = [len(i) for i in quotes]

    # set the amount of quotes from each list required or the number of quotes in th elist if it isnt long enough
    amount = [r if r <= a else a for r, a in zip(requested, available)]
    req_amt_diff = sum(requested) - sum(amount)

    # iterate over the list until there are enough quotes to satisfy list but not more than any list contains
    iteration = 0
    while req_amt_diff != 0:
        change_bools = [0 if r > n else 1 for r, n in zip(requested, amount)]  # list with extra quotes
        chng_amt = sum(change_bools)  # number of lists that can be increased

        # amount of missing quotes that are required split into even integers
        diff_split = [req_amt_diff // chng_amt + (1 if x < req_amt_diff % chng_amt else 0) for x in range(chng_amt)]

        # set new amount by adding additional quotes to lists that have extras
        amount = [i + diff_split.pop() if x == 1 else i for i, x in zip(amount, change_bools)]
        req_amt_diff = sum(requested) - sum(amount)  # recheck if enough quotes have been assigned

        if (iteration := iteration + 1) >= len(quotes):  # just incase to prevent endless loop
            print(f"while loop broken: {iteration}")  # add error as if this happens somethings gone wrong
            break

    return amount


def shuffle_quotes(quotes: list[list[str]], quote_amount: list[int]) -> list[str]:
    """
    shuffle each list of quotes and then take the desired number of quotes. Reuturn a list of the shuffled quotes
    desired length. Assumes that enough quotes are provided and there are a matching number of quote lists and amount
    of requested
    :param quotes: list of quote lists
    :param quote_amount: number of quotes to use from each list
    :return: list of quotes
    """
    # shuffle quotes
    for i in quotes:
        random.shuffle(i)

    shuffled = [i[:x] for i, x in zip(quotes, quote_amount)]
    shuffled = [i for q in shuffled for i in q]

    return shuffled


def make_bingo_card(options: list[str], name: str) -> None:
    env = Environment(loader=FileSystemLoader('..'))
    template = env.get_template('movieBingoCardMaker/assets/cardTemplate.html')  # set with path object
    # TODO set title in template

    html_content = template.render(card=[options[q:q + 5] for q in range(0, 25, 5)])  # TODO set bingo size with variable

    with open(f"export/{name}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Bingo card saved as {name}.html")


def save_bingo_card(html_content: str) -> None:
    # TODO save to export folder
    #  use file title
    pass


def title_from_file_name(file_path: Path) -> str:
    """
    takes the file name and outputs a title formatted in title case by replacing - and _ with spaces
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
    parser.add_argument(  # TODO allow for a list of names to be inputted well (--players)
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
    path_movie = path_base.joinpath('movie').joinpath(f'{args.file}') if args.file is not None else None
    print(path_movie)

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
    quotes_req = calc_quote_amount([quotes_cliches, quotes_movie], [50, 50], 24)  # TODO set ratio according to cmd options
    print(f"{quotes_req=}")

    for i in range(args.count):
        bingo_quotes = shuffle_quotes([quotes_cliches, quotes_movie], quotes_req)
        # print(bingo_quotes)

        # shuffle free space options and insert at required index
        random.shuffle(quotes_free)
        bingo_quotes.insert(12, quotes_free[0])

        # make bingo card and save it
        make_bingo_card(bingo_quotes, f"{title}-{i}")

    # TODO set title depending on movie
