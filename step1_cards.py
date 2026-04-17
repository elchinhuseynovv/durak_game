"""
DURAK GAME - STEP 1: CARDS & DECK

"""

from dataclasses import dataclass
from enum import Enum
import random


# suits and ranks

class Suit(Enum):
    HEARTS   = '♥'
    DIAMONDS = '♦'
    CLUBS    = '♣'
    SPADES   = '♠'

class Rank(Enum):
    SIX   = 6
    SEVEN = 7
    EIGHT = 8
    NINE  = 9
    TEN   = 10
    JACK  = 11
    QUEEN = 12
    KING  = 13
    ACE   = 14

# Card

@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    def beats(self, other: 'Card', trump: Suit) -> bool:
        """Return True if this card can beat `other` given the trump suit."""
        if self.suit == other.suit:
            return self.rank.value > other.rank.value
        if self.suit == trump:
            return True  #any trump beats a non-trump
        return False
    
    def __str__(self):
        return f"{self.rank.name.capitalize()}{self.suit.value}"
    
    def __repr__(self):
        return self.__str__()
    

# Deck

class Deck:
    def __init__(self):
        self.cards: list[Card] = [
            Card(rank, suit)
            for suit in Suit
            for rank in Rank
        ]
        random.shuffle(self.cards)

    def deal(self, n: int) -> list[Card]:
        dealt = self.cards[:n]
        self.cards = self.cards[:n]
        return dealt
    
    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        return f"Deck({len(self.cards)} cards)"
    

# Quick Test

if __name__ == "__main__":
    deck = Deck()
    trump = deck.cards[-1].suit      # bottom card defines trump
    print(f"Trump suit: {trump.value}    |    {deck}\n ")

    hand = deck.deal(6)
    print("Your hand:", hand)

    c1, c2 = hand[0], hand[1]
    print(f"\nDoes {c1} beat {c2}? → {c1.beats(c2, trump)}")
    print(f"Does {c2} beat {c1}? → {c2.beats(c1, trump)}")