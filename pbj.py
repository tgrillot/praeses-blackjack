from deck import Deck
from player import Player
import click
from os.path import isfile
import json

class Pbj:
    def __init__(self,newgame=False):
        if not isfile('state.json') or newgame:
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
        self.deck = Deck(state["deck"]["deck"])
        self.dealer = Player(state["dealer"])
        self.players = []
        for player in state["players"]:
            self.players.append(Player(player))
        
    def _write_state(self):
        with open('state.json', 'w') as f:
            json.dump(self, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)

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

    def _display_state(self):
        #click.clear()
        click.echo("---------- Blackjack Game In Progress ----------")
        click.echo()
        click.echo("Dealer's Hand:")
        click.echo(self.dealer.get_hand_ascii("d",self.turn,len(self.players)))
        if self.dealer.nat == True:
            click.echo("Natural 21!")
        click.echo()

        for player_idx, player in enumerate(self.players):
            click.echo(f"Player {player_idx + 1}'s Hand:")
            click.echo(player.get_hand_ascii("p",self.turn,len(self.players)))
            click.echo("Hand Value: " + str(player.total))
            if player.nat == True:
                click.echo("Natural 21!")
            if player.bust == True:
                click.echo("Bust!")
            click.echo()

        progress = self.prog
        turn = self.turn
        if progress == "Cont":
            click.echo(f"It's Player {turn}'s turn. Please choose whether to hit or stand.")
        elif progress == "End":
            click.echo("Game over.")
        click.echo()
    
    def _eval_all(self):
        click.echo("Evaluating hands...")
        self.dealer.evaluate()
        for player in self.players:
            player.evaluate()
    
    def play(self, pcount, ):
        if self.prog == "Cont":
            self._display_state()
            return
        click.echo('Lets play some blackjack.')
        self.players = self._generate_players(pcount)
        self.deck.shuffle()    
        self._deal_cards()
        self.prog = "Cont"
        self.turn = 1
        self._eval_all()
        self._write_state()
        self._display_state()

    def hit(self):
        pi = self.turn - 1
        self.players[pi].hand.append(self.deck.draw_card())
        self.players[pi].evaluate()
        if self.players[pi].total >= 21:
            self.turn += 1
        self._write_state()
        self._display_state()
        
    
    def stand(self):
        self.turn += 1
        self._write_state()
        self._display_state()