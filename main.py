from PIL import Image, ImageDraw, ImageFont
import random
import csv


def generate_bingo_card():
    quotes = [
        "The fate of the kingdom rests in your hands.",
        "In darkness, light prevails.",
        "Evil knows no mercy, but neither do we.",
        "The fate of the kingdom rests in your hands.",
        "In darkness, light prevails.",
        "Evil knows no mercy, but neither do we.",
        "Destiny has a way of finding you.",
        "To save the kingdom, you must first save yourself.",
        "Fear is a weapon, and courage is its antidote.",
        "The journey may be perilous, but the reward is great.",
        "Trust not what you see, but what you feel in your heart.",
        "In the heart of danger, heroes are born.",
        "A hero is defined by deeds, not by blood.",
        "The path to redemption is paved with sacrifice.",
        "Legends are not born; they are forged.",
        "The sword chooses the wielder, not the other way around.",
        "The battle may be lost, but the war is not over.",
        "Sometimes, the greatest magic is found within.",
        "To conquer fear is the first step to true power.",
        "In the face of darkness, be the light.",
        "A true leader inspires others to believe in themselves.",
        "The scars of the past shape the warriors of the future.",
        "Magic is not in the spells but in the hearts that cast them.",
        "The greatest strength lies in unity.",
        "Even the mightiest fall, but rise stronger.",
        "The echoes of bravery resonate through the ages.",
        "The prophecy foretells, but the choices define.",
        "The battle may be won with steel, but the war is won with the spirit."
    ]

    # Randomly shuffle the quotes
    random.shuffle(quotes)

    # Create a 5x5 grid with quotes
    card = [quotes[i:i + 5] for i in range(0, 25, 5)]

    return card


def draw_bingo_card(draw, card):
    # Set up font, image size, and box size
    font = ImageFont.load_default()
    image_size = (800, 800)

    # Calculate box size based on the number of rows and columns
    rows, cols = len(card), len(card[0])
    box_size = (image_size[0] // cols, image_size[1] // rows)

    # Draw the bingo card on the image
    for i, row in enumerate(card):
        for j, quote in enumerate(row):
            box_position = (j * box_size[0], i * box_size[1])
            draw.rectangle([box_position, (box_position[0] + box_size[0], box_position[1] + box_size[1])], outline="black")
            draw.text((box_position[0] + 10, box_position[1] + 10), f"{i * 5 + j + 1}. {quote}", font=font, fill="black", width=box_size[0] - 20)


def save_bingo_card_as_jpg(card_number):
    # Create a blank image
    image = Image.new("RGB", (800, 800), "white")
    draw = ImageDraw.Draw(image)

    # Draw the bingo card on the image
    draw_bingo_card(draw, generate_bingo_card())

    # Save the image as a JPG file
    image.save(f"bingo_card_{card_number}.jpg")
    print(f"Bingo card {card_number} saved as bingo_card_{card_number}.jpg")


if __name__ == "__main__":
    for card_number in range(1, 6):
        save_bingo_card_as_jpg(card_number)
# TODO the text still doesn't wrap
