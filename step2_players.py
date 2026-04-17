"""
DURAK - Step 2: Players

"""
from step1_cards import Card, Deck, Suit, Rank


# Base Player

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] = []


    def draw(self, cards: list[Card]):
        """Add cards to hand"""
        self.hand.extend(cards)

    def remove_card(self, card: Card):
        """Remove a specific card from hand"""
        self.hand.remove(card)

    def has_cards(self) -> bool:
        return len(self.hand) > 0
    
    def show_hand(self):
        print(f"\n{self.name}'s hand:")
        for i, card in enumerate(self.hand):
            print(f"  [{i}] {card}")

    def __str__(self):
        return f"{self.name} ({len(self.hand)} cards)"