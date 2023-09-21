from deck import Deck
from player import Player
import click
from os.path import isfile
import json

class Pbj:
    def __init__(self):
        if not isfile('state.json'):
            data = {}
            data['prog'] = "New"
            with open('state.json', 'w') as f:
                json.dump(data,f)
        self._read_state()

    def _read_state(self):
        with open('state.json', 'r') as f:
            state = json.load(f)
        if state["prog"] == "New" or state["prog"] == "End":
            self.prog = "New"
            self.deck = Deck()
            self.dealer = Player()
            self.turn = 0
            return
        self.turn = state["turn"]
        self.prog = state["prog"]
        self.deck = Deck(state["deck"])
        self.dealer = Player(state["dealer"])
        self.players = []
        for player in state["players"]:
            self.players.append(Player(player))
        
    def _write_state(self):
        with open('state.json', 'w') as f:
            json.dump(self, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def play(self, pcount):
        if self.prog == "Cont":
            self.display_game_state()
            return
        click.echo('Lets play some blackjack.')
        self.players = self._generate_players(pcount)
        self.deck.shuffle()    
        self._deal_cards()
        self.prog = "Cont"
        self._write_state()
        self.display_game_state()

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

    def display_game_state(self):
        click.clear()
        click.echo("---------- Blackjack Game In Progress ----------")
        click.echo()

        click.echo("Dealer's Hand:")
        click.echo(self.dealer.get_hand_ascii())
        click.echo()

        for player_idx, player in enumerate(self.players):
            click.echo(f"Player {player_idx + 1}'s Hand:")
            click.echo(player.get_hand_ascii())
            click.echo()

        progress = self.prog
        turn = self.turn
        if progress == "Cont":
            click.echo(f"Game in progress. It's Player {turn + 1}'s turn.")
        elif progress == "End":
            click.echo("Game over.")
        click.echo()