import random
import click

class Deck:
    def __init__(self, decks, pre=None):
        if pre == None:
            self.deck = self._generate_deck(decks)
        else:
            self.deck = pre

    def _generate_deck(self, decks):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["\u2665","\u2666","\u2663","\u2660"]
        deck = []
        for suit in suits:
            for rank in ranks:
                card = {"rank": rank, "suit": suit, "value": self._get_card_value(rank)}
                deck.append(card)
        return deck * decks

    def _get_card_value(self, rank):
        if rank in ["10", "J", "Q", "K"]:
            return 10
        elif rank == "A":
            return 11
        else:
            return int(rank)

    def shuffle(self):
        click.echo('Shuffling the deck...')
        random.shuffle(self.deck)

    def cut(self,x,decks):
        part = 100 - (x + 19)
        count = decks * 52.0
        cut = round((part * count) / 100)
        cut_card = {"rank":"C","suit":" ","value":0}
        self.deck.insert(cut,cut_card)

    def draw_card(self):
        if not self.deck:
            return None
        return self.deck.pop(0)

        