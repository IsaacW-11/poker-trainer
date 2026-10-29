import re

from trainer.constants import RANKS, SUITS

def card_to_num(card: str) -> int:
    if not isinstance(card, str):
        raise TypeError("Invalid type")
    if len(card) != 2:
        raise ValueError("Invalid card format")

    card_rank = card[0].upper()
    card_suit = card[1].lower()

    rank_num = RANKS.index(card_rank)
    suit_num = SUITS.index(card_suit)

    card_num = rank_num * 4 + suit_num

    return card_num

def num_to_card(num: int) -> str:
    if not isinstance(num, int) or isinstance(num, bool):
        raise TypeError("Invalid type")
    if num < 0:
        raise ValueError("Num cannot be negative")
    if num > 51:
        raise ValueError("Num cannot be greater than 51")

    card_rank = num // 4
    card_suit = num % 4

    card = RANKS[card_rank] + SUITS[card_suit]

    return card

def parse_hand(hand: str) -> list[int]:
    if not isinstance(hand, str):
        raise TypeError("Invalid type")

    sanitized_text = "".join(hand.split()) # removes whitespace

    if not len(sanitized_text) % 2 == 0:
        raise ValueError("Not correct length. At least 1 card was not complete")


    card_list = re.findall(r".{2}", sanitized_text)
    card_num_list = []

    for card in card_list:
        card_num_list.append(card_to_num(card))

    if len(card_num_list) != len(set(card_num_list)):
        raise ValueError("Duplicate cards")

    return card_num_list