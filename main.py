import random
import csv
from weasyprint import HTML
from pathlib import Path
import sys


def read_csvs(csv_folder: Path, movie_name: str = None) -> list:
    """
    reads general cliche csv and if a specific movie is specified that one too
    returns a list of cliches
    also needs to return a list of center bingo options
    maybe a dict of the two for ease
    :param csv_folder:
    :param movie_name:
    :return:
    """
    # TODO
    pass


def bingo_quotes(quotes: dict) -> dict:
    # TODO take list of all quotes and return list of 24 random ones and one center option
    pass


def card_html():
    # TODO use html template and quotes to make a html for the specific bingo card
    pass


def card_html_to_pdf():
    # TODO read card html and convert all to pdfs
    pass


def main():
    # TODO parse cmd line arguments for movie csv name, number of bingo cards required
    # TODO make bingo cards
    pass


if __name__ == "__main__":
    main()
