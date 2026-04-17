"""
DURAK - Step 2: Players
Depends on step1_cards.py — keep both files in the same folder.
"""
 
from step1_cards import Card, Deck, Suit, Rank
 
 
# Base Player
 
class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] = []
 
    def draw(self, cards: list[Card]):
        """Add cards to hand."""
        self.hand.extend(cards)
 
    def remove_card(self, card: Card):
        """Remove a specific card from hand."""
        self.hand.remove(card)
 
    def has_cards(self) -> bool:
        return len(self.hand) > 0
 
    def show_hand(self):
        print(f"\n{self.name}'s hand:")
        for i, card in enumerate(self.hand):
            print(f"  [{i}] {card}")
 
    def __str__(self):
        return f"{self.name} ({len(self.hand)} cards)"
 
 
# Human Player
 
class HumanPlayer(Player):
    def __init__(self, name: str = "You"):
        super().__init__(name)
 
    def choose_card(self, valid_cards: list[Card], prompt: str = "Choose a card") -> Card | None:
        """
        Ask the human to pick a card from valid_cards.
        Returns None if the player wants to pass (e.g. stop attacking).
        """
        if not valid_cards:
            return None
 
        print(f"\n{prompt}:")
        for i, card in enumerate(valid_cards):
            print(f"  [{i}] {card}")
        print("  [p] Pass / Stop")
 
        while True:
            choice = input("Your choice: ").strip().lower()
            if choice == 'p':
                return None
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(valid_cards):
                    return valid_cards[idx]
            print("  Invalid input, try again.")
 
 
# AI Player
 
class AIPlayer(Player):
    def __init__(self, name: str = "AI"):
        super().__init__(name)
 
    def choose_attack_card(self, table_ranks: set[Rank], trump: Suit) -> Card | None:
        """
        Pick the weakest card to attack with.
        On the first attack (empty table), play lowest non-trump if possible.
        On follow-up attacks, only play ranks already on the table.
        """
        if not self.hand:
            return None
 
        if table_ranks:
            # Can only add cards whose rank is already on the table
            candidates = [c for c in self.hand if c.rank in table_ranks]
        else:
            candidates = list(self.hand)
 
        if not candidates:
            return None
 
        # Prefer non-trump, then pick lowest rank
        non_trump = [c for c in candidates if c.suit != trump]
        pool = non_trump if non_trump else candidates
        return min(pool, key=lambda c: c.rank.value)
 
    def choose_defense_card(self, attack_card: Card, trump: Suit) -> Card | None:
        """
        Pick the cheapest card that beats the attack card.
        Prefer same-suit beats; use trump only as last resort.
        """
        same_suit = [c for c in self.hand if c.suit == attack_card.suit and c.beats(attack_card, trump)]
        if same_suit:
            return min(same_suit, key=lambda c: c.rank.value)
 
        trump_cards = [c for c in self.hand if c.suit == trump and c.beats(attack_card, trump)]
        if trump_cards:
            return min(trump_cards, key=lambda c: c.rank.value)
 
        return None   # can't defend → must take
 
 
# Quick test
 
if __name__ == "__main__":
    deck = Deck()
    trump = deck.cards[-1].suit
    print(f"Trump: {trump.value}\n")
 
    human = HumanPlayer("Zaur")
    ai    = AIPlayer("Tahmina")
 
    human.draw(deck.deal(6))
    ai.draw(deck.deal(6))
 
    human.show_hand()
    ai.show_hand()
 
    print(f"\n{deck} remaining.")
 
    attack = ai.choose_attack_card(set(), trump)
    print(f"\nAI attacks with: {attack}")
 
    if attack:
        defense = human.hand[0]   # just grab first card for demo
        print(f"Does {defense} beat {attack}? → {defense.beats(attack, trump)}")