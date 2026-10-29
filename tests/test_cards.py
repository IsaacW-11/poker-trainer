import pytest

from trainer.cards import card_to_num, num_to_card, parse_hand
from trainer.constants import RANKS, SUITS

# tests for card_to_num / num_to_card
# card_to_num accepts exactly 2 characters (representing 1 card)

@pytest.mark.parametrize("rank", RANKS)
@pytest.mark.parametrize("suit", SUITS)
def test_card_conversion(rank, suit):
    card = rank + suit
    assert num_to_card(card_to_num(card)) == card

@pytest.mark.parametrize("num", range(52))
def test_card_number_range(num):
    assert card_to_num(num_to_card(num)) == num

@pytest.mark.parametrize("card, expected_num", [
    ("2c", 0),
    ("2d", 1),
    ("7h", 22),
    ("Jc", 36),
    ("Ah", 50),
    ("As", 51),
])
def test_specific_card_conversions(card, expected_num):
    assert card_to_num(card) == expected_num
    assert num_to_card(expected_num) == card

@pytest.mark.parametrize("card", ["Ah", "aH", "AH", "ah"])
def test_case_insensitive(card):
    assert card_to_num(card) == card_to_num("Ah")

def test_num_to_card_output_format():
    assert num_to_card(card_to_num("ah")) == "Ah" # always Upper + lower no matter input
    assert num_to_card(card_to_num("tS")) == "Ts"

@pytest.mark.parametrize("card", [
    "1c",
    "Xh",
    "11c",
    "10h",
    "Az",
    "A?",
    "",
    "A",
    "h",
    "Ahx",
    "AhKd",
    "hA",
])
def test_card_to_num_invalid_strings(card):
    with pytest.raises(ValueError):
        card_to_num(card)

@pytest.mark.parametrize("card", [
    " Ah",
    "Ah ",
    " Ah ",
    "\nAh",
    "Ah\n",
    "\tAh",
    "Ah\t",
    "A h",
    "A\nh",
    "A\th",
    "  ",
    "\tA \nh\n",
])
def test_card_to_num_rejects_whitespace(card):
    with pytest.raises(ValueError):
        card_to_num(card)

@pytest.mark.parametrize("value", [50, 5.0, None, ["A", "h"], ("A", "h")])
def test_card_to_num_invalid_type(value):
    with pytest.raises(TypeError):
        card_to_num(value)

@pytest.mark.parametrize("num", [-1, -4, -52, -100, 52, 53, 100])
def test_num_to_card_out_of_bounds(num):
    with pytest.raises(ValueError):
        num_to_card(num)

@pytest.mark.parametrize("value", [5.0, 0.0, "5", "Ah", None, [5]])
def test_num_to_card_invalid_type(value):
    with pytest.raises(TypeError):
        num_to_card(value)

@pytest.mark.parametrize("value", [True, False])
def test_num_to_card_rejects_bool(value):
    with pytest.raises(TypeError):
        num_to_card(value)

# tests for parse_hand
# accepts any even number string (representing any number of cards)

@pytest.mark.parametrize("text, expected", [
    ("Ah", [50]),
    ("AhKs", [50, 47]),
    ("2c7hJcAs", [0, 22, 36, 51]),
    ("AhKdQcJsTh", [50, 45, 40, 39, 34])
])
def test_parse_hand_basic(text, expected):
    assert parse_hand(text) == expected

def test_parse_hand_seven_cards():
    cards = parse_hand("AhKd7c2s9hTdJc")
    assert len(cards) == 7
    assert [num_to_card(c) for c in cards] == ["Ah", "Kd", "7c", "2s", "9h", "Td", "Jc"]

def test_parse_hand_case_insensitive():
    assert parse_hand("ahkd") == parse_hand("AhKd")

@pytest.mark.parametrize("text", [
    "AhKd",
    "Ah Kd",
    " Ah Kd ",
    "Ah  Kd",
    "Ah\nKd",
    "\nAhKd\n",
    "\tAh\tKd\t",
    "A h K d",
    "A\nhK d",
    "  ah   kd\n",
])
def test_parse_hand_ignores_whitespace(text):
    assert parse_hand(text) == [50, 45]

@pytest.mark.parametrize("text", ["", " ", "\n", "  \t\n "])
def test_parse_hand_empty_returns_empty_list(text):
    assert parse_hand(text) == []

@pytest.mark.parametrize("text", [
    "A",
    "AhK",
    "Ah Kd 7",
    "AhXd",
    "AhKz",
    "1cAh",
    "10hAs",
    "Ah,Kd",
    "hAKd",
])
def test_parse_hand_invalid(text):
    with pytest.raises(ValueError):
        parse_hand(text)

@pytest.mark.parametrize("text", [
    "AhAh",
    "Ah ah",
    "AhKd7cAh",
    "2c 3c 4c 2c",
])
def test_parse_hand_rejects_duplicates(text):
    with pytest.raises(ValueError):
        parse_hand(text)

@pytest.mark.parametrize("value", [None, 50, ["Ah", "Kd"], ("Ah",)])
def test_parse_hand_invalid_type(value):
    with pytest.raises(TypeError):
        parse_hand(value)