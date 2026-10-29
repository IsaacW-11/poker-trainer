import pytest

from trainer.cards import card_to_num, num_to_card
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

#