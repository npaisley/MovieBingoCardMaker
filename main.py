import random
from jinja2 import Environment, FileSystemLoader


# TODO getopts to set parameters
# TODO menu for selecting movie (set by csv title)
# TODO read quotes from csv files (seperate for center (freebie), reg cliches, movie specific)
# TODO options for amount of movie vs cliches
# TODO options for how many bingo cards
# TODO set title depending on movie
def generate_bingo_card():
    quotes = [
        "I'm trying to protect you.",
        "At least you have a home.",
        "Or die trying.",
        "Don't you die on me.",
        "Did I just say that out loud?",
        "You just don't get it.",
        "The only thing I don't regret is you.",
        "I'm in.",
        "NOOOOOOOOOOOOOOOO!",
        '"We only have one shot." or "Make it count."',
        "You're/we're no match for me/them.",
        "It was personal to me!",
        "Kill me.",
        "Only one person/thing can do/stop X.",
        "I've seen this in a dream.",
        "It's not what it looks like!",
        "You'll know it when you see it.",
        "Do you know who I am?",
        '"Don\'t laugh." tells story, they laugh',
        '"I won\'t do X." immediately does X',
        "Can I/you afford X?" "I/you can't afford not to X.",
        "We've got company!",
        "It's showtime.",
        "It's right behind me, isn't it?",
        '"I\'ve been expecting you." or "I knew you\'d come."',
        "There's no time!"
    ]

    # Randomly shuffle the quotes
    random.shuffle(quotes)

    # Create a 5x5 grid with quotes
    card = [quotes[i:i+5] for i in range(0, 25, 5)]

    return card


def load_quotes_csv():
    """
    loads cliches, freebies, and movie specifics quotes
    :return:
    """
    pass


def draw_bingo_card_html(card):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('/assets/card.html')

    html_content = template.render(card=card)

    with open("bingo_card.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print("Bingo card saved as bingo_card.html")


if __name__ == "__main__":
    card = generate_bingo_card()
    draw_bingo_card_html(card)
