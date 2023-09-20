from deck import Deck
from player import Player
import click

class Pbj:
    def __init__(self, pcount):
        click.echo('Lets play some blackjack.')
        self.deck = Deck()
        self.dealer = Player()
        self.players = self._generate_players(pcount)
        self.deck.shuffle()    
        self._deal_cards()
        self.show_game_state()
        click.echo(self.deck.deck_count)

    def _generate_players(self, pcount):
        players = []
        for i in range(pcount):
            player = Player()
            players.append(player)
        return players

    def _deal_cards(self):
        click.echo('Dealing cards...')
        deal = 0
        while deal < 2:
            for player in self.players:
                player.hand.append(self.deck.draw_card())
            self.dealer.hand.append(self.deck.draw_card())
            deal += 1

    def show_game_state(self):
        click.echo("Dealer Hand:")
        for card in self.dealer.hand:
            click.echo(card['rank'] + ' of ' + card['suit'])
        for player in self.players:
            click.echo('Player ' + str(self.players.index(player) + 1) + ' Hand:')
            for card in player.hand:
                click.echo(card['rank'] + ' of ' + card['suit'])
        click.echo(self.deck.deck_count)
