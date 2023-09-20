import random
import click

class Deck:
    def __init__(self):
        self.deck = self._generate_deck()

    def _generate_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        deck = []
        for suit in suits:
            for rank in ranks:
                card = {"rank": rank, "suit": suit, "value": self._get_card_value(rank)}
                deck.append(card)
        return deck

    def _get_card_value(self, rank):
        if rank in ["10", "Jack", "Queen", "King"]:
            return 10
        elif rank == "Ace":
            return 11
        else:
            return int(rank)

    def shuffle(self):
        click.echo('Shuffling the deck...')
        random.shuffle(self.deck)

    def draw_card(self):
        if not self.deck:
            return None
        return self.deck.pop()

    @property
    def deck_count(self):
        return len(self.deck)

        